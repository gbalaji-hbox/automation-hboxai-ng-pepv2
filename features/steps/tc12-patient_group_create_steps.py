from behave import when, then

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