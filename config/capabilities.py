"""Appium Android capability construction."""

from __future__ import annotations

from appium.options.android import UiAutomator2Options

from config.settings import Settings, settings


def build_android_options(config: Settings = settings) -> UiAutomator2Options:
    """Return options for a new Android UiAutomator2 session."""

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = config.android_udid
    options.device_name = config.device_name
    options.platform_version = config.platform_version
    options.app = str(config.app_path)
    options.app_wait_activity = (
        "com.saucelabs.mydemoapp.android.view.activities.MainActivity"
    )
    options.app_wait_duration = 30000
    options.new_command_timeout = config.command_timeout
    return options
