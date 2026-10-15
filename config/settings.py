"""Runtime configuration for local and CI Android execution."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_APP_PATH = REPOSITORY_ROOT / "demo_app" / "mda-2.3.0-27.apk"
DEFAULT_ANDROID_HOME = Path(r"C:\Users\HP\AppData\Local\Android\Sdk")


def _env(name: str, default: str) -> str:
    value = os.environ.get(name)
    return value.strip() if value and value.strip() else default


def _resolve_repository_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else REPOSITORY_ROOT / path


@dataclass(frozen=True)
class Settings:
    """Validated values used to configure an Appium session."""

    appium_server_url: str
    app_path: Path
    android_udid: str
    platform_version: str
    android_home: Path
    device_name: str
    command_timeout: int


def load_settings(*, require_app: bool = True) -> Settings:
    """Read environment overrides and return validated runtime settings.

    Relative ``APP_PATH`` values are resolved from the repository root, making
    the configuration independent of the terminal's current directory.
    """

    app_path = _resolve_repository_path(os.environ.get("APP_PATH", str(DEFAULT_APP_PATH)))
    android_home_value = (
        os.environ.get("ANDROID_HOME")
        or os.environ.get("ANDROID_SDK_ROOT")
        or str(DEFAULT_ANDROID_HOME)
    )
    settings = Settings(
        appium_server_url=_env("APPIUM_SERVER_URL", "http://127.0.0.1:4723"),
        app_path=app_path,
        android_udid=_env("ANDROID_UDID", "emulator-5554"),
        platform_version=_env("APPIUM_PLATFORM_VERSION", "37"),
        android_home=Path(android_home_value).expanduser(),
        device_name=_env("ANDROID_DEVICE_NAME", _env("ANDROID_UDID", "emulator-5554")),
        command_timeout=int(_env("APPIUM_COMMAND_TIMEOUT", "120")),
    )
    validate_settings(settings, require_app=require_app)
    return settings


def validate_settings(settings: Settings, *, require_app: bool = True) -> None:
    """Raise actionable errors for invalid configuration or required paths."""

    if not settings.appium_server_url.startswith(("http://", "https://")):
        raise ValueError("APPIUM_SERVER_URL must be an http:// or https:// URL.")
    if not settings.android_udid:
        raise ValueError("ANDROID_UDID must identify a connected Android device.")
    if not settings.platform_version:
        raise ValueError("APPIUM_PLATFORM_VERSION must be set, for example 37 or 35.")
    if settings.command_timeout <= 0:
        raise ValueError("APPIUM_COMMAND_TIMEOUT must be a positive number of seconds.")
    if require_app and not settings.app_path.is_file():
        raise FileNotFoundError(
            f"Application APK was not found at {settings.app_path}. "
            "Set APP_PATH to the main demo APK; do not use the androidTest APK."
        )


settings = load_settings()
