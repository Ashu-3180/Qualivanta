"""Shared Appium fixture for functional Android tests."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from appium import webdriver

from config.capabilities import build_android_options
from config.settings import settings
from utilities.android_diagnostics import logcat_excerpt
from utilities.logger import get_logger
from utilities.screenshots import save_screenshot


LOGGER = get_logger("qualivanta.test_diagnostics")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def _safe_artifact_stem(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", nodeid).strip("._") or "test"


def _collect_failure_diagnostics(driver, request) -> None:
    """Best-effort failure evidence that never replaces the original failure."""

    report = getattr(request.node, "rep_call", None)
    if not report or not report.failed:
        return
    directory = Path("artifacts")
    stem = _safe_artifact_stem(request.node.nodeid)
    directory.mkdir(parents=True, exist_ok=True)
    try:
        screenshot = save_screenshot(driver, f"{stem}_failure", directory)
        LOGGER.error("Failure screenshot: %s", screenshot)
    except Exception as exc:  # pragma: no cover - exercised only during failure handling
        LOGGER.error("Could not capture failure screenshot: %s", exc)
    try:
        source_path = directory / f"{stem}_page_source.xml"
        source_path.write_text(driver.page_source, encoding="utf-8")
        LOGGER.error("Failure page source: %s", source_path)
    except Exception as exc:  # pragma: no cover - exercised only during failure handling
        LOGGER.error("Could not capture failure page source: %s", exc)
    try:
        log_path = directory / f"{stem}_logcat.txt"
        log_path.write_text(logcat_excerpt(settings.android_udid, settings.android_home), encoding="utf-8")
        LOGGER.error("Failure Logcat excerpt: %s", log_path)
    except Exception as exc:  # pragma: no cover - exercised only during failure handling
        LOGGER.error("Could not capture Logcat excerpt: %s", exc)
    try:
        error_path = directory / f"{stem}_error.txt"
        error_path.write_text(str(report.longrepr), encoding="utf-8")
        LOGGER.error("Failure context: %s", error_path)
    except Exception as exc:  # pragma: no cover - exercised only during failure handling
        LOGGER.error("Could not capture failure context: %s", exc)


@pytest.fixture
def driver(request):
    """Create one isolated Appium session for each test and always close it."""

    session = webdriver.Remote(settings.appium_server_url, options=build_android_options(settings))
    try:
        yield session
    finally:
        _collect_failure_diagnostics(session, request)
        session.quit()
