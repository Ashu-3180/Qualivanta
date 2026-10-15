"""Functional shopping-cart scenarios."""

import pytest

from pages.cart_page import CartPage
from pages.catalog_page import ProductsPage
from pages.product_page import ProductDetailsPage


def _clear_cart(driver) -> None:
    """Return to a known empty cart using only verified UI actions."""

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


def _add_first_product(driver) -> tuple[ProductDetailsPage, str]:
    catalog = ProductsPage(driver)
    catalog.wait_until_loaded()
    catalog.open_product(0)
    details = ProductDetailsPage(driver)
    details.wait_until_loaded()
    title = details.get_product_name()
    details.add_to_cart()
    return details, title


@pytest.mark.functional
def test_added_product_appears_in_cart(driver):
    _clear_cart(driver)
    details, expected_title = _add_first_product(driver)
    details.open_cart()
    cart = CartPage(driver)
    cart.wait_until_loaded()

    try:
        assert expected_title in cart.get_item_titles(), "The selected product should appear in the cart."
    finally:
        cart.remove_all_items()


@pytest.mark.functional
def test_cart_quantity_reflects_one_added_product(driver):
    _clear_cart(driver)
    details, _ = _add_first_product(driver)
    details.open_cart()
    cart = CartPage(driver)
    cart.wait_until_loaded()

    try:
        assert cart.get_cart_quantity() == 1, "The cart quantity should be 1 after adding one product."
        assert cart.get_items_summary().startswith("1 "), "The cart summary should report one item."
    finally:
        cart.remove_all_items()
