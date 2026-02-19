from behave import when, then, given

from features.pages.users_page.user_group_page import UserGroupPage
from utils.logger import printf


@when(u'I click "Add New User Group" button')
def step_impl(context):
    context.user_group_page = UserGroupPage(context.driver)
    context.user_group_page.click_add_new_user_group()

@when(u'I fill the create user group form with valid data')
def step_impl(context):
    context.group_info = context.user_group_page.fill_create_user_group_form()
    context.group_name = context.group_info['name']

@then(u'notification "User Group Created" appears')
def step_impl(context):
    assert context.user_group_page.check_group_notification("User Group Created"), "User Group Created notification not appeared"

@when(u'I find the created user group in the list and click edit')
def step_impl(context):
    context.user_group_page.find_and_edit_user_group(context.group_name)

@when(u'I update the user group name to "Edited"')
def step_impl(context):
    context.edited_group_name = context.user_group_page.update_user_group_name("Edited")

@then(u'notification "User group updated successfully" appears')
def step_impl(context):
    assert context.user_group_page.check_group_notification("User group updated successfully"), "User Group Updated notification not appeared"

@when(u'I find the edited user group in the list and click delete')
def step_impl(context):
    context.user_group_page.find_and_delete_user_group(context.edited_group_name)

@when(u'I confirm the user group delete in the dialog')
def step_impl(context):
    context.user_group_page.confirm_user_group_delete()

@then(u'notification "User group deleted successfully" appears')
def step_impl(context):
    assert context.user_group_page.check_group_notification("User group deleted successfully"), "User Group Deleted notification not appeared"

@then(u'modal closes without creating user group')
def step_impl(context):
    assert context.user_page.is_returned_to_users_page(), "Modal did not close properly"

@when(u'I delete all user groups containing "{text}" in their name')
def step_impl(context, text):
    context.user_group_page = UserGroupPage(context.driver)
    context.user_group_page.delete_user_groups_with_name_containing(text)

@then(u'all test automation user groups should be deleted')
def step_impl(context):
    # Check if no user groups with automation in name
    printf("Cleanup completed")