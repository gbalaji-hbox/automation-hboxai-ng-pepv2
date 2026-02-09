from behave import when, then, given

from features.pages.patient_groups_page.patient_groups_page import PatientGroupsPage
from utils.logger import printf


@when(u'I fetch the first row data from the patient groups table')
def step_impl(context):
    context.patient_groups_page = PatientGroupsPage(context.driver)
    context.first_row_data = context.patient_groups_page.get_first_row_data()


@when(u'I enter that value in the group search field and search')
def step_impl(context):
    if not hasattr(context, 'first_row_data') or not context.first_row_data:
        context.first_row_data = context.patient_groups_page.get_first_row_data()

    context.search_criteria = field = "Group Name"
    if field == 'Group Name':
        data_field = 'Group Name'
    else:
        data_field = field

    context.search_value = context.first_row_data.get(data_field)

    result = context.patient_groups_page.perform_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the Patient Groups table should show the results matching the search criteria')
def step_impl(context):
    printf(f"verifying search results for patient groups table")
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.patient_groups_page.verify_search_results(
        context.search_criteria,
        context.search_value), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"


@when(u'I click on "{action_button}" button for a Patient Group in the table')
def step_impl(context, action_button):
    context.patient_groups_page = PatientGroupsPage(context.driver)
    result = context.patient_groups_page.click_action_button(action_button)
    if not result:
        raise AssertionError(f"Failed to click {action_button} button")


@then(u'"Patient Group Operation History dialog opens" should happen')
def step_impl(context):
    assert context.patient_groups_page.verify_history_dialog_opens(), "History dialog did not open"


@then(u'"Edit Patient Group page loads" should happen')
def step_impl(context):
    assert context.patient_groups_page.is_navigated_to_edit_page(), "Edit Patient Group page did not load"


@then(u'"delete Patient Group confirmation dialog appears" should happen')
def step_impl(context):
    assert context.patient_groups_page.verify_delete_dialog_opens(), "Delete confirmation dialog did not appear"


@then(u'"archive Patient Group confirmation dialog appears" should happen')
def step_impl(context):
    assert context.patient_groups_page.verify_archive_dialog_opens(), "Archive confirmation dialog did not appear"


@then(u'"Duplicate Patient Group details page loads" should happen')
def step_impl(context):
    assert context.patient_groups_page.is_navigated_to_duplicate_page(), "Duplicate Patient Group details page did not load"


@when(u'I select {records} records per page from dropdown for patient groups table')
def step_impl(context, records):
    context.patient_groups_page = PatientGroupsPage(context.driver)
    result = context.patient_groups_page.select_records_per_page(records)
    if not result:
        raise AssertionError(f"Failed to select {records} records per page")


@then(u'the patient groups table should display exactly {records} records per page')
def step_impl(context, records):
    assert context.patient_groups_page.verify_patient_group_records_per_page(records), \
        f"Programs table did not display exactly {records} records per page."


@when(u'I click on "Create New Group" button')
def step_impl(context):
    context.patient_groups_page = PatientGroupsPage(context.driver)
    context.patient_groups_page.click_create_new_group()


@when(u'I select "{option}" from the create menu')
def step_impl(context, option):
    result = context.patient_groups_page.select_create_option(option)
    if not result:
        raise AssertionError(f"Failed to select {option}")


@then(u'I should be navigated to the "{page}" page')
def step_impl(context, page):
    assert context.patient_groups_page.verify_navigation_to_create_page(
        page), f"Did not navigate to {page} page as expected"
