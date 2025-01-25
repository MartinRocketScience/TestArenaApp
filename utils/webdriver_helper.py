import os

from dotenv import load_dotenv
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

load_dotenv()


class WebDriverHelper:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, int(os.getenv("EXPLICIT_WAIT", "20")))
        self.actions = ActionChains(driver)

    def find_element(self, locator):
        """Wait for element to be present and return it"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable_element(self, locator):
        """Wait for element to be clickable and return it"""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def is_element_visible(self, locator):
        """Check if element is visible"""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def click_element(self, locator):
        """Click on element when it's clickable"""
        element = self.find_clickable_element(locator)
        element.click()

    def input_text(self, locator, text):
        """Input text into element"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Get text from element"""
        element = self.find_element(locator)
        return element.text

    def select_by_text(self, locator, text):
        """Select option by visible text"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)

    def hover_and_click_offset(self, locator, x_offset=0, y_offset=0):
        """Move to element, then move by offset and click"""
        element = self.find_element(locator)
        self.actions.move_to_element(element).move_by_offset(
            x_offset, y_offset
        ).click().perform()
        return element
