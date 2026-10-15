"""Capture a generic initial-screen screenshot and page source."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from appium import webdriver

from config.capabilities import build_android_options
from config.settings import REPOSITORY_ROOT, load_settings
from scripts.download_demo_app import validate_apk
from utilities.android_diagnostics import appium_server_ready, boot_completed, device_is_ready
from utilities.screenshots import save_screenshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture a generic Appium UI snapshot for APK inspection.")
    parser.add_argument("--name", default="initial_screen", help="Descriptive output name (default: initial_screen).")
    parser.add_argument("--output-dir", type=Path, default=Path("docs/app_inspection"))
    args = parser.parse_args()
    driver = None
    try:
        config = load_settings()
        digest = validate_apk(config.app_path)
        if not device_is_ready(config.android_udid, config.android_home):
            raise RuntimeError(f"Configured device {config.android_udid} is not connected and ready.")
        if not boot_completed(config.android_udid, config.android_home):
            raise RuntimeError(f"Configured device {config.android_udid} has not completed Android boot.")
        if not appium_server_ready(config.appium_server_url):
            raise RuntimeError(f"Appium server is not reachable at {config.appium_server_url}.")
        print(f"Using APK SHA-256: {digest}")
        driver = webdriver.Remote(config.appium_server_url, options=build_android_options(config))
        output_dir = args.output_dir if args.output_dir.is_absolute() else REPOSITORY_ROOT / args.output_dir
        screenshot = save_screenshot(driver, args.name, output_dir)
        source_path = screenshot.with_suffix(".xml")
        source_path.write_text(driver.page_source, encoding="utf-8")
        print(f"Screenshot: {screenshot.resolve()}")
        print(f"Page source: {source_path.resolve()}")
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"UI snapshot failed: {exc}", file=sys.stderr)
        return 1
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    raise SystemExit(main())
