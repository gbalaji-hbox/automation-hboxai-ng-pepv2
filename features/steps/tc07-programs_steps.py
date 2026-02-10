from behave import given, when, then

from features.pages.program_type_page.program_page import ProgramPage


@given(u'I am on the {tab_name} tab from program type')
def step_impl(context, tab_name):
    context.program_page = ProgramPage(context.driver)
    context.program_page.navigate_to_tab(tab_name)


@when(u'I fetch the first row data from the programs table')
def step_impl(context):
    context.first_row_program_data = context.program_page.get_program_first_row_data()


@when(u'I select {field} option and enter the fetched data in the search box')
def step_impl(context, field):
    if not hasattr(context, 'first_row_program_data') or not context.first_row_program_data:
        context.first_row_data = context.user_page.get_program_first_row_data()
    context.search_criteria = field
    context.search_value = context.first_row_program_data.get(field)
    result = context.program_page.perform_program_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the {tab_name} table should show matching results')
def step_impl(context, tab_name):
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.program_page.verify_program_search_results(
        context.search_criteria, context.search_value, tab_name
    ), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"

@when(u'I click on "{action_button}" button in programs table first row')
def step_impl(context, action_button):
    context.program_page.click_on_program_action_button(action_button)

@then(u'"Program Operation History dialog opens" should happen')
def step_impl(context):
    assert context.program_page.verify_program_operation_history_dialog(), \
        "Program Operation History dialog did not open as expected."


@then(u'"Edit program page loads" should happen')
def step_impl(context):
    assert context.program_page.is_navigated_to_program_edit_page(), \
        "Edit program page did not load as expected."


@then(u'"Program delete confirmation dialog appears" should happen')
def step_impl(context):
    assert context.program_page.verify_program_delete_confirmation_dialog(), \
        "Program delete confirmation dialog did not appear as expected."

@when(u'I select {records} records per page for programs table')
def step_impl(context, records):
    context.program_page.select_programs_records_per_page(records)


@then(u'the Programs table should display exactly {records} records per page')
def step_impl(context, records):
    assert context.program_page.verify_program_records_per_page(records), \
        f"Programs table did not display exactly {records} records per page."

