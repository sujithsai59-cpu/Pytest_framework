"""Page Objects for the SauceDemo cart and checkout flow."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CSS_SELECTOR, ".cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def get_cart_item_count(self):
        return len(self.find_all(self.CART_ITEMS))

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)


class CheckoutInfoPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def fill_info(self, first_name, last_name, zip_code):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.ZIP_CODE_INPUT, zip_code)

    def continue_to_overview(self):
        self.click(self.CONTINUE_BUTTON)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_MESSAGE, timeout=3)


class CheckoutOverviewPage(BasePage):
    ITEM_TOTAL = (By.CSS_SELECTOR, ".summary_subtotal_label")
    FINISH_BUTTON = (By.ID, "finish")

    def get_item_total(self):
        text = self.get_text(self.ITEM_TOTAL)  # "Item total: $29.99"
        return float(text.split("$")[1])

    def finish(self):
        self.click(self.FINISH_BUTTON)


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = (By.CSS_SELECTOR, ".complete-header")

    def get_confirmation_message(self):
        return self.get_text(self.COMPLETE_HEADER)
