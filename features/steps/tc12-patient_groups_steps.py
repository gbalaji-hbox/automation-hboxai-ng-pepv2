from behave import when, then, given

from features.pages.patient_groups_page.patient_groups_page import PatientGroupsPage
from utils.logger import printf


@given(u'I am on the Patient Groups page')
def step_impl(context):
    context.patient_groups_page = PatientGroupsPage(context.driver)
    # Assuming we're already on the patient groups page from login


@when(u'I apply filters with clinic "{clinic}"')
def step_impl(context, clinic):
    result = context.patient_groups_page.apply_filters_for_patient_group(clinic=clinic)
    if not result:
        raise AssertionError(f"Failed to apply filters with clinic: {clinic}")


@when(u'I select {count} random patients from the filtered results')
def step_impl(context, count):
    count = int(count)
    result = context.patient_groups_page.select_patients_from_table(count)
    if not result:
        raise AssertionError(f"Failed to select {count} patients")


@when(u'I extract the EMR IDs from the selected patients')
def step_impl(context):
    context.extracted_emr_ids = context.patient_groups_page.extract_emr_ids_from_selected_patients(5)
    if not context.extracted_emr_ids or len(context.extracted_emr_ids) != 5:
        raise AssertionError(f"Failed to extract 5 EMR IDs. Got: {context.extracted_emr_ids}")


@when(u'I name the group "{group_name}" and save it')
def step_impl(context, group_name):
    result = context.patient_groups_page.click_create_group_button()
    if not result:
        raise AssertionError("Failed to click Create Group button")

    result = context.patient_groups_page.name_and_save_patient_group(group_name)
    if not result:
        raise AssertionError(f"Failed to name and save group: {group_name}")


@then(u'the patient group should be created successfully')
def step_impl(context):
    assert context.patient_groups_page.verify_group_created_successfully(), "Patient group was not created successfully"


@when(u'I create patient group by EMRs with clinic "{clinic}" and the previously extracted EMR IDs')
def step_impl(context, clinic):
    if not hasattr(context, 'extracted_emr_ids') or not context.extracted_emr_ids:
        raise AssertionError("No extracted EMR IDs found. Run the filter scenario first.")

    result = context.patient_groups_page.create_patient_group_by_emrs(clinic, context.extracted_emr_ids)
    if not result:
        raise AssertionError(f"Failed to create patient group by EMRs with clinic: {clinic}")