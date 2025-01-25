from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DashboardPage(BasePage):
    # Locators
    USER_INFO = (By.CLASS_NAME, "user-info")

    def __init__(self):
        super().__init__()

    def is_user_info_element_visible(self):
        """Check if user info element is visible (indicates successful login)"""
        return self.helper.is_element_visible(self.USER_INFO)
