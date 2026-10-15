"""Page Object Model for the verified shopping-cart screen."""

from __future__ import annotations

import re

from appium.webdriver.common.appiumby import AppiumBy

from pages.catalog_page import ProductsPage
from utilities.waits import wait_for, wait_for_clickable, wait_for_visible


class CartPage:
    """Interactions and state queries for My Cart."""

    CART_HEADING = ProductsPage.PRODUCTS_HEADING
    CART_ITEM_LIST = ProductsPage.PRODUCT_LIST
    CART_ITEM_TITLE = ProductsPage.PRODUCT_TITLE
    CART_ITEM_PRICE = ProductsPage.PRODUCT_PRICE
    CART_QUANTITY = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")
    CART_ITEMS_SUMMARY = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/itemsTV")
    CART_TOTAL = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalPriceTV")
    REMOVE_ITEM = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/removeBt")
    PROCEED_TO_CHECKOUT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartBt")

    def __init__(self, driver, timeout: int = 20) -> None:
        self.driver = driver
        self.timeout = timeout

    def wait_until_loaded(self):
        return wait_for_visible(self.driver, self.CART_HEADING, self.timeout)

    def get_item_titles(self) -> list[str]:
        elements = self.driver.find_elements(*self.CART_ITEM_TITLE)
        return [element.text.strip() for element in elements if element.text and element.text.strip()]

    def has_items(self) -> bool:
        return bool(self.driver.find_elements(*self.CART_ITEM_TITLE))

    def get_cart_quantity(self) -> int:
        text = wait_for_visible(self.driver, self.CART_QUANTITY, self.timeout).text.strip()
        match = re.search(r"\d+", text)
        if not match:
            raise AssertionError(f"Cart quantity did not contain a number; received {text!r}.")
        return int(match.group())

    def get_items_summary(self) -> str:
        return wait_for_visible(self.driver, self.CART_ITEMS_SUMMARY, self.timeout).text.strip()

    def get_total(self) -> str:
        return wait_for_visible(self.driver, self.CART_TOTAL, self.timeout).text.strip()

    def proceed_to_checkout(self) -> None:
        """Start checkout from a populated cart."""

        wait_for_clickable(self.driver, self.PROCEED_TO_CHECKOUT, self.timeout).click()

    def remove_all_items(self) -> None:
        """Remove every currently listed item using the verified cart action."""

        while self.has_items():
            wait_for_clickable(self.driver, self.REMOVE_ITEM, self.timeout).click()
            wait_for(self.driver, lambda driver: not driver.find_elements(*self.CART_ITEM_TITLE), self.timeout)
