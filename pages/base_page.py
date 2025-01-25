import pytest

from utils.webdriver_helper import WebDriverHelper


class BasePage:
    def __init__(self):
        self.driver = pytest.driver
        self.config = pytest.config
        self.helper = WebDriverHelper(self.driver)

    def get_title(self):
        """Get page title"""
        return self.driver.title

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()

    def navigate_to(self, url=None):
        """Navigate to specific URL or base URL if none provided"""
        if url is None:
            url = self.config["base_url"]
        self.driver.get(url)
