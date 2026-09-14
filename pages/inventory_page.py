"""Page Object for the SauceDemo product listing (inventory) page."""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    INVENTORY_ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_NAME = (By.CSS_SELECTOR, ".inventory_item_name")
    ADD_TO_CART_BUTTON_TEMPLATE = "add-to-cart-{}"
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")
    CART_LINK = (By.CSS_SELECTOR, ".shopping_cart_link")
    SORT_DROPDOWN = (By.CSS_SELECTOR, ".product_sort_container")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")

    def is_loaded(self):
        return self.is_visible(self.PAGE_TITLE)

    def get_item_names(self):
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_item_prices(self):
        prices = self.find_all(self.ITEM_PRICES)
        return [float(p.text.replace("$", "")) for p in prices]

    def add_item_to_cart_by_slug(self, slug):
        """slug example: 'sauce-labs-backpack' -> button id add-to-cart-sauce-labs-backpack"""
        locator = (By.ID, self.ADD_TO_CART_BUTTON_TEMPLATE.format(slug))
        self.click(locator)

    def get_cart_count(self):
        if self.is_visible(self.CART_BADGE, timeout=2):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def sort_by(self, option_value):
        """option_value: one of 'az', 'za', 'lohi', 'hilo'"""
        from selenium.webdriver.support.ui import Select
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(option_value)
