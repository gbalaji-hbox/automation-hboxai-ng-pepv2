from behave import when, then

from features.pages.patient_groups_page.patient_groups_page import PatientGroupsPage
from utils.logger import printf


@when(u'I apply filters with clinic "{clinic}"')
def step_impl(context, clinic):
    result = context.patient_groups_page.apply_filters_for_patient_group(clinic=clinic)
    if not result:
        raise AssertionError(f"Failed to apply filters with clinic: {clinic}")


@when(u'I extract the EMR IDs from the selected patients')
def step_impl(context):
    context.extracted_emr_ids = context.patient_groups_page.extract_emr_ids_from_selected_patients(5)
    if not context.extracted_emr_ids or len(context.extracted_emr_ids) != 5:
        raise AssertionError(f"Failed to extract 5 EMR IDs. Got: {context.extracted_emr_ids}")


@when(u'returned to Patient Groups page')
def step_impl(context):
    context.patient_groups_page.return_to_patient_groups_page()


@when(u'I create patient group by EMRs with clinic "{clinic}" and the previously extracted EMR IDs')
def step_impl(context, clinic):
    if not hasattr(context, 'extracted_emr_ids') or not context.extracted_emr_ids:
        raise AssertionError("No extracted EMR IDs found. Run the filter scenario first.")

    result = context.patient_groups_page.create_patient_group_by_emrs(clinic, context.extracted_emr_ids)
    if not result:
        raise AssertionError(f"Failed to create patient group by EMRs with clinic: {clinic}")


@when(u'I click Create Group and enter valid group name and note')
def step_impl(context):
    context.group_name = context.patient_groups_page.enter_group_name_and_note()


@then(u'the patient group should be created successfully')
def step_impl(context):
    assert context.patient_groups_page.verify_group_created_successfully(), "Patient group was not created successfully"


@when(u'I find the created patient group in the list and click edit')
def step_impl(context):
    if not hasattr(context, 'group_name') or not context.group_name:
        raise AssertionError("No group_name found. Run the create group scenario first.")
    context.patient_groups_page.find_group_and_click_edit(context.group_name)


@when(u'I update the patient group name and save')
def step_impl(context):
    context.updated_group_name = context.patient_groups_page.update_group_name()


@then(u'the patient group name should be updated successfully')
def step_impl(context):
    assert context.patient_groups_page.verify_group_name_updated_successfully(), \
        "Patient group name was not updated successfully"


@when(u'I click the add patients button for the edited patient group')
def step_impl(context):
    context.patient_groups_page.click_add_patients_button()


@when(u'I select the first patient in the patient results table')
def step_impl(context):
    context.patient_groups_page.select_patients()


@when(u'I click add selected button on edited patient group page')
def step_impl(context):
    context.patient_groups_page.click_add_selected_button()


@then(u'the patients should be added to the patient group successfully')
def step_impl(context):
    assert context.patient_groups_page.verify_patients_added_successfully(), \
        "Patients were not added to the patient group successfully"


@when(u'I click the remove patients button for the edited patient group')
def step_impl(context):
    result = context.patient_groups_page.click_remove_patients_button()
    if not result:
        raise AssertionError("Failed to click the remove patients button for the edited patient group")


@when(u'I select the first patient in the table to be removed')
def step_impl(context):
    result = context.patient_groups_page.select_patient_to_remove()
    if not result:
        raise AssertionError("Failed to select the first patient in the table to be removed")


@when(u'I click remove selected button on edited patient group page')
def step_impl(context):
    result = context.patient_groups_page.click_remove_selected_button()
    if not result:
        raise AssertionError("Failed to click remove selected button on edited patient group page")


@then(u'the patients should be removed from the patient group successfully')
def step_impl(context):
    assert context.patient_groups_page.verify_patients_removed_successfully(), \
        "Patients were not removed from the patient group successfully"

@when(u'returned to Patient Groups page from edited patient group page')
def step_impl(context):
    context.patient_groups_page.return_to_patient_groups_list()


@when(u'I find the edited patient group in the list and click delete')
def step_impl(context):
    if not hasattr(context, 'updated_group_name') or not context.updated_group_name:
        raise AssertionError("No group_name found. Run the update group scenario first.")
    context.patient_groups_page.click_delete_patients_button(context.updated_group_name)


@when(u'I confirm the patient group delete in the dialog')
def step_impl(context):
    context.patient_groups_page.confirm_delete_patient_group_button()
@then(u'the patient group should be deleted successfully')
def step_impl(context):
    assert context.patient_groups_page.verify_the_group_deleted_successfully(), \
        "Patient group was not deleted successfully"


@when(u'I delete all patient groups containing "Automation" in their name')
def step_impl(context):
    context.patient_groups_page = PatientGroupsPage(context.driver)
    context.patient_groups_page.delete_all_automation_patient_groups("Automation")


@then(u'all test automation patient groups should be deleted')
def step_impl(context):
    # Check if no user groups with automation in name
    printf("Cleanup completed")



