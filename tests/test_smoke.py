"""Smoke coverage for the verified Products catalog screen."""

import pytest

from pages.catalog_page import ProductsPage


@pytest.mark.smoke
def test_products_heading_is_displayed(driver):
    products = ProductsPage(driver)

    assert products.is_products_heading_displayed(), "The Products heading should be visible after app launch."


@pytest.mark.smoke
def test_product_catalog_is_present(driver):
    products = ProductsPage(driver)

    assert products.is_product_catalog_displayed(), "The product catalog container should be visible after app launch."


@pytest.mark.smoke
def test_product_titles_and_prices_can_be_retrieved(driver):
    products = ProductsPage(driver)
    products.wait_until_loaded()

    titles = products.get_visible_product_titles()
    prices = products.get_visible_product_prices()

    assert titles, "At least one visible product title should be retrievable from the catalog."
    assert prices, "At least one visible product price should be retrievable from the catalog."


@pytest.mark.smoke
def test_product_catalog_contains_valid_title_and_price(driver):
    products = ProductsPage(driver)
    products.wait_until_loaded()

    titles = products.get_visible_product_titles()
    prices = products.get_visible_product_prices()

    assert any(title.strip() for title in titles), "The catalog should contain at least one non-empty product title."
    assert any(price.strip() for price in prices), "The catalog should contain at least one non-empty product price."
