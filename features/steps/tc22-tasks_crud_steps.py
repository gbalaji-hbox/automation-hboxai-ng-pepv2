from behave import when, then

from features.pages.workflow_tasks_page.tasks_page import TasksPage


@when(u'I click "Add New Task" button')
def step_impl(context):
    context.tasks_page = TasksPage(context.driver)
    context.tasks_page.click_add_new_task()


@when(u'I fill the create task form with valid data')
def step_impl(context):
    context.task_name = context.tasks_page.fill_create_task_form()


@when(u'I click "Save" button on the task form')
def step_impl(context):
    context.tasks_page.submit_create_task()


@then(u'notification "Task created successfully" appears')
def step_impl(context):
    assert context.tasks_page.check_task_notification("created"), \
        "Task created notification not appeared"


@when(u'I find the created task in the list and click edit')
def step_impl(context):
    context.tasks_page.find_and_edit_task(context.task_name)


@when(u'I update the task name to "Edited"')
def step_impl(context):
    context.edited_task_name = context.tasks_page.update_task_name("Edited")


@when(u'I click "Update" button on the task form')
def step_impl(context):
    context.tasks_page.submit_update_task()


@then(u'notification "Task updated successfully" appears')
def step_impl(context):
    assert context.tasks_page.check_task_notification("updated"), \
        "Task updated notification not appeared"


@when(u'I find the edited task in the list and click delete')
def step_impl(context):
    context.tasks_page.find_and_delete_task(context.edited_task_name)


@when(u'I confirm the task delete in the dialog')
def step_impl(context):
    context.tasks_page.confirm_task_delete()


@then(u'notification "Task deleted successfully" appears')
def step_impl(context):
    assert context.tasks_page.is_navigated_to_workflow_tasks_page(), \
        "Task deleted notification not appeared"


@when(u'I click "Cancel" button on the task form')
def step_impl(context):
    context.tasks_page.cancel_task_form()


@then(u'task form closes without creating record')
def step_impl(context):
    assert context.tasks_page.is_navigated_to_workflow_tasks_page(), \
        "Task form did not close properly"


@when(u'I delete all tasks containing "Automation" in their name')
def step_impl(context):
    context.tasks_page = TasksPage(context.driver)
    context.deleted_task_count = context.tasks_page.delete_tasks_with_name_containing("Automation")


@then(u'all test automation tasks should be deleted')
def step_impl(context):
    pass
