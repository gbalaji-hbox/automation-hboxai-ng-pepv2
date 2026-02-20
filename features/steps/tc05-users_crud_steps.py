from behave import when, then

from features.pages.users_page.users_page import UsersPage
from utils.logger import printf


@when(u'I click "Add New User" button')
def step_impl(context):
    context.user_page = UsersPage(context.driver)
    context.user_page.click_add_new_user()


@when(u'I fill the create user form with valid data')
def step_impl(context):
    context.user_info = context.user_page.fill_create_user_form()
    context.user_email = context.user_info['email']


@when(u'I click "Save" button on the modal')
def step_impl(context):
    context.user_page.submit_user_form()


@then(u'notification "User Created" appears')
def step_impl(context):
    assert context.user_page.check_user_notification("User Created"), \
        "User Created notification not appeared"


@when(u'I find the created user in the list and click edit')
def step_impl(context):
    context.user_page.find_and_edit_user(context.user_email)


@when(u'I update the user last name to "Edited"')
def step_impl(context):
    context.user_page.update_user_last_name("Edited")


@then(u'notification "User updated successfully" appears')
def step_impl(context):
    assert context.user_page.check_user_notification(
        "User updated successfully"), "User Updated notification not appeared"


@when(u'I find the edited user in the list and click delete')
def step_impl(context):
    context.user_page.find_and_delete_user(context.user_email)


@when(u'I confirm the user delete in the dialog')
def step_impl(context):
    context.user_page.confirm_user_delete()


@then(u'notification "User deleted successfully" appears')
def step_impl(context):
    assert context.user_page.check_user_notification(
        "User deleted successfully"), "User Deleted notification not appeared"


@when(u'I enter "{character}" in "{field}" input field')
def step_impl(context, character, field):
    context.expected_error = context.user_page.get_expected_message(field)
    context.user_page.enter_text_in_field(field, character)


@when(u'I clear the "{field}" input field')
def step_impl(context, field):
    context.user_page.clear_field(field)


@then(u'validation error message appears for "{field}"')
def step_impl(context, field):
    assert context.user_page.check_validation_error_for_field(field, context.expected_error), \
        f"Validation error for {field} not appeared"


@when(u'I click "Cancel" button on the modal')
def step_impl(context):
    context.user_page.cancel_user_form()


@then(u'modal closes without creating user')
def step_impl(context):
    assert context.user_page.is_returned_to_users_page(), "Modal did not close properly"


@when(u'I delete all users containing "{text}" in their email')
def step_impl(context, text):
    context.user_page = UsersPage(context.driver)
    context.user_page.delete_users_with_email_containing(text)


@then(u'all test automation users should be deleted')
def step_impl(context):
    # Check if no users with automation in email
    printf("Cleanup completed")
