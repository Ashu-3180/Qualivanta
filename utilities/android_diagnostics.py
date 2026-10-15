"""Read-only diagnostics for Android, Java, SDK, ADB, and Appium."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def run_command(command: list[str], timeout: int = 15) -> subprocess.CompletedProcess[str]:
    """Run a diagnostic command without changing system state."""

    return subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)


def adb_path(android_home: str | Path | None = None) -> str | None:
    home = Path(android_home) if android_home else None
    candidate = home / "platform-tools" / ("adb.exe" if os.name == "nt" else "adb") if home else None
    return str(candidate) if candidate and candidate.is_file() else shutil.which("adb")


def connected_devices(android_home: str | Path | None = None) -> list[dict[str, str]]:
    executable = adb_path(android_home)
    if not executable:
        raise FileNotFoundError("ADB was not found. Check ANDROID_HOME/ANDROID_SDK_ROOT or install platform-tools.")
    result = run_command([executable, "devices"], timeout=15)
    if result.returncode != 0:
        raise RuntimeError(f"ADB devices failed: {result.stderr.strip() or result.stdout.strip()}")
    devices = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2:
            devices.append({"udid": parts[0], "state": parts[1]})
    return devices


def device_is_ready(udid: str, android_home: str | Path | None = None) -> bool:
    return any(item["udid"] == udid and item["state"] == "device" for item in connected_devices(android_home))


def boot_completed(udid: str, android_home: str | Path | None = None) -> bool:
    executable = adb_path(android_home)
    if not executable:
        raise FileNotFoundError("ADB was not found; cannot check Android boot completion.")
    result = run_command([executable, "-s", udid, "shell", "getprop", "sys.boot_completed"], timeout=15)
    return result.returncode == 0 and result.stdout.strip() == "1"


def device_metadata(udid: str, android_home: str | Path | None = None) -> dict[str, str]:
    executable = adb_path(android_home)
    if not executable:
        raise FileNotFoundError("ADB was not found; cannot read device metadata.")
    metadata: dict[str, str] = {}
    for key in ("ro.product.model", "ro.build.version.release", "ro.build.version.sdk"):
        result = run_command([executable, "-s", udid, "shell", "getprop", key], timeout=15)
        metadata[key] = result.stdout.strip()
    return metadata


def logcat_excerpt(udid: str, android_home: str | Path | None = None, lines: int = 200) -> str:
    """Return a bounded read-only Logcat excerpt for failure diagnostics."""

    executable = adb_path(android_home)
    if not executable:
        return "ADB was not found; Logcat was unavailable."
    result = run_command([executable, "-s", udid, "logcat", "-d", "-t", str(lines)], timeout=20)
    if result.returncode != 0:
        return f"ADB Logcat failed: {result.stderr.strip() or result.stdout.strip()}"
    return result.stdout[-100_000:]


def java_configuration() -> dict[str, str | bool]:
    java_home = os.environ.get("JAVA_HOME", "")
    java = shutil.which("java")
    return {"JAVA_HOME": java_home, "java_available": bool(java), "java_path": java or ""}


def sdk_configuration(android_home: str | Path | None = None) -> dict[str, str | bool]:
    value = str(android_home or os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or "")
    return {"ANDROID_HOME": value, "sdk_exists": bool(value and Path(value).is_dir())}


def appium_server_ready(url: str, timeout: int = 5) -> bool:
    endpoint = url.rstrip("/") + "/status"
    try:
        with urllib.request.urlopen(endpoint, timeout=timeout) as response:
            payload: Any = json.loads(response.read().decode("utf-8"))
        return response.status == 200 and isinstance(payload, dict)
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return False
