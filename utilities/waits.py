"""Explicit wait helpers used by page objects."""

from __future__ import annotations

from typing import Any, Callable

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


def wait_for(driver: WebDriver, condition: Callable[[WebDriver], Any], timeout: int = 20) -> Any:
    """Wait until a Selenium condition returns a truthy value."""

    return WebDriverWait(driver, timeout).until(condition)


def wait_for_visible(driver: WebDriver, locator: tuple[str, str], timeout: int = 20) -> Any:
    """Wait until the element identified by ``locator`` is visible."""

    from selenium.webdriver.support import expected_conditions as expected

    return wait_for(driver, expected.visibility_of_element_located(locator), timeout)


def wait_for_clickable(driver: WebDriver, locator: tuple[str, str], timeout: int = 20) -> Any:
    """Wait until the element identified by ``locator`` can be clicked."""

    from selenium.webdriver.support import expected_conditions as expected

    return wait_for(driver, expected.element_to_be_clickable(locator), timeout)
