"""
Base Page Object.

Every page class inherits from this. It centralizes waits and common
interactions so individual page objects stay thin and readable, and so
timeout/wait behavior is defined in exactly one place.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        self.driver = driver

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.DEFAULT_TIMEOUT)

    def find(self, locator, timeout=None):
        """Wait for a single element to be present and return it."""
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def find_all(self, locator, timeout=None):
        """Wait for at least one matching element and return the list."""
        return self._wait(timeout).until(EC.presence_of_all_elements_located(locator))

    def click(self, locator, timeout=None):
        """Wait until an element is clickable, then click it."""
        element = self._wait(timeout).until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator, text, timeout=None):
        """Clear a field and type into it."""
        element = self.find(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator, timeout=None):
        return self.find(locator, timeout).text

    def is_visible(self, locator, timeout=None):
        """Return True/False instead of raising, for assertions on absence."""
        try:
            self._wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_current_url(self):
        return self.driver.current_url

    def get_title(self):
        return self.driver.title
