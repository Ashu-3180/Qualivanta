"""Validate or download the official Sauce Labs demo application APK."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DESTINATION = REPOSITORY_ROOT / "demo_app" / "mda-2.3.0-27.apk"
RELEASE_API = "https://api.github.com/repos/saucelabs/my-demo-app-android/releases/tags/2.3.0"
ASSET_NAME = "mda-2.3.0-27.apk"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_apk(path: Path) -> str:
    """Validate APK ZIP structure and return its SHA-256 digest."""

    if path.name == "mda-androidTest-2.3.0-27.apk":
        raise ValueError("The androidTest APK is auxiliary instrumentation content, not the application under test.")
    if not path.is_file():
        raise FileNotFoundError(f"APK does not exist: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"APK is empty: {path}")
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if "AndroidManifest.xml" not in names:
                raise ValueError(f"APK does not contain AndroidManifest.xml: {path}")
            bad_member = archive.testzip()
            if bad_member:
                raise ValueError(f"APK ZIP integrity check failed for member {bad_member}: {path}")
    except PermissionError as exc:
        raise ValueError(f"APK cannot be read due to filesystem permissions: {path}") from exc
    except zipfile.BadZipFile as exc:
        raise ValueError(f"APK is not a valid ZIP-compatible Android package: {path}") from exc
    return sha256(path)


def _release_asset() -> tuple[str, int | None]:
    request = urllib.request.Request(RELEASE_API, headers={"Accept": "application/vnd.github+json", "User-Agent": "Qualivanta"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            metadata = json.load(response)
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not retrieve release metadata for tag 2.3.0: {exc}") from exc
    for asset in metadata.get("assets", []):
        if asset.get("name") == ASSET_NAME and asset.get("browser_download_url"):
            return asset["browser_download_url"], asset.get("size")
    raise RuntimeError(f"Release tag 2.3.0 does not contain the exact asset {ASSET_NAME}.")


def download_apk(destination: Path = DEFAULT_DESTINATION) -> Path:
    """Reuse a valid APK or safely download and validate a missing one."""

    destination = destination.expanduser()
    if destination.exists():
        digest = validate_apk(destination)
        print(f"Reusing valid APK: {destination}")
        print(f"SHA-256: {digest}")
        return destination

    url, expected_size = _release_asset()
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix=f".{destination.stem}.", suffix=".download", dir=destination.parent, delete=False) as temp:
            temp_path = Path(temp.name)
            request = urllib.request.Request(url, headers={"User-Agent": "Qualivanta"})
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    while chunk := response.read(1024 * 1024):
                        temp.write(chunk)
            except (OSError, urllib.error.URLError) as exc:
                raise RuntimeError(f"Failed to download {ASSET_NAME}: {exc}") from exc
        if expected_size is not None and temp_path.stat().st_size != expected_size:
            raise RuntimeError(f"Downloaded asset size does not match release metadata: {temp_path.stat().st_size} != {expected_size}.")
        digest = validate_apk(temp_path)
        os.replace(temp_path, destination)
        temp_path = None
        print(f"Downloaded and validated APK: {destination}")
        print(f"SHA-256: {digest}")
        return destination
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate or download the Qualivanta demo APK.")
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    args = parser.parse_args()
    try:
        download_apk(args.destination if args.destination.is_absolute() else REPOSITORY_ROOT / args.destination)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"APK validation/download failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
