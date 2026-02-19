from behave import given, when, then

from features.pages.scheduled_appointments_page.scheduled_appointments_page import ScheduledAppointmentsPage


@given(u'I am on the "{tab_name}" tab')
def step_impl(context, tab_name):
    context.scheduled_appointments_page = ScheduledAppointmentsPage(context.driver)
    context.scheduled_appointments_page.click_on_tab(tab_name)


@when(u'I click on the "{tab_name}" tab')
def step_impl(context, tab_name):
    context.scheduled_appointments_page = ScheduledAppointmentsPage(context.driver)
    if not hasattr(context, 'scheduled_appointments_page'):
        context.scheduled_appointments_page = ScheduledAppointmentsPage(context.driver)
    context.scheduled_appointments_page.click_on_tab(tab_name)


@then(u'the "{tab_name}" tab should be active')
def step_impl(context, tab_name):
    context.scheduled_appointments_page = ScheduledAppointmentsPage(context.driver)
    assert context.scheduled_appointments_page.is_tab_active(tab_name), \
        f"Tab '{tab_name}' is not active."


@then(u'the scheduled appointments table should display records')
def step_impl(context):
    assert context.scheduled_appointments_page.is_table_displayed(), \
        "Scheduled appointments table is not displayed or has no records."


@when(u'I fetch the first row data from the scheduled appointments table')
def step_impl(context):
    context.scheduled_appointments_page.navigate_to_listing()
    context.first_row_data = context.scheduled_appointments_page.get_first_row_data()


@when(u'I search by "{field}" with the fetched value in scheduled appointments')
def step_impl(context, field):
    if not hasattr(context, 'first_row_data') or not context.first_row_data:
        context.first_row_data = context.scheduled_appointments_page.get_first_row_data()

    context.search_criteria = field
    context.search_value = context.first_row_data.get(field)

    result = context.scheduled_appointments_page.perform_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the scheduled appointments search results should match in the table')
def step_impl(context):
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.scheduled_appointments_page.verify_search_results(
        context.search_criteria, context.search_value
    ), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"


@when(u'I click on the patient name button in the first row')
def step_impl(context):
    if not hasattr(context, 'scheduled_appointments_page'):
        context.scheduled_appointments_page = ScheduledAppointmentsPage(context.driver)
    context.scheduled_appointments_page.navigate_to_listing()
    context.scheduled_appointments_page.click_patient_name_button()


@then(u'I should be navigated to the patient details page')
def step_impl(context):
    if not hasattr(context, 'scheduled_appointments_page'):
        context.scheduled_appointments_page = ScheduledAppointmentsPage(context.driver)
    assert context.scheduled_appointments_page.is_navigated_to_patient_details(), \
        "Did not navigate to patient details page."


@when(u'I select {records} records per page for scheduled appointments table')
def step_impl(context, records):
    context.scheduled_appointments_page.navigate_to_listing()
    context.scheduled_appointments_page.select_records_per_page(records)


@then(u'the scheduled appointments table should display exactly {records} records per page')
def step_impl(context, records):
    if not hasattr(context, 'scheduled_appointments_page'):
        context.scheduled_appointments_page = ScheduledAppointmentsPage(context.driver)
    assert context.scheduled_appointments_page.verify_records_per_page(int(records)), \
        f"Scheduled appointments table did not display exactly {records} records per page."