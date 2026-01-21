from behave import given, when, then
from utils.logger import printf


@given(u'I am on the Program tab from Program Type')
def step_impl(context):
    raise StepNotImplementedError(u'Given I am on the Program tab from Program Type')

@when('I fetch the first row data from the program table')
def step_impl(context):
    """Fetch first row data from program table"""
    context.first_row_data = context.program_type_page.get_first_program_row_data()
    assert context.first_row_data, "Failed to fetch first row data from program table"
    printf(f"First row program data: {context.first_row_data}")

@when(u'I enter that value in the "{search_criteria}" search field and search on program tab in in Program Type page')
def step_impl(context, search_criteria):
    raise StepNotImplementedError(u'When I enter that value in the "Program Name" search field and search on program tab in in Program Type page')


@then(u'the program table should show filtered results in Program Type page')
def step_impl(context):
    raise StepNotImplementedError(u'Then the program table should show filtered results in Program Type page')

@when('I fetch the first row data from the patient program status table')
def step_impl(context):
    """Fetch first row data from patient program status table"""
    context.first_row_data = context.program_type_page.get_first_patient_program_status_row_data()
    assert context.first_row_data, "Failed to fetch first row data from patient program status table"
    printf(f"First row status data: {context.first_row_data}")
