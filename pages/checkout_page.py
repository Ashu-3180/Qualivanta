"""Page Object Model for the verified checkout workflow."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy

from pages.cart_page import CartPage
from utilities.waits import wait_for, wait_for_clickable, wait_for_visible


class CheckoutPage:
    """Shipping, payment, and order-review interactions."""

    CHECKOUT_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/checkoutTitleTV")
    SHIPPING_SECTION = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/enterShippingAddressTV")
    FULL_NAME = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/fullNameET")
    ADDRESS_1 = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address1ET")
    ADDRESS_2 = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address2ET")
    CITY = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityET")
    ZIP_CODE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/zipET")
    STATE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/stateET")
    COUNTRY = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryET")
    ACTION_BUTTON = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/paymentBtn")
    CART = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartRL")

    LOGIN_BUTTON = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/loginBtn")
    SAVED_USERNAME = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/username1TV")

    PAYMENT_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/enterPaymentTitleTV")
    PAYMENT_NAME = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameET")
    CARD_NUMBER = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cardNumberET")
    EXPIRATION_DATE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/expirationDateET")
    SECURITY_CODE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/securityCodeET")
    REVIEW_LIST = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/placeOrderRV")
    REVIEW_ITEM_COUNT = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/itemNumberTV")
    REVIEW_TOTAL = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/totalAmountTV")
    REVIEW_PRODUCT_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/titleTV")
    REVIEW_PRODUCT_PRICE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")

    SHIPPING_ERRORS = {
        "full_name": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/fullNameErrorTV"),
        "address_1": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/address1ErrorTV"),
        "city": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cityErrorTV"),
        "zip_code": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/zipErrorTV"),
        "country": (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/countryErrorTV"),
    }

    def __init__(self, driver, timeout: int = 20) -> None:
        self.driver = driver
        self.timeout = timeout

    def start_from_cart(self, cart: CartPage) -> None:
        """Proceed from cart and complete the app's verified login gate."""

        cart.proceed_to_checkout()
        next_screen = wait_for(
            self.driver,
            lambda driver: driver.find_elements(*self.LOGIN_BUTTON)
            or driver.find_elements(*self.CHECKOUT_TITLE)
            or False,
            self.timeout,
        )
        if next_screen[0].get_attribute("resourceId") == self.LOGIN_BUTTON[1]:
            wait_for_clickable(self.driver, self.SAVED_USERNAME, self.timeout).click()
            wait_for_clickable(self.driver, self.LOGIN_BUTTON, self.timeout).click()
        self.wait_for_shipping()

    def wait_for_shipping(self):
        return wait_for_visible(self.driver, self.SHIPPING_SECTION, self.timeout)

    def open_cart(self) -> None:
        """Return to the cart through the verified checkout header action."""

        wait_for_clickable(self.driver, self.CART, self.timeout).click()

    def _fill(self, locator: tuple[str, str], value: str) -> None:
        field = wait_for_visible(self.driver, locator, self.timeout)
        field.clear()
        field.send_keys(value)

    def enter_shipping_information(self, information: dict[str, str]) -> None:
        """Fill supported shipping fields; omitted optional fields are unchanged."""

        fields = {
            "full_name": self.FULL_NAME,
            "address_1": self.ADDRESS_1,
            "address_2": self.ADDRESS_2,
            "city": self.CITY,
            "zip_code": self.ZIP_CODE,
            "state": self.STATE,
            "country": self.COUNTRY,
        }
        for name, value in information.items():
            if name not in fields:
                raise ValueError(f"Unsupported shipping field {name!r}.")
            self._fill(fields[name], value)

    def submit_shipping_information(self) -> None:
        wait_for_clickable(self.driver, self.ACTION_BUTTON, self.timeout).click()

    def get_shipping_validation_messages(self) -> dict[str, str]:
        """Return the non-empty validation messages currently exposed."""

        messages: dict[str, str] = {}
        for name, locator in self.SHIPPING_ERRORS.items():
            elements = self.driver.find_elements(*locator)
            if elements and elements[0].text.strip():
                messages[name] = elements[0].text.strip()
        return messages

    def wait_for_payment(self):
        return wait_for_visible(self.driver, self.PAYMENT_TITLE, self.timeout)

    def enter_payment_information(self, information: dict[str, str]) -> None:
        fields = {
            "name": self.PAYMENT_NAME,
            "card_number": self.CARD_NUMBER,
            "expiration_date": self.EXPIRATION_DATE,
            "security_code": self.SECURITY_CODE,
        }
        for name, value in information.items():
            if name not in fields:
                raise ValueError(f"Unsupported payment field {name!r}.")
            self._fill(fields[name], value)

    def submit_payment_information(self) -> None:
        wait_for_clickable(self.driver, self.ACTION_BUTTON, self.timeout).click()

    def wait_for_review(self):
        return wait_for_visible(self.driver, self.REVIEW_LIST, self.timeout)

    def get_review_product_titles(self) -> list[str]:
        elements = wait_for(self.driver, lambda driver: driver.find_elements(*self.REVIEW_PRODUCT_TITLE) or False, self.timeout)
        return [element.text.strip() for element in elements if element.text and element.text.strip()]

    def get_review_product_prices(self) -> list[str]:
        elements = wait_for(self.driver, lambda driver: driver.find_elements(*self.REVIEW_PRODUCT_PRICE) or False, self.timeout)
        return [element.text.strip() for element in elements if element.text and element.text.strip()]

    def get_review_item_count(self) -> str:
        return wait_for_visible(self.driver, self.REVIEW_ITEM_COUNT, self.timeout).text.strip()

    def get_review_total(self) -> str:
        return wait_for_visible(self.driver, self.REVIEW_TOTAL, self.timeout).text.strip()

    def place_order(self):
        from pages.order_confirmation_page import OrderConfirmationPage

        wait_for_clickable(self.driver, self.ACTION_BUTTON, self.timeout).click()
        confirmation = OrderConfirmationPage(self.driver, self.timeout)
        confirmation.wait_until_loaded()
        return confirmation
