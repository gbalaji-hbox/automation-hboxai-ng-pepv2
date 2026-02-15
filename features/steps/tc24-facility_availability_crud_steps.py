from behave import when, then

from features.pages.facility_availability_page.facility_availability_page import FacilityAvailabilityPage


@when(u'I click "Add New Facility Availability" button')
def step_impl(context):
    context.facility_availability_page = FacilityAvailabilityPage(context.driver)
    context.facility_availability_page.click_add_new_facility_availability()


@when(u'I fill the create facility availability form with valid data')
def step_impl(context):
    if not hasattr(context, "facility_availability_page"):
        context.facility_availability_page = FacilityAvailabilityPage(context.driver)
    context.facility_availability_data = context.facility_availability_page.fill_create_facility_availability_form()


@when(u'I click "Create Facility Availability" button on the facility availability form')
def step_impl(context):
    context.facility_availability_page.submit_create_facility_availability()


@then(u'notification "Facility availability created successfully" appears')
def step_impl(context):
    assert context.facility_availability_page.check_facility_availability_notification("created"), \
        "Facility availability created notification not appeared"


@when(u'I find the created facility availability in the list and click edit')
def step_impl(context):
    context.facility_availability_page.find_and_edit_facility_availability(context.facility_availability_data)


@when(u'I update the facility availability end date')
def step_impl(context):
    updated_end_date = context.facility_availability_page.update_facility_availability_end_date(
        context.facility_availability_data["end_date"]
    )
    context.facility_availability_data["end_date"] = updated_end_date


@when(u'I click "Update Facility Availability" button on the facility availability form')
def step_impl(context):
    context.facility_availability_page.submit_update_facility_availability()


@then(u'notification "Facility availability updated successfully" appears')
def step_impl(context):
    assert context.facility_availability_page.check_facility_availability_notification("updated"), \
        "Facility availability updated notification not appeared"


@when(u'I find the updated facility availability in the list and click delete')
def step_impl(context):
    context.facility_availability_page.find_and_delete_facility_availability(context.facility_availability_data)


@when(u'I confirm the facility availability delete in the dialog')
def step_impl(context):
    context.facility_availability_page.confirm_facility_availability_delete()


@then(u'notification "Facility availability delete failed" appears')
def step_impl(context):
    assert context.facility_availability_page.check_facility_availability_notification("delete failed"), \
        "Facility availability delete failed notification not appeared"


@when(u'I click "Cancel" button on the facility availability form')
def step_impl(context):
    context.facility_availability_page.cancel_facility_availability_form()


@then(u'facility availability form closes without creating record')
def step_impl(context):
    assert context.facility_availability_page.is_navigated_to_facility_availability_page(), \
        "Facility availability form did not close properly"
