from behave import when, then
from features.pages.add_patient_page.add_patient_page import AddPatientPage


@when(u'I select "{clinic_name}" clinic')
def step_impl(context, clinic_name):
    context.add_patient_page = AddPatientPage(context.driver)
    context.add_patient_page.select_clinic(clinic_name)


@when(u'I select "{facility_name}" facility')
def step_impl(context, facility_name):
    context.add_patient_page.select_facility(facility_name)


@when(u'I select the first available provider')
def step_impl(context):
    context.add_patient_page.select_first_available_provider()


@when(u'I fill the patient personal information with valid data')
def step_impl(context):
    context.patient_info = context.add_patient_page.fill_personal_information(include_optional=False)


@when(u'I fill the patient personal information with valid data including optional fields')
def step_impl(context):
    context.patient_info = context.add_patient_page.fill_personal_information(include_optional=True)


@when(u'I fill the medical records with valid data')
def step_impl(context):
    context.medical_info = context.add_patient_page.fill_medical_records(include_optional=False)


@when(u'I fill the medical records with valid data including optional fields')
def step_impl(context):
    context.medical_info = context.add_patient_page.fill_medical_records(include_optional=True)


@when(u'I select "{program}" program eligibility')
def step_impl(context, program):
    context.add_patient_page.select_program_eligibility(program)


@when(u'I fill the emergency contact information')
def step_impl(context):
    context.emergency_info = context.add_patient_page.fill_emergency_contact()


@when(u'I click "Continue" button to proceed to address')
def step_impl(context):
    context.add_patient_page.click_continue_button()


@when(u'I fill the address information with valid data')
def step_impl(context):
    context.address_info = context.add_patient_page.fill_address_information(include_optional=False)


@when(u'I fill the address information with valid data including optional fields')
def step_impl(context):
    context.address_info = context.add_patient_page.fill_address_information(include_optional=True)


@when(u'I click "Continue" button to proceed to summary')
def step_impl(context):
    context.add_patient_page.click_continue_button()


@when(u'I verify the summary page displays all patient information')
def step_impl(context):
    assert context.add_patient_page.verify_summary_displays_patient_info(), \
        "Summary page does not display all patient information sections"


@when(u'I click "Submit" button to create patient')
def step_impl(context):
    context.add_patient_page.click_submit_button()


@then(u'notification "Patient added successfully!" appears')
def step_impl(context):
    assert context.add_patient_page.is_patient_added_notification_visible(), \
        "Patient added successfully notification not appeared"


@then(u'the Continue button should be disabled')
def step_impl(context):
    context.add_patient_page = AddPatientPage(context.driver)
    assert context.add_patient_page.is_continue_button_disabled(), \
        "Continue button should be disabled when mandatory fields are empty"


@when(u'I click "Previous" button to go back')
def step_impl(context):
    context.add_patient_page.click_previous_button()


@then(u'I should be on the Patient Details step')
def step_impl(context):
    assert context.add_patient_page.is_on_patient_details_step(), \
        "Not on Patient Details step"


@then(u'the Facility dropdown should be disabled')
def step_impl(context):
    context.add_patient_page = AddPatientPage(context.driver)
    assert context.add_patient_page.is_facility_dropdown_disabled(), \
        "Facility dropdown should be disabled before selecting clinic"


@then(u'the Provider dropdown should be disabled')
def step_impl(context):
    assert context.add_patient_page.is_provider_dropdown_disabled(), \
        "Provider dropdown should be disabled before selecting clinic"