"""Page Object Model for the verified product-details screen."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.catalog_page import ProductsPage
from utilities.waits import wait_for_clickable, wait_for_visible


class ProductDetailsPage:
    """Interactions with the selected product details."""

    PRODUCT_NAME = ProductsPage.PRODUCTS_HEADING
    PRODUCT_PRICE = ProductsPage.PRODUCT_PRICE
    PRODUCT_IMAGE = ProductsPage.PRODUCT_IMAGE
    CART = ProductsPage.CART
    ADD_TO_CART = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartBt")

    def __init__(self, driver, timeout: int = 20) -> None:
        self.driver = driver
        self.timeout = timeout

    def wait_until_loaded(self):
        """Wait for the selected product and its Add to cart action."""

        wait_for_visible(self.driver, self.PRODUCT_NAME, self.timeout)
        return wait_for_visible(self.driver, self.ADD_TO_CART, self.timeout)

    def get_product_name(self) -> str:
        return wait_for_visible(self.driver, self.PRODUCT_NAME, self.timeout).text.strip()

    def get_product_price(self) -> str:
        return wait_for_visible(self.driver, self.PRODUCT_PRICE, self.timeout).text.strip()

    def add_to_cart(self) -> None:
        wait_for_clickable(self.driver, self.ADD_TO_CART, self.timeout).click()

    def open_cart(self) -> None:
        wait_for_clickable(self.driver, self.CART, self.timeout).click()
