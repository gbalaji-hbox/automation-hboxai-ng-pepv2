from behave import when


@when(u'I select first {count} patients in the patient results table')
def step_impl(context, count):
    context.patient_groups_page.select_patients_from_table(count)