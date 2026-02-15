from behave import given, when, then

from features.pages.workflow_tasks_page.workflow_page import WorkflowPage


@given(u'I am on the Workflow tab from workflow tasks')
def step_impl(context):
    context.workflow_page = WorkflowPage(context.driver)
    context.workflow_page.navigate_to_tab()


@when(u'I fetch the first row data from the workflow table')
def step_impl(context):
    context.first_row_workflow_data = context.workflow_page.get_workflow_first_row_data()


@when(u'I select {field} option and enter the fetched data in workflow search box')
def step_impl(context, field):
    if not hasattr(context, 'first_row_workflow_data') or not context.first_row_workflow_data:
        context.first_row_workflow_data = context.workflow_page.get_workflow_first_row_data()

    context.search_criteria = field
    context.search_value = context.first_row_workflow_data.get(field)
    result = context.workflow_page.perform_workflow_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the workflow search results should match in workflow table')
def step_impl(context):
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.workflow_page.verify_workflow_search_results(
        context.search_criteria,
        context.search_value
    ), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"


@when(u'I click on "{action_button}" button in workflow table first row')
def step_impl(context, action_button):
    context.workflow_page.click_on_workflow_action_button(action_button)


@then(u'"Workflow Operation History dialog opens" should happen')
def step_impl(context):
    assert context.workflow_page.verify_workflow_operation_history_dialog(), \
        "Workflow Operation History dialog did not open as expected."


@then(u'"Edit workflow page loads" should happen')
def step_impl(context):
    assert context.workflow_page.is_navigated_to_workflow_edit_page(), \
        "Edit workflow page did not load as expected."


@then(u'"Workflow delete confirmation dialog appears" should happen')
def step_impl(context):
    assert context.workflow_page.verify_workflow_delete_confirmation_dialog(), \
        "Workflow delete confirmation dialog did not appear as expected."


@when(u'I select {records} records per page for workflow table')
def step_impl(context, records):
    context.workflow_page.select_workflow_records_per_page(records)


@then(u'the workflow table should display exactly {records} records per page for workflow tab')
def step_impl(context, records):
    assert context.workflow_page.verify_workflow_records_per_page(records), \
        f"Workflow table did not display exactly {records} records per page."
