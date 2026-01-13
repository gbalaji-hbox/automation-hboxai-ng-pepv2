from behave import given, when, then

from features.pages.dashboard_page.dashboard_page import DashboardPage


@given(u'I am logged in as a valid user')
def step_impl(context):
    context.dashboard_page = DashboardPage(context.driver)
    context.dashboard_page.is_logged_in()


@when(u'I navigate to the {page_name} page')
def step_impl(context, page_name):
    context.dashboard_page.navigate_to_dashboard(page_name)


@then(u'I should see the dashboard header')
def step_impl(context):
    assert context.dashboard_page.verify_dashboard_header(), "Dashboard header is not visible"


@then(u'I should see the main navigation menu')
def step_impl(context):
    assert context.dashboard_page.verify_hamburger_menu(), "Hamburger Navigation menu is not visible"


@then(u'I should see the user profile section')
def step_impl(context):
    assert context.dashboard_page.verify_user_profile_section(), "User profile section is not visible"