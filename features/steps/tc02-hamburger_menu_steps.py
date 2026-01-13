from behave import given, when, then

from features.pages.dashboard_page.dashboard_page import DashboardPage
from features.pages.login_page.login_page import LoginPage


@given(u'I am on the {page_name} page')
def step_impl(context, page_name):
    context.dashboard_page = DashboardPage(context.driver)
    context.dashboard_page.navigate_to_dashboard(page_name)
    context.dashboard_page.wait_for_dom_stability(timeout=5)


@when(u'I extract all available hamburger menu options')
def step_impl(context):
    menu_options = context.dashboard_page.get_all_available_menu_options()
    context.extracted_menu_options = menu_options if menu_options else []
    assert len(context.extracted_menu_options) > 0, "Failed to extract hamburger menu options"


@then(u'I should verify each menu option navigates to the correct page')
def step_impl(context):
    return_option = context.dashboard_page.choose_return_option(context.extracted_menu_options)
    context.navigation_results = context.dashboard_page.verify_all_menu_navigation_with_options(
        context.extracted_menu_options,
        return_option,
    )
    context.dashboard_page.assert_navigation_results(context.navigation_results)


@then(u'I should verify all menu option links are functional')
def step_impl(context):
    context.dashboard_page.assert_links_functional(context.navigation_results)


@when(u'I click on "Logout" in the Hamburger Menu')
def step_impl(context):
    result = context.dashboard_page.click_logout_option()
    assert result, "Failed to click on 'Logout' in the hamburger menu"

@then(u'I should be logged out and navigated to the Login page')
def step_impl(context):
    login_page = LoginPage(context.driver)
    # Wait for navigation to complete
    context.dashboard_page.wait_for_dom_stability(timeout=3)
    
    # Check if we're logged out and on the login page
    is_logged_out = login_page.is_logged_out()
    assert is_logged_out, "User is not logged out - login button not visible"
    
    # Verify we're on the login page by checking URL or presence of login elements
    current_url = context.driver.current_url
    expected_login_url = login_page.url
    assert expected_login_url in current_url, f"Not on login page. Expected: {expected_login_url}, Current: {current_url}"

