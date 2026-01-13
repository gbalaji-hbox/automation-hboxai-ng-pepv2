from time import sleep
from behave import given, when, then

from features.commons.routes import Routes
from features.pages.login_page.login_page import LoginPage
from utils.logger import printf
from utils.ui.config_reader import read_configuration

@given('I navigate to the Login page')
def navigate_to_login_page(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate_to_login()


@when('I enter valid email and password')
def enter_valid_credentials(context):
    email = read_configuration("Credentials", "enroller_admin_user_name")
    password = read_configuration("Credentials", f"common_{Routes.get_env()}_password")

    context.login_page.enter_email(email)
    context.login_page.enter_password(password)


@when('I click the Submit button')
def click_submit_button(context):
    context.login_page.click_submit()

@then('I should be logged in successfully')
def verify_successful_login(context):
    assert context.login_page.is_login_successful(), "Login was not successful"

@when('I enter invalid email and password')
def enter_invalid_credentials(context):
    invalid_email = "invalid@example.com"
    invalid_password = "wrong_password"
    context.login_page.enter_email(invalid_email)
    context.login_page.enter_password(invalid_password)


@then('I should see an error message')
def verify_error_message(context):
    assert context.login_page.is_error_message_displayed(), "Error message is not displayed"

@when(u'I enter invalid password')
def step_impl(context):
    email = read_configuration("Credentials", "enroller_admin_user_name")
    context.login_page.enter_email(email)
    context.login_page.enter_password("invalid_password")


@then(u'I should see a password error message')
def step_impl(context):
    assert context.login_page.is_password_error_displayed(), "Password error message is not displayed"

@when(u'I click on logout from dashboard header')
def step_impl(context):
    context.login_page.click_sign_out()
    sleep(5)
    printf("clicked logout")


@then(u'I should be logged out successfully')
def step_impl(context):
    assert context.login_page.is_logged_out(), "Logout was not successful"