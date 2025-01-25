from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login")
    EMAIL_ERROR_MESSAGE = (
        By.XPATH,
        "//input[@id='email']/following-sibling::div[@class='login_form_error']",
    )
    PASSWORD_ERROR_MESSAGE = (
        By.XPATH,
        "//input[@id='password']/following-sibling::div[@class='login_form_error']",
    )

    def __init__(self):
        super().__init__()

    def enter_email(self, email):
        """Enter email into email input field"""
        self.helper.input_text(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password):
        """Enter password into password input field"""
        self.helper.input_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Click login button"""
        self.helper.click_element(self.LOGIN_BUTTON)
        return self

    def perform_login(self, email, password):
        """Perform full login action"""
        return self.enter_email(email).enter_password(password).click_login()

    def get_email_error_message(self):
        """Get error message if login fails"""
        return self.helper.get_text(self.EMAIL_ERROR_MESSAGE)

    def get_password_error_message(self):
        """Get error message if login fails"""
        return self.helper.get_text(self.PASSWORD_ERROR_MESSAGE)
