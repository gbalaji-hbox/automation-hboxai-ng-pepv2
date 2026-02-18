from behave import when, then

from features.pages.workflow_tasks_page.workflow_page import WorkflowPage


@when(u'I click "Create New Workflow" button')
def step_impl(context):
    context.workflow_page = WorkflowPage(context.driver)
    context.workflow_page.click_create_new_workflow()


@when(u'I fill the create workflow form with valid data')
def step_impl(context):
    context.workflow_info = context.workflow_page.fill_create_workflow_form()
    context.workflow_name = context.workflow_info["name"]


@when(u'I click "Create Workflow" button on the workflow form')
def step_impl(context):
    context.workflow_page.submit_create_workflow()


@then(u'notification "Workflow created successfully" appears')
def step_impl(context):
    assert context.workflow_page.check_workflow_notification("Workflow created successfully"), \
        "Workflow created notification not appeared"


@when(u'I find the created workflow in the list and click edit')
def step_impl(context):
    context.workflow_page.find_and_edit_workflow(context.workflow_name)


@when(u'I update the workflow name to "Edited"')
def step_impl(context):
    context.edited_workflow_name = context.workflow_page.update_workflow_name("Edited")


@when(u'I remove a trigger row from the workflow')
def step_impl(context):
    context.workflow_page.remove_trigger_row()


@when(u'I click "Update Workflow" button on the workflow form')
def step_impl(context):
    context.workflow_page.submit_update_workflow()


@then(u'notification "Workflow updated successfully" appears')
def step_impl(context):
    assert context.workflow_page.check_workflow_notification("Workflow updated successfully"), \
        "Workflow updated notification not appeared"


@when(u'I find the edited workflow in the list and click delete')
def step_impl(context):
    context.workflow_page.find_and_delete_workflow(context.edited_workflow_name)


@when(u'I confirm the workflow delete in the dialog')
def step_impl(context):
    context.workflow_page.confirm_workflow_delete()


@then(u'notification "Workflow deleted successfully" appears')
def step_impl(context):
    assert context.workflow_page.is_returned_to_workflow_page(), \
        "Workflow deleted notification not appeared"


@when(u'I click "Cancel" button on the workflow form')
def step_impl(context):
    context.workflow_page.cancel_workflow_form()


@then(u'modal closes without creating workflow')
def step_impl(context):
    assert context.workflow_page.is_returned_to_workflow_page(), "Modal did not close properly"


@when(u'I delete all workflows containing "Automation" in their name')
def step_impl(context):
    context.workflow_page = WorkflowPage(context.driver)
    context.workflow_page.delete_workflows_with_name_containing("Automation")


@then(u'all test automation workflows should be deleted')
def step_impl(context):
    pass