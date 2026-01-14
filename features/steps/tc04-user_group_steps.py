from behave import when, then

from features.pages.users_page.user_group_page import UserGroupPage


@when(u'I fetch the first row data from the user groups table')
def step_impl(context):
    context.user_group_page = UserGroupPage(context.driver)
    context.first_row_data = context.user_group_page.get_first_row_data()

@then(u'"User group Operation History dialog opens" should happen')
def step_impl(context):
    context.user_group_page = UserGroupPage(context.driver)
    assert context.user_group_page.is_user_group_history_dialog_open(), \
        'User Operation History dialog did not open as expected.'


@then(u'"Edit User Group page loads" should happen')
def step_impl(context):
    context.user_group_page = UserGroupPage(context.driver)
    assert context.user_group_page.is_navigated_to_edit_user_group_page(), \
        'Edit User page did not load as expected.'

@then(u'"delete User Group confirmation dialog appears" should happen')
def step_impl(context):
    context.user_group_page = UserGroupPage(context.driver)
    assert context.user_group_page.is_delete_confirmation_dialog_open(), 'Delete Confirmation dialog did not appears as expected.'

@then(u'the user group table should display exactly {count} records per page')
def step_impl(context, count):
    context.user_group_page = UserGroupPage(context.driver)
    assert context.user_group_page.verify_rows_per_page(count), \
        f'Table did not display exactly {count} records per page as expected.'


