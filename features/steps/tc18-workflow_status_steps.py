from behave import given, when, then

from features.pages.workflow_tasks_page.workflow_status_page import WorkflowStatusPage


@given(u'I am on the Workflow Status tab from workflow tasks')
def step_impl(context):
    context.workflow_status_page = WorkflowStatusPage(context.driver)
    context.workflow_status_page.navigate_to_tab()


@when(u'I fetch the first row data from the workflow status table')
def step_impl(context):
    context.first_row_workflow_status_data = context.workflow_status_page.get_workflow_status_first_row_data()


@when(u'I enter the "{field}" value in workflow status search box')
def step_impl(context, field):
    if not hasattr(context, 'first_row_workflow_status_data') or not context.first_row_workflow_status_data:
        context.first_row_workflow_status_data = context.workflow_status_page.get_workflow_status_first_row_data()

    context.search_criteria = field
    context.search_value = context.first_row_workflow_status_data.get(field)
    result = context.workflow_status_page.perform_workflow_status_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the workflow status search results should match in workflow status table')
def step_impl(context):
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.workflow_status_page.verify_workflow_status_search_results(
        context.search_criteria,
        context.search_value
    ), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"


@when(u'I click on "{action_button}" button in workflow status table first row')
def step_impl(context, action_button):
    context.workflow_status_page.click_on_workflow_status_action_button(action_button)


@then(u'"Workflow Status Operation History dialog opens" should happen')
def step_impl(context):
    assert context.workflow_status_page.verify_workflow_status_operation_history_dialog(), \
        "Workflow Status Operation History dialog did not open as expected."


@then(u'"Edit workflow status page loads" should happen')
def step_impl(context):
    assert context.workflow_status_page.is_navigated_to_workflow_status_edit_page(), \
        "Edit workflow status page did not load as expected."


@then(u'"Workflow status delete confirmation dialog appears" should happen')
def step_impl(context):
    assert context.workflow_status_page.verify_workflow_status_delete_confirmation_dialog(), \
        "Workflow status delete confirmation dialog did not appear as expected."


@when(u'I select {records} records per page for workflow status table')
def step_impl(context, records):
    context.workflow_status_page.select_workflow_status_records_per_page(records)


@then(u'the workflow status table should display exactly {records} records per page for workflow status tab')
def step_impl(context, records):
    assert context.workflow_status_page.verify_workflow_status_records_per_page(records), \
        f"Workflow status table did not display exactly {records} records per page."
