import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize(
    "email,password,error",
    [
        ("abcemail@gmail.com", "wrongpassword", "Incorrect email address or password"),
        ("", "", "Email address is required"),
        ("laharimaredi0103@gmail.com", "", "Password is required"),
    ]
)
def test_invalid_login(driver, email, password, error):

    login = LoginPage(driver)

    login.open("https://practice.expandtesting.com/notes/app")
    login.login(email, password)

    error_msg = login.get_error_message(error)

    assert error_msg.is_displayed()
