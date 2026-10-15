"""Page Object Model for the verified checkout confirmation screen."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from utilities.waits import wait_for_clickable, wait_for_visible


class OrderConfirmationPage:
    COMPLETE_HEADING = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/completeTV")
    THANK_YOU_MESSAGE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/thankYouTV")
    CONTINUE_SHOPPING = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/shoopingBt")

    def __init__(self, driver, timeout: int = 20) -> None:
        self.driver = driver
        self.timeout = timeout

    def wait_until_loaded(self):
        wait_for_visible(self.driver, self.COMPLETE_HEADING, self.timeout)
        return wait_for_visible(self.driver, self.THANK_YOU_MESSAGE, self.timeout)

    def get_heading(self) -> str:
        return wait_for_visible(self.driver, self.COMPLETE_HEADING, self.timeout).text.strip()

    def get_message(self) -> str:
        return wait_for_visible(self.driver, self.THANK_YOU_MESSAGE, self.timeout).text.strip()

    def continue_shopping(self) -> None:
        wait_for_clickable(self.driver, self.CONTINUE_SHOPPING, self.timeout).click()
