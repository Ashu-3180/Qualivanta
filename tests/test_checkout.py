"""Functional checkout workflow and validation scenarios."""

import pytest

from pages.cart_page import CartPage
from pages.catalog_page import ProductsPage
from pages.checkout_page import CheckoutPage
from pages.product_page import ProductDetailsPage


SHIPPING = {
    "full_name": "Ada Lovelace",
    "address_1": "1 Analytical Engine Way",
    "city": "London",
    "zip_code": "NW1 1AA",
    "country": "United Kingdom",
}
PAYMENT = {
    "name": "Ada Lovelace",
    "card_number": "4111 1111 1111 1111",
    "expiration_date": "12/30",
    "security_code": "123",
}


def _clear_cart_if_populated(driver) -> None:
    catalog = ProductsPage(driver)
    catalog.wait_until_loaded()
    if catalog.get_cart_quantity() == 0:
        return
    catalog.open_cart()
    cart = CartPage(driver)
    cart.wait_until_loaded()
    cart.remove_all_items()
    driver.back()
    catalog.wait_until_loaded()


def _prepare_checkout(driver) -> tuple[CheckoutPage, str, str, CartPage]:
    _clear_cart_if_populated(driver)
    catalog = ProductsPage(driver)
    catalog.open_product(0)
    details = ProductDetailsPage(driver)
    details.wait_until_loaded()
    title, price = details.get_product_name(), details.get_product_price()
    details.add_to_cart()
    details.open_cart()
    cart = CartPage(driver)
    cart.wait_until_loaded()
    checkout = CheckoutPage(driver)
    checkout.start_from_cart(cart)
    return checkout, title, price, cart


def _cleanup_cart_from_checkout(driver) -> None:
    CheckoutPage(driver).open_cart()
    cart = CartPage(driver)
    cart.wait_until_loaded()
    cart.remove_all_items()


@pytest.mark.functional
def test_successful_end_to_end_checkout(driver):
    checkout, _, _, _ = _prepare_checkout(driver)
    checkout.enter_shipping_information(SHIPPING)
    checkout.submit_shipping_information()
    checkout.wait_for_payment()
    checkout.enter_payment_information(PAYMENT)
    checkout.submit_payment_information()
    checkout.wait_for_review()

    confirmation = checkout.place_order()

    assert confirmation.get_heading() == "Checkout Complete", "Successful checkout should show the observed completion heading."
    assert confirmation.get_message() == "Thank you for your order", "Successful checkout should show the observed thank-you message."
    confirmation.continue_shopping()
    ProductsPage(driver).wait_until_loaded()
    _clear_cart_if_populated(driver)


@pytest.mark.negative
def test_checkout_required_shipping_fields_show_validation(driver):
    checkout, _, _, _ = _prepare_checkout(driver)
    for field in SHIPPING:
        checkout.enter_shipping_information({field: ""})
    checkout.submit_shipping_information()

    messages = checkout.get_shipping_validation_messages()

    assert set(messages) == set(SHIPPING), "All observed required shipping fields should expose validation messages."
    assert all(message for message in messages.values()), "Required-field validation messages should not be empty."
    _cleanup_cart_from_checkout(driver)


@pytest.mark.functional
def test_checkout_back_navigation_preserves_cart_contents(driver):
    checkout, expected_title, _, _ = _prepare_checkout(driver)
    driver.back()
    cart = CartPage(driver)
    cart.wait_until_loaded()

    try:
        assert expected_title in cart.get_item_titles(), "Leaving checkout should preserve the selected cart product."
        assert cart.get_cart_quantity() == 1, "Leaving checkout should preserve the cart quantity."
    finally:
        cart.remove_all_items()


@pytest.mark.functional
def test_checkout_review_preserves_product_quantity_and_total(driver):
    checkout, expected_title, expected_price, _ = _prepare_checkout(driver)
    checkout.enter_shipping_information(SHIPPING)
    checkout.submit_shipping_information()
    checkout.wait_for_payment()
    checkout.enter_payment_information(PAYMENT)
    checkout.submit_payment_information()
    checkout.wait_for_review()

    try:
        assert expected_title in checkout.get_review_product_titles(), "Order review should retain the selected product."
        assert expected_price in checkout.get_review_product_prices(), "Order review should retain the selected product price."
        assert checkout.get_review_item_count().startswith("1 "), "Order review should report one selected item."
        assert checkout.get_review_total(), "Order review should expose a non-empty total."
    finally:
        _cleanup_cart_from_checkout(driver)
