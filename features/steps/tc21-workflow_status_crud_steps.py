from behave import when, then

from features.pages.workflow_tasks_page.workflow_status_page import WorkflowStatusPage


@when(u'I click "Add New Workflow Status" button')
def step_impl(context):
    context.workflow_status_page = WorkflowStatusPage(context.driver)
    context.workflow_status_page.click_add_new_workflow_status()


@when(u'I fill the create workflow status form with valid data')
def step_impl(context):
    context.workflow_status_name = context.workflow_status_page.fill_create_workflow_status_form()


@when(u'I click "Save" button on the workflow status form')
def step_impl(context):
    context.workflow_status_page.submit_create_workflow_status()


@then(u'notification "Workflow Status created successfully" appears')
def step_impl(context):
    assert context.workflow_status_page.check_workflow_status_notification("created"), \
        "Workflow status created notification not appeared"


@when(u'I find the created workflow status in the list and click edit')
def step_impl(context):
    context.workflow_status_page.find_and_edit_workflow_status(context.workflow_status_name)


@when(u'I update the workflow status name to "Edited"')
def step_impl(context):
    context.edited_workflow_status_name = context.workflow_status_page.update_workflow_status_name("Edited")


@when(u'I click "Update" button on the workflow status form')
def step_impl(context):
    context.workflow_status_page.submit_update_workflow_status()


@then(u'notification "Workflow Status updated successfully" appears')
def step_impl(context):
    assert context.workflow_status_page.check_workflow_status_notification("updated"), \
        "Workflow status updated notification not appeared"


@when(u'I find the edited workflow status in the list and click delete')
def step_impl(context):
    context.workflow_status_page.find_and_delete_workflow_status(context.edited_workflow_status_name)


@when(u'I confirm the workflow status delete in the dialog')
def step_impl(context):
    context.workflow_status_page.confirm_workflow_status_delete()


@then(u'notification "Workflow Status deleted successfully" appears')
def step_impl(context):
    assert context.workflow_status_page.is_navigated_to_workflow_tasks_page(), \
        "Workflow status deleted notification not appeared"


@when(u'I click "Cancel" button on the workflow status form')
def step_impl(context):
    context.workflow_status_page.cancel_workflow_status_form()


@then(u'workflow status form closes without creating record')
def step_impl(context):
    assert context.workflow_status_page.is_navigated_to_workflow_tasks_page(), \
        "Workflow status form did not close properly"


@when(u'I delete all workflow statuses containing "Automation" in their name')
def step_impl(context):
    context.workflow_status_page = WorkflowStatusPage(context.driver)
    context.deleted_workflow_status_count = context.workflow_status_page.delete_workflow_statuses_with_name_containing("Automation")


@then(u'all test automation workflow statuses should be deleted')
def step_impl(context):
    pass
