from behave import when, then, given
from behave.exception import StepNotImplementedError

from features.pages.users_page.users_page import UsersPage


@given(u'I am on the {tab_name} tab')
def step_impl(context, tab_name):
    context.user_page = UsersPage(context.driver)
    context.user_page.click_on_tab(tab_name)


@when(u'I fetch the first row data from the users table')
def step_impl(context):
    context.first_row_data = context.user_page.get_first_row_data()


@when(u'I enter that value in the "{field}" search field and search')
def step_impl(context, field):
    if not hasattr(context, 'first_row_data') or not context.first_row_data:
        context.first_row_data = context.user_page.get_first_row_data()

    context.search_criteria = field
    if field == 'Email':
        data_field = 'Email Address'
    else:
        data_field = field

    context.search_value = context.first_row_data.get(data_field)

    result = context.user_page.perform_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@then(u'the users table should filter results to show matching groups')
def step_impl(context):
    if not hasattr(context, 'search_criteria') or not hasattr(context, 'search_value'):
        raise AssertionError("Search criteria and value not set. Run search step first.")

    assert context.user_page.verify_search_results(
        context.search_criteria, context.search_value
    ), f"Dynamic search failed for {context.search_criteria}: {context.search_value}"

@when(u'I click on "{action_button}" button for a user in the users table')
def step_impl(context, action_button):
    context.user_page.click_on_action_button(action_button)


@then(u'"User Operation History dialog opens" should happen')
def step_impl(context):
    assert context.user_page.is_user_history_dialog_open(), \
        'User Operation History dialog did not open as expected.'


@then(u'"Edit User page loads" should happen')
def step_impl(context):
    assert context.user_page.is_navigated_to_edit_user_page(), \
        'Edit User page did not load as expected.'


@then(u'"confirmation dialog appears" should happen')
def step_impl(context):
    assert context.user_page.is_delete_confirmation_dialog_open(), 'Delete Confirmation dialog did not appears as expected.'

@when(u'I select {count} records per page from pagination dropdown')
def step_impl(context, count):
    context.user_page.select_records_per_page(count)


@then(u'the table should display exactly {count} records per page')
def step_impl(context, count):
    assert context.user_page.verify_rows_per_page(count), \
        f'Table did not display exactly {count} records per page as expected.'
