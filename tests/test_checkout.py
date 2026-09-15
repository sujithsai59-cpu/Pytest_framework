"""
End-to-end checkout flow.

This is the highest-value test in the suite from a UAT perspective: it
walks the full user journey (login -> add to cart -> checkout -> confirm)
the way a real user or acceptance tester would, rather than testing
components in isolation.
"""

import pytest
import time
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage, CheckoutInfoPage, CheckoutOverviewPage, CheckoutCompletePage
from utils import config


@pytest.mark.smoke
@pytest.mark.e2e
def test_end_to_end_checkout_completes_successfully(driver):
    # 1. Log in
    login_page = LoginPage(driver).load()
    user = config.USERS["standard"]
    login_page.login(user["username"], user["password"])

    # 2. Add an item and go to cart
    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart_by_slug("sauce-labs-backpack")
    inventory_page.go_to_cart()

    cart_page = CartPage(driver)
    assert cart_page.get_cart_item_count() == 1
    cart_page.checkout()

    # 3. Fill in shipping info
    info_page = CheckoutInfoPage(driver)
    info_page.enter_first_name("Jane")
    time.sleep(0.5)
    info_page.enter_last_name("Doe")
    time.sleep(0.5)
    info_page.enter_zip_code("500001")
    time.sleep(0.5)
    info_page.continue_to_overview()
    # 4. Confirm order overview total is present and finish
    overview_page = CheckoutOverviewPage(driver)
    assert overview_page.get_item_total() > 0
    overview_page.finish()

    # 5. Verify confirmation
    complete_page = CheckoutCompletePage(driver)
    assert "thank you" in complete_page.get_confirmation_message().lower()


@pytest.mark.regression
def test_checkout_requires_first_name(driver):
    login_page = LoginPage(driver).load()
    user = config.USERS["standard"]
    login_page.login(user["username"], user["password"])

    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart_by_slug("sauce-labs-backpack")
    inventory_page.go_to_cart()

    
    CartPage(driver).checkout()

    info_page = CheckoutInfoPage(driver)
    info_page.enter_first_name("") 
    time.sleep(0.5) 
    info_page.enter_last_name("Doe")
    time.sleep(0.5)
    info_page.enter_zip_code("500001")
    time.sleep(0.5)
    info_page.continue_to_overview()
    assert info_page.is_error_displayed()
