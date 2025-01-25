from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class TaskViewPage(BasePage):
    # Locators
    TASK_NUMBER = (By.CLASS_NAME, "object_nr")
    TASK_TITLE = (By.CLASS_NAME, "content_label_title")
    TASK_STATUS = (By.CSS_SELECTOR, "span.statusIcon[title='Nowe']")

    def __init__(self):
        super().__init__()

    def get_task_number(self):
        """Get task number (e.g. TP-1)"""
        return self.helper.get_text(self.TASK_NUMBER)

    def get_task_title(self):
        """Get task title"""
        return self.helper.get_text(self.TASK_TITLE)

    def is_task_status_new(self):
        """Check if task has 'New' status"""
        return self.helper.is_element_visible(self.TASK_STATUS)
