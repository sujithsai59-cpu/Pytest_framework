"""Product listing (inventory) test suite: sorting, add-to-cart, cart badge."""

import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils import config


@pytest.fixture
def logged_in_inventory_page(driver):
    """Reusable precondition: most inventory tests need a logged-in session."""
    login_page = LoginPage(driver).load()
    user = config.USERS["standard"]
    login_page.login(user["username"], user["password"])
    return InventoryPage(driver)


@pytest.mark.smoke
def test_add_single_item_to_cart_updates_badge(logged_in_inventory_page):
    page = logged_in_inventory_page

    page.add_item_to_cart_by_slug("sauce-labs-backpack")

    assert page.get_cart_count() == 1


@pytest.mark.regression
def test_add_multiple_items_updates_badge_correctly(logged_in_inventory_page):
    page = logged_in_inventory_page

    page.add_item_to_cart_by_slug("sauce-labs-backpack")
    page.add_item_to_cart_by_slug("sauce-labs-bike-light")
    page.add_item_to_cart_by_slug("sauce-labs-bolt-t-shirt")

    assert page.get_cart_count() == 3


@pytest.mark.regression
@pytest.mark.parametrize(
    "sort_option, check",
    [
        ("lohi", lambda prices: prices == sorted(prices)),
        ("hilo", lambda prices: prices == sorted(prices, reverse=True)),
    ],
    ids=["price_low_to_high", "price_high_to_low"],
)
def test_sort_by_price(logged_in_inventory_page, sort_option, check):
    page = logged_in_inventory_page

    page.sort_by(sort_option)
    prices = page.get_item_prices()

    assert check(prices), f"Items were not sorted correctly for option '{sort_option}': {prices}"


@pytest.mark.regression
def test_sort_by_name_a_to_z(logged_in_inventory_page):
    page = logged_in_inventory_page

    page.sort_by("az")
    names = page.get_item_names()

    assert names == sorted(names)
