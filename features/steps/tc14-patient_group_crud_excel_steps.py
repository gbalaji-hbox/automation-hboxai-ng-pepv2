from behave import when, then


@when(u'I create patient group by excel upload containing "enrollment_patient_ids"')
def step_impl(context):
    context.group_name = context.patient_groups_page.create_patient_group_by_excel_upload()

@then(u'the patient group uploaded by excel should be created successfully')
def step_impl(context):
    assert context.patient_groups_page.verify_patient_group_created_by_excel_upload(), \
        "Patient group uploaded by excel was not created successfully"

