from behave import when, then

from features.pages.patient_groups_page.patient_groups_page import PatientGroupsPage


@when(u'I select first {count} patients in the patient results table')
def step_impl(context, count):
    context.patient_groups_page.select_patients_from_table(count)


# ==================== Duplicate Group Steps ====================

@when(u'I find a patient group and click duplicate')
def step_impl(context):
    context.patient_groups_page = PatientGroupsPage(context.driver)
    context.patient_groups_page.click_duplicate_button()


@then(u'the duplicate page should open with correct heading')
def step_impl(context):
    assert context.patient_groups_page.verify_duplicate_page_heading(), \
        "Duplicate page heading not found"


@then(u'the default group name should contain "(Copy)"')
def step_impl(context):
    default_name = context.patient_groups_page.get_default_duplicate_group_name()
    assert default_name is not None, "Could not get default duplicate group name"
    assert "(Copy)" in default_name, \
        f"Default group name does not contain '(Copy)': {default_name}"


@when(u'I click create group button on duplicate page')
def step_impl(context):
    context.patient_groups_page.click_create_group_on_duplicate_page()


@then(u'the duplicate patient group should be created successfully')
def step_impl(context):
    assert context.patient_groups_page.verify_duplicate_group_created(), \
        "Duplicate patient group was not created successfully"


# ==================== Archive/Unarchive Group Steps ====================

@when(u'I find a patient group and click archive')
def step_impl(context):
    context.patient_groups_page = PatientGroupsPage(context.driver)
    context.first_row_data = context.patient_groups_page.click_archive_button()


@then(u'the archive confirmation dialog should appear')
def step_impl(context):
    assert context.patient_groups_page.verify_archive_dialog_opens(cancel_after_verify=False), \
        "Archive confirmation dialog did not appear"


@when(u'I confirm the archive action')
def step_impl(context):
    context.patient_groups_page.confirm_archive()


@then(u'the patient group should be archived successfully')
def step_impl(context):
    assert context.patient_groups_page.is_archived_success_message_displayed(), \
        "Archive success message not displayed"


@when(u'I click on Archived Groups button')
def step_impl(context):
    context.patient_groups_page.navigate_to_archived_groups()


@then(u'the archived groups page should open')
def step_impl(context):
    assert context.patient_groups_page.verify_archived_groups_page(), \
        "Archived groups page did not open"


@then(u'the archived group should appear in the list')
def step_impl(context):
    # Verify the archived group is visible in the list by checking for Archived status
    group_name = context.first_row_data['Group Name'] if context.first_row_data else None
    assert group_name is not None, "Group name not found in context"
    assert context.patient_groups_page.verify_group_archived(group_name), \
        "Patient group was not archived successfully"


@when(u'I click the unarchive button for the archived group')
def step_impl(context):
    context.patient_groups_page.click_unarchive_button()


@then(u'the unarchive confirmation dialog should appear')
def step_impl(context):
    assert context.patient_groups_page.verify_unarchive_dialog_opens(), \
        "Unarchive confirmation dialog did not appear"


@when(u'I confirm the unarchive action')
def step_impl(context):
    context.patient_groups_page.confirm_unarchive()


@then(u'the patient group should be restored to active status')
def step_impl(context):
    group_name = context.first_row_data['Group Name'] if context.first_row_data else None
    assert group_name is not None, "Group name not found in context"
    assert context.patient_groups_page.verify_group_unarchived(group_name), \
        "Patient group was not restored to active status"
