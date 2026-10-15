"""Page Object Model for the verified Products catalog screen."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from utilities.waits import wait_for, wait_for_clickable, wait_for_visible


class ProductsPage:
    """Interactions and state queries for the Products page."""

    PRODUCTS_HEADING = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productTV")
    PRODUCT_LIST = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productRV")
    PRODUCT_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/titleTV")
    PRODUCT_PRICE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
    MENU = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/menuIV")
    SORT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/sortIV")
    CART = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartRL")
    CART_QUANTITY = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartTV")
    PRODUCT_IMAGE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productIV")
    SORT_OPTIONS = {
        "name_ascending": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameAscCL"),
        "name_descending": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameDesCL"),
        "price_ascending": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceAscCL"),
        "price_descending": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceDesCL"),
    }

    def __init__(self, driver, timeout: int = 20) -> None:
        self.driver = driver
        self.timeout = timeout

    def wait_until_loaded(self):
        """Wait for the page heading and catalog container to be visible."""

        wait_for_visible(self.driver, self.PRODUCTS_HEADING, self.timeout)
        return wait_for_visible(self.driver, self.PRODUCT_LIST, self.timeout)

    def is_products_heading_displayed(self) -> bool:
        """Return whether the Products heading is visible."""

        return wait_for_visible(self.driver, self.PRODUCTS_HEADING, self.timeout).is_displayed()

    def is_product_catalog_displayed(self) -> bool:
        """Return whether the product list container is visible."""

        return wait_for_visible(self.driver, self.PRODUCT_LIST, self.timeout).is_displayed()

    def get_visible_product_titles(self) -> list[str]:
        """Return non-empty titles currently exposed by the product list."""

        elements = wait_for(
            self.driver,
            lambda driver: driver.find_elements(*self.PRODUCT_TITLE) or False,
            self.timeout,
        )
        return [element.text.strip() for element in elements if element.text and element.text.strip()]

    def get_visible_product_prices(self) -> list[str]:
        """Return non-empty prices currently exposed by the product list."""

        elements = wait_for(
            self.driver,
            lambda driver: driver.find_elements(*self.PRODUCT_PRICE) or False,
            self.timeout,
        )
        return [element.text.strip() for element in elements if element.text and element.text.strip()]

    def get_cart_quantity(self) -> int:
        """Return the catalog cart badge quantity, or zero when no badge is exposed."""

        elements = self.driver.find_elements(*self.CART_QUANTITY)
        if not elements:
            return 0
        text = elements[0].text.strip()
        if not text.isdigit():
            raise AssertionError(f"Cart badge did not contain a numeric quantity; received {text!r}.")
        return int(text)

    def open_product(self, index: int = 0):
        """Open a visible product by zero-based catalog position."""

        products = wait_for(
            self.driver,
            lambda driver: driver.find_elements(*self.PRODUCT_IMAGE) or False,
            self.timeout,
        )
        if index < 0 or index >= len(products):
            raise IndexError(f"Product index {index} is outside the {len(products)} visible catalog products.")
        products[index].click()

    def select_sort_option(self, option: str) -> None:
        """Select one of the verified catalog sorting options."""

        try:
            locator = self.SORT_OPTIONS[option]
        except KeyError as exc:
            supported = ", ".join(sorted(self.SORT_OPTIONS))
            raise ValueError(f"Unsupported sort option {option!r}; supported options are: {supported}.") from exc
        self.open_sort_control()
        wait_for_clickable(self.driver, locator, self.timeout).click()
        wait_for_visible(self.driver, self.PRODUCT_LIST, self.timeout)

    def open_cart(self):
        """Open the cart from the Products page."""

        return wait_for_clickable(self.driver, self.CART, self.timeout).click()

    def open_menu(self):
        """Open the navigation menu from the Products page."""

        return wait_for_clickable(self.driver, self.MENU, self.timeout).click()

    def open_sort_control(self):
        """Open the catalog sorting control."""

        return wait_for_clickable(self.driver, self.SORT, self.timeout).click()
