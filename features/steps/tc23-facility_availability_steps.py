from behave import given, when, then

from features.pages.facility_availability_page.facility_availability_page import FacilityAvailabilityPage


@when(u'I fetch the first row data from the facility availability table')
def step_impl(context):
    context.facility_availability_page = FacilityAvailabilityPage(context.driver)
    context.facility_availability_page.navigate_to_listing()
    context.first_row_facility_availability_data = context.facility_availability_page.get_facility_availability_first_row_data()


@when(u'I select {field} option and enter the fetched data in facility availability search box')
def step_impl(context, field):
    if not hasattr(context, 'first_row_facility_availability_data') or not context.first_row_facility_availability_data:
        context.first_row_facility_availability_data = context.facility_availability_page.get_facility_availability_first_row_data()

    context.search_criteria = field
    context.search_value = context.first_row_facility_availability_data.get(field)
    result = context.facility_availability_page.perform_facility_availability_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the facility availability search results should match in facility availability table')
def step_impl(context):
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.facility_availability_page.verify_facility_availability_search_results(
        context.search_criteria,
        context.search_value,
    ), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"


@when(u'I click on "{action_button}" button in facility availability table first row')
def step_impl(context, action_button):
    context.facility_availability_page = FacilityAvailabilityPage(context.driver)
    context.facility_availability_page.navigate_to_listing()
    context.facility_availability_page.click_on_facility_availability_action_button(action_button)


@then(u'"Facility Availability Operation History dialog opens" should happen')
def step_impl(context):
    assert context.facility_availability_page.verify_facility_availability_operation_history_dialog(), \
        "Facility Availability Operation History dialog did not open as expected."


@then(u'"Edit facility availability page loads" should happen')
def step_impl(context):
    assert context.facility_availability_page.is_navigated_to_facility_availability_edit_page(), \
        "Edit facility availability page did not load as expected."


@then(u'"Facility availability delete confirmation dialog appears" should happen')
def step_impl(context):
    assert context.facility_availability_page.verify_facility_availability_delete_confirmation_dialog(), \
        "Facility availability delete confirmation dialog did not appear as expected."


@when(u'I select {records} records per page for facility availability table')
def step_impl(context, records):
    context.facility_availability_page = FacilityAvailabilityPage(context.driver)
    context.facility_availability_page.navigate_to_listing()
    context.facility_availability_page.select_facility_availability_records_per_page(records)


@then(u'the facility availability table should display exactly {records} records per page')
def step_impl(context, records):
    assert context.facility_availability_page.verify_facility_availability_records_per_page(records), \
        f"Facility availability table did not display exactly {records} records per page."
