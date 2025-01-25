from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AddTaskPage(BasePage):
    # PATH
    PATH = "/TP/task_add"

    def __init__(self):
        super().__init__()

    # Locators
    TITLE_INPUT = (By.ID, "title")
    DESCRIPTION_INPUT = (By.ID, "description")
    ENVIRONMENT_INPUT = (By.ID, "token-input-environments")
    VERSION_SELECT = (By.ID, "token-input-versions")
    ASSIGN_TO_ME_CHECKBOX = (By.ID, "j_assignToMe")
    DUE_DATE_INPUT = (By.ID, "dueDate")
    SAVE_BUTTON = (By.ID, "save")

    def navigate_to_add_task(self):
        """Navigate to add task page"""
        self.navigate_to(f"{self.config['base_url']}{self.PATH}")

    def enter_title(self, title):
        """Enter task title"""
        self.helper.input_text(self.TITLE_INPUT, title)

    def enter_description(self, description):
        """Enter task description"""
        self.helper.input_text(self.DESCRIPTION_INPUT, description)

    def select_environment(self, environment):
        """Select environment from dropdown"""
        env_input = self.helper.find_element(self.ENVIRONMENT_INPUT)
        env_input.send_keys(environment)
        self.helper.hover_and_click_offset(
            self.ENVIRONMENT_INPUT, x_offset=0, y_offset=20
        )

    def select_version(self, version):
        """Select version from dropdown"""
        version_input = self.helper.find_element(self.VERSION_SELECT)
        version_input.send_keys(version)
        self.helper.hover_and_click_offset(self.VERSION_SELECT, x_offset=0, y_offset=20)

    def assign_to_me(self):
        """Click assign to me checkbox"""
        self.helper.click_element(self.ASSIGN_TO_ME_CHECKBOX)

    def enter_due_date(self, due_date):
        """Enter due date"""
        self.helper.input_text(self.DUE_DATE_INPUT, due_date)

    def click_save(self):
        """Click save button"""
        self.helper.click_element(self.SAVE_BUTTON)
