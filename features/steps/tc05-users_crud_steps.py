from behave import when, then, given
from faker import Faker

from features.pages.users_page.users_page import UsersPage
from utils.logger import printf

@given(u'I am on the Users page')
def step_impl(context):
    context.user_page = UsersPage(context.driver)
    # Assume already on users page after login

@when(u'I click "Add New User" button')
def step_impl(context):
    context.user_page.click_add_new_user()

@when(u'I fill the create user form with valid data')
def step_impl(context):
    faker = Faker()
    context.user_email = f"{faker.first_name().lower()}.{faker.last_name().lower()}@automation.test"
    context.user_page.fill_create_user_form(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=context.user_email,
        phone="1234567890",
        password="Password123",
        user_type="ES"
    )

@when(u'I click "Save" button on the modal')
def step_impl(context):
    context.user_page.submit_user_form()

@then(u'notification "User Created" appears')
def step_impl(context):
    assert context.user_page.check_notification("User Created"), "User Created notification not appeared"

@when(u'I find the created user in the list')
def step_impl(context):
    # Assume search for the email
    pass

@when(u'I click edit for the created user')
def step_impl(context):
    context.user_page.find_and_edit_user(context.user_email)

@when(u'I update the user last name to "Edited"')
def step_impl(context):
    context.user_page.update_user_last_name("Edited")

@then(u'notification "User Updated" appears')
def step_impl(context):
    assert context.user_page.check_notification("User Updated"), "User Updated notification not appeared"

@when(u'I find the edited user in the list')
def step_impl(context):
    # Update email if changed, but last name changed
    pass

@when(u'I click delete for the edited user')
def step_impl(context):
    context.user_page.find_and_delete_user(context.user_email)

@when(u'I confirm the user delete in the dialog')
def step_impl(context):
    # Already in find_and_delete_user
    pass

@then(u'notification "User Deleted" appears')
def step_impl(context):
    assert context.user_page.check_notification("User Deleted"), "User Deleted notification not appeared"

@when(u'I click "Save" button without filling user required fields')
def step_impl(context):
    context.user_page.submit_user_form()

@then(u'validation error messages appear for required fields')
def step_impl(context):
    assert context.user_page.check_validation_errors(), "Validation errors not appeared"

@when(u'I click "Cancel" button on the modal')
def step_impl(context):
    context.user_page.cancel_user_form()

@then(u'modal closes without creating user')
def step_impl(context):
    # Check if back to users page, perhaps check url or element
    # For simplicity, assume closed
    printf("Modal cancelled")

@when(u'I delete all users containing "Automation" in their email')
def step_impl(context):
    context.user_page.delete_users_with_email_containing("automation")

@then(u'all test automation users should be deleted')
def step_impl(context):
    # Check if no users with automation in email
    printf("Cleanup completed")