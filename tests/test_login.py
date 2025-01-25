import os

import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


def test_login_with_valid_credentials():
    login_page = LoginPage()
    dashboard_page = DashboardPage()

    login_page.navigate_to()

    (
        login_page.enter_email(os.getenv("TEST_USER_EMAIL"))
        .enter_password(os.getenv("TEST_USER_PASSWORD"))
        .click_login()
    )

    assert dashboard_page.is_user_info_element_visible(), "User should be logged in"


def test_login_with_empty_credentials():
    login_page = LoginPage()
    login_page.navigate_to()

    login_page.click_login()

    assert login_page.get_email_error_message() == "Pole wymagane"
    assert login_page.get_password_error_message() == "Pole wymagane"


@pytest.mark.parametrize(
    "email, password, error",
    [
        (
            "invalid_email@example.com",
            "wrongpassword",
            "Adres e-mail i/lub hasło są niepoprawne.",
        ),
        (
            os.getenv("TEST_USER_EMAIL"),
            "wrongpassword",
            "Adres e-mail i/lub hasło są niepoprawne.",
        ),
    ],
)
def test_login_with_invalid_credentials(email, password, error):
    login_page = LoginPage()
    login_page.navigate_to()

    (login_page.enter_email(email).enter_password(password).click_login())

    assert login_page.get_password_error_message() == error


@pytest.mark.parametrize("email", ["wrong_email_format", "email@email"])
def test_login_with_invalid_email_format(email):
    login_page = LoginPage()
    login_page.navigate_to()

    (
        login_page.enter_email(email)
        .enter_password(os.getenv("TEST_USER_PASSWORD"))
        .click_login()
    )

    assert (
        login_page.get_email_error_message()
        == "Nieprawidłowy format adresu e-mail. Wprowadź adres ponownie."
    )
