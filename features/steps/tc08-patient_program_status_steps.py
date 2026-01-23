from behave import when, then

from features.pages.program_type_page.patient_program_status_page import PatientProgramStatusPage


@when(u'I fetch the first row data from the patient programs status table')
def step_impl(context):
    context.patient_program_status_page = PatientProgramStatusPage(context.driver)
    context.first_row_program_data = context.patient_program_status_page.get_patient_program_status_first_row_data()


@when(u'I enter the "{field}" value in the patient program status search box')
def step_impl(context, field):
    if not hasattr(context, 'first_row_program_data') or not context.first_row_program_data:
        context.first_row_program_data = context.patient_program_status_page.get_patient_program_status_first_row_data()
    context.search_criteria = field
    context.search_value = context.first_row_program_data.get(field)
    result = context.patient_program_status_page.perform_patient_program_status_search_by_field(field, context.search_value)

    if not result:
        raise AssertionError(f"Failed to perform search for field: {field}")


@when(u'I click on "{action_button}" button in patient program status table first row')
def step_impl(context, action_button):
    context.patient_program_status_page = PatientProgramStatusPage(context.driver)
    context.patient_program_status_page.click_on_patient_program_status_action_button(action_button)

@then(u'"Patient Program Status Operation History dialog opens" should happen')
def step_impl(context):
    assert context.patient_program_status_page.verify_patient_program_status_operation_history_dialog(), \
        "Program Operation History dialog did not open as expected."


@then(u'"Edit patient program status page loads" should happen')
def step_impl(context):
    assert context.patient_program_status_page.is_navigated_to_patient_program_status_edit_page(), \
        "Edit program page did not load as expected."


@then(u'"Patient program status delete confirmation dialog appears" should happen')
def step_impl(context):
    assert context.patient_program_status_page.verify_patient_program_status_delete_confirmation_dialog(), \
        "Program delete confirmation dialog did not appear as expected."

@when(u'I select {records} records per page for patient program status table')
def step_impl(context, records):
    context.patient_program_status_page = PatientProgramStatusPage(context.driver)
    context.patient_program_status_page.select_patient_program_status_records_per_page(records)


@then(u'the Patient Program Status table should display exactly {records} records per page')
def step_impl(context, records):
    assert context.patient_program_status_page.verify_patient_program_status_records_per_page(records), \
        f"Programs table did not display exactly {records} records per page."
