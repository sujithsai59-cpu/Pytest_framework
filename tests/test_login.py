"""
Login test suite.

Covers the standard positive path plus the negative/edge cases that
SauceDemo's test accounts are specifically designed to exercise
(locked-out user, empty fields). Parametrizing the negative cases keeps
the suite readable and makes it trivial to add another bad-credentials
scenario later.
"""

import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils import config


@pytest.mark.smoke
def test_successful_login_shows_inventory_page(driver):
    login_page = LoginPage(driver).load()
    user = config.USERS["standard"]

    login_page.login(user["username"], user["password"])

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded(), "Inventory page did not load after valid login"
    assert "inventory" in inventory_page.get_current_url()


@pytest.mark.regression
def test_locked_out_user_sees_error(driver):
    login_page = LoginPage(driver).load()
    user = config.USERS["locked_out"]

    login_page.login(user["username"], user["password"])

    assert login_page.is_error_displayed()
    assert "locked out" in login_page.get_error_message().lower()


@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_message_fragment",
    [
        ("", "", "username is required"),
        ("standard_user", "", "password is required"),
        ("invalid_user", "wrong_password", "do not match"),
    ],
    ids=["empty_credentials", "missing_password", "invalid_credentials"],
)
def test_invalid_login_shows_expected_error(driver, username, password, expected_message_fragment):
    login_page = LoginPage(driver).load()

    login_page.login(username, password)

    assert login_page.is_error_displayed()
    assert expected_message_fragment in login_page.get_error_message().lower()
