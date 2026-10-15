"""Functional catalog and product-details scenarios."""

import pytest

from pages.catalog_page import ProductsPage
from pages.product_page import ProductDetailsPage


@pytest.mark.functional
def test_opening_product_shows_matching_details(driver):
    catalog = ProductsPage(driver)
    catalog.wait_until_loaded()
    expected_title = catalog.get_visible_product_titles()[0]
    expected_price = catalog.get_visible_product_prices()[0]

    catalog.open_product(0)
    details = ProductDetailsPage(driver)
    details.wait_until_loaded()

    assert details.get_product_name() == expected_title, "Product details should show the selected product title."
    assert details.get_product_price() == expected_price, "Product details should show the selected product price."


@pytest.mark.functional
def test_name_ascending_sort_orders_visible_products(driver):
    catalog = ProductsPage(driver)
    catalog.wait_until_loaded()

    catalog.select_sort_option("name_ascending")
    actual_titles = catalog.get_visible_product_titles()

    assert actual_titles, "Sorting should leave visible products in the catalog."
    assert actual_titles == sorted(actual_titles, key=str.casefold), (
        "The Name - Ascending option should order visible product titles alphabetically."
    )
