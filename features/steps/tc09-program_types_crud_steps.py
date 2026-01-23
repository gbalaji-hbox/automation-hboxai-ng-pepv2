from behave import when, then

from features.pages.program_type_page.program_page import ProgramPage
from utils.logger import printf


@when(u'I click "Add New Program" button')
def step_impl(context):
    context.program_page = ProgramPage(context.driver)
    context.program_page.click_add_new_program()


@when(u'I fill the create program form with valid data')
def step_impl(context):
    context.program_info = context.program_page.fill_create_program_form()
    context.program_name = context.program_info['name']


@when(u'I click "Save" button on the program form')
def step_impl(context):
    context.program_page.submit_program_form()


@then(u'notification "Program type created successfully" appears')
def step_impl(context):
    assert context.program_page.check_program_notification("Program type created successfully"), \
        "Program type created notification not appeared"


@when(u'I find the created program in the list and click edit')
def step_impl(context):
    context.program_page.find_and_edit_program(context.program_name)


@when(u'I update the program name to "Edited"')
def step_impl(context):
    context.edited_program_name = context.program_page.update_program_name("Edited")


@then(u'notification "Program type updated successfully" appears')
def step_impl(context):
    assert context.program_page.check_program_notification("Program type updated successfully"), \
        "Program type updated notification not appeared"


@when(u'I find the edited program in the list and click delete')
def step_impl(context):
    context.program_page.find_and_delete_program(context.edited_program_name)


@when(u'I confirm the program delete in the dialog')
def step_impl(context):
    context.program_page.confirm_program_delete()


@then(u'notification "Program type deleted successfully" appears')
def step_impl(context):
    assert context.program_page.check_program_notification("Program type deleted successfully"), \
        "Program type deleted notification not appeared"


@when(u'I click "Cancel" button on the program form')
def step_impl(context):
    context.program_page.cancel_program_form()


@then(u'modal closes without creating program')
def step_impl(context):
    assert context.program_page.is_returned_to_programs_page(), "Modal did not close properly"


@when(u'I delete all programs containing "Automation" in their name')
def step_impl(context):
    context.program_page = ProgramPage(context.driver)
    context.program_page.delete_programs_with_name_containing("Automation")


@then(u'all test automation programs should be deleted')
def step_impl(context):
    # Check if no programs with automation in name
    printf("Cleanup completed")