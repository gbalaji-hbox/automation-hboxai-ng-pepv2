from behave import given, when, then

from features.pages.workflow_tasks_page.tasks_page import TasksPage


@given(u'I am on the Tasks tab from workflow tasks')
def step_impl(context):
    context.tasks_page = TasksPage(context.driver)
    context.tasks_page.navigate_to_tab()


@when(u'I fetch the first row data from the tasks table')
def step_impl(context):
    context.first_row_tasks_data = context.tasks_page.get_tasks_first_row_data()


@when(u'I enter the "{field}" value in tasks search box')
def step_impl(context, field):
    if not hasattr(context, 'first_row_tasks_data') or not context.first_row_tasks_data:
        context.first_row_tasks_data = context.tasks_page.get_tasks_first_row_data()

    context.search_criteria = field
    context.search_value = context.first_row_tasks_data.get(field)
    result = context.tasks_page.perform_tasks_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the tasks search results should match in tasks table')
def step_impl(context):
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.tasks_page.verify_tasks_search_results(
        context.search_criteria,
        context.search_value
    ), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"


@when(u'I click on "{action_button}" button in tasks table first row')
def step_impl(context, action_button):
    context.tasks_page.click_on_tasks_action_button(action_button)


@then(u'"Task Operation History dialog opens" should happen')
def step_impl(context):
    assert context.tasks_page.verify_tasks_operation_history_dialog(), \
        "Task Operation History dialog did not open as expected."


@then(u'"Edit task page loads" should happen')
def step_impl(context):
    assert context.tasks_page.is_navigated_to_task_edit_page(), \
        "Edit task page did not load as expected."


@then(u'"Task delete confirmation dialog appears" should happen')
def step_impl(context):
    assert context.tasks_page.verify_task_delete_confirmation_dialog(), \
        "Task delete confirmation dialog did not appear as expected."


@when(u'I select {records} records per page for tasks table')
def step_impl(context, records):
    context.tasks_page.select_tasks_records_per_page(records)


@then(u'the tasks table should display exactly {records} records per page for tasks tab')
def step_impl(context, records):
    assert context.tasks_page.verify_tasks_records_per_page(records), \
        f"Tasks table did not display exactly {records} records per page."
