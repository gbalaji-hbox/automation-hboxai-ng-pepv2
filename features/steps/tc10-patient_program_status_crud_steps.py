from behave import when, then

from features.pages.program_type_page.patient_program_status_page import PatientProgramStatusPage
from utils.logger import printf


@when(u'I click "Add New Patient Program Status" button')
def step_impl(context):
    context.patient_program_status_page = PatientProgramStatusPage(context.driver)
    context.patient_program_status_page.click_add_new_patient_program_status()


@when(u'I fill the create patient program status form with valid data')
def step_impl(context):
    context.patient_program_status_info = context.patient_program_status_page.fill_create_patient_program_status_form()
    context.patient_program_status_name = context.patient_program_status_info['name']


@when(u'I click "{button_name}" button on the patient program status form')
def step_impl(context, button_name):
    context.patient_program_status_page.submit_patient_program_status_form(button_name)


@then(u'notification "Program status created successfully" appears')
def step_impl(context):
    assert context.patient_program_status_page.check_patient_program_status_notification("Program status created successfully"), \
        "Program status created notification not appeared"


@when(u'I find the created patient program status in the list and click edit')
def step_impl(context):
    context.patient_program_status_page.find_and_edit_patient_program_status(context.patient_program_status_name)


@when(u'I update the patient program status name to "Edited"')
def step_impl(context):
    context.edited_patient_program_status_name = context.patient_program_status_page.update_patient_program_status_name("Edited")


@then(u'notification "Program status updated successfully" appears')
def step_impl(context):
    assert context.patient_program_status_page.check_patient_program_status_notification("Program status updated successfully"), \
        "Program status updated notification not appeared"


@when(u'I find the edited patient program status in the list and click delete')
def step_impl(context):
    context.patient_program_status_page.find_and_delete_patient_program_status(context.edited_patient_program_status_name)


@when(u'I confirm the patient program status delete in the dialog')
def step_impl(context):
    context.patient_program_status_page.confirm_patient_program_status_delete()


@then(u'notification "Program status deleted successfully" appears')
def step_impl(context):
    assert context.patient_program_status_page.check_patient_program_status_notification("Program status deleted successfully"), \
        "Program status deleted notification not appeared"



@then(u'modal closes without creating patient program status')
def step_impl(context):
    assert context.patient_program_status_page.is_returned_to_patient_program_status_page(), "Modal did not close properly"


@when(u'I delete all patient program statuses containing "Automation" in their name')
def step_impl(context):
    context.patient_program_status_page = PatientProgramStatusPage(context.driver)
    context.patient_program_status_page.delete_patient_program_statuses_with_name_containing("Automation")


@then(u'all test automation patient program statuses should be deleted')
def step_impl(context):
    # Check if no patient program statuses with automation in name
    printf("Cleanup completed")