from behave import when, then

from features.pages.activities_page.activities_page import ActivitiesPage


@when(u'I fetch the first row data from the activities table')
def step_impl(context):
    context.activities_page = ActivitiesPage(context.driver)
    context.first_row_activities_data = context.activities_page.get_activities_first_row_data()


@when(u'I enter the "{field}" value in activities search box')
def step_impl(context, field):
    if not hasattr(context, 'first_row_activities_data') or not context.first_row_activities_data:
        context.first_row_activities_data = context.activities_page.get_activities_first_row_data()

    context.search_criteria = field
    context.search_value = context.first_row_activities_data.get(field)
    result = context.activities_page.perform_activities_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the activities search results should match in activities table')
def step_impl(context):
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.activities_page.verify_activities_search_results(
        context.search_criteria,
        context.search_value,
    ), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"


@when(u'I click on "{action_button}" button in activities table first row')
def step_impl(context, action_button):
    context.activities_page = ActivitiesPage(context.driver)
    context.activities_page.navigate_to_listing()
    context.activities_page.click_on_activities_action_button(action_button)


@then(u'"Activity Operation History dialog opens" should happen')
def step_impl(context):
    assert context.activities_page.verify_activities_operation_history_dialog(), \
        "Activity Operation History dialog did not open as expected."


@then(u'"Edit activity page loads" should happen')
def step_impl(context):
    assert context.activities_page.is_navigated_to_activity_edit_page(), \
        "Edit activity page did not load as expected."


@then(u'"Activity creation page loads with pre-filled data" should happen')
def step_impl(context):
    assert context.activities_page.verify_activity_duplicate_prefilled(), \
        "Activity duplicate page did not load with pre-filled data as expected."


@then(u'"Activity delete confirmation dialog appears" should happen')
def step_impl(context):
    assert context.activities_page.verify_activity_delete_confirmation_dialog(), \
        "Activity delete confirmation dialog did not appear as expected."


@when(u'I select {records} records per page for activities table')
def step_impl(context, records):
    context.activities_page = ActivitiesPage(context.driver)
    context.activities_page.navigate_to_listing()
    context.activities_page.select_activity_records_per_page(records)


@then(u'the activities table should display exactly {records} records per page')
def step_impl(context, records):
    assert context.activities_page.verify_activity_records_per_page(records), \
        f"Activities table did not display exactly {records} records per page."