from behave import given, when, then

from features.pages.login_page.login_page import LoginPage
from features.pages.user_dashboard_page.user_dashboard_page import UserDashboardPage


@given(u'I am on User {page} page')
def step_impl(context, page):
    context.user_dashboard_page = UserDashboardPage(context.driver)
    context.user_dashboard_page.navigate_to_dashboard(page)
    context.user_dashboard_page.wait_for_dom_stability(timeout=2)


@when(u'I wait for patient details to load in the dashboard')
def step_impl(context):
    context.user_dashboard_page.wait_for_patient_details_to_load()


@when(u'I set enrollment status to "{status}"')
def step_impl(context, status):
    context.user_dashboard_page.set_enrollment_status(status)


@when(u'I set workflow status to "Call Answered"')
def step_impl(context):
    context.user_dashboard_page.set_workflow_status("Call Answered")


@when(u'I set appointment type to "{appointment_type}"')
def step_impl(context, appointment_type):
    context.user_dashboard_page.set_appointment_type(appointment_type)


@when(u'I select the first available resource')
def step_impl(context):
    login_page = LoginPage(context.driver)
    user_name, _ = login_page.get_credentials_for_role("vpe_internal")
    context.user_dashboard_page.set_first_available_resource(user_name)

@when(u'I select the first available facility')
def step_impl(context):
    context.user_dashboard_page.set_first_available_facility()


@when(u'I select the available appointment date and slot')
def step_impl(context):
    context.user_dashboard_page.set_available_appointment_date_and_slot()


@when(u'I enter a the comment for the engagement')
def step_impl(context):
    context.user_dashboard_page.set_comment_for_engagement()


@when(u'I save the patient enrollment')
def step_impl(context):
    context.user_dashboard_page.save_patient_enrollment()


@then(u'Patient engagement should be saved successfully')
def step_impl(context):
    assert context.user_dashboard_page.is_patient_enrollment_saved()


@when(u'I click on the Next Patient button')
def step_impl(context):
    context.user_dashboard_page.click_on_next_patient_button()


@then(u'I should see the next patient details in the dashboard')
def step_impl(context):
    assert context.user_dashboard_page.is_next_patient_loaded()