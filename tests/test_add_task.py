import os
from datetime import datetime, timedelta

import pytest

from pages.add_task_page import AddTaskPage
from pages.login_page import LoginPage
from pages.task_view_page import TaskViewPage


def test_add_task_happy_path():
    # Initialize page objects
    login_page = LoginPage()
    add_task_page = AddTaskPage()
    task_view_page = TaskViewPage()

    # Test data
    task_title = "Test Task"
    task_description = "This is a test task description"
    environment = "TP_Local"
    version = "TP_V0.01"
    due_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 23:59")

    # Login to the application
    login_page.navigate_to()
    login_page.perform_login(
        os.getenv("TEST_USER_EMAIL"), os.getenv("TEST_USER_PASSWORD")
    )

    # Navigate to add task page
    add_task_page.navigate_to_add_task()

    # Fill in task details
    add_task_page.enter_title(task_title)
    add_task_page.enter_description(task_description)
    add_task_page.select_environment(environment)
    add_task_page.select_version(version)
    add_task_page.assign_to_me()
    add_task_page.enter_due_date(due_date)
    add_task_page.click_save()

    # Verify task was added
    assert task_view_page.get_task_number().startswith(
        "TP-1"
    ), "Task number should start with 'TP-1'"
    assert (
        "Test Task" in task_view_page.get_task_title()
    ), "Task title should be 'Test Task'"
    assert task_view_page.is_task_status_new(), "Task status should be 'New'"
