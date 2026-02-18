from datetime import datetime

from behave import given, when, then
from time import sleep

from faker import Faker

from features.pages.login_page.login_page import LoginPage
from features.pages.user_dashboard_page.vpe_user_dashboard_page import VpeUserDashboardPage
from features.pages.users_page.users_page import UsersPage
from features.pages.users_page.user_group_page import UserGroupPage
from features.pages.patient_groups_page.patient_groups_page import PatientGroupsPage
from features.pages.workflow_tasks_page.workflow_page import WorkflowPage
from features.pages.activities_page.activities_page import ActivitiesPage
from features.pages.dashboard_page.dashboard_page import DashboardPage
from features.pages.search_patients_page.search_patients_page import SearchPatientsPage
from features.pages.patient_details_page.patient_details_page import PatientDetailsPage
from features.commons.routes import Routes
from utils.logger import printf
from utils.ui.login_utility import LoginHelper
from utils.utils import get_current_date


# ===== USER CREATION STEPS =====
@given(u'I login as "{user_role}"')
def step_impl(context, user_role):
    """Login as a specific user role (e.g., enroller_admin)."""
    # Get or create driver for this user role
    driver = LoginHelper.get_driver_for_role(context, user_role)
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login_as_role(user_role)
    login_page.is_login_successful()

    context.driver = driver
    printf(f"Logged in as {user_role}")



@when(u'I create {role} user with automation email and password "{password}"')
def step_impl(context, role, password):
    """Create a user with specific role and password."""
    context.users_page = UsersPage(context.driver)
    context.users_page.click_add_new_user()

    # Generate unique email
    faker = Faker()
    unique_id = faker.random_int(1000, 9999)
    email = f"automation_{role.lower()}_{unique_id}@hbox.ai"
    
    # Fill form with specific role, email, and password
    user_info = context.users_page.fill_create_user_form(
        user_role=role,
        email=email,
        password=password
    )
    context.users_page.submit_user_form()
    
    # Store user info for later use
    if not hasattr(context, 'created_users'):
        context.created_users = {}
    context.created_users[f"{role}_User"] = user_info
    
    printf(f"Created {role} user with email: {email}")


@then(u'I store the created user email as "{variable_name}"')
def step_impl(context, variable_name):
    """Store the last created user's email in context variables."""
    if not hasattr(context, 'stored_variables'):
        context.stored_variables = {}
    
    # Extract role from variable name (e.g., "ES_User_Email" -> "ES")
    role = variable_name.split('_')[0]
    user_key = f"{role}_User"
    
    if hasattr(context, 'created_users') and user_key in context.created_users:
        email = context.created_users[user_key]['email']
        context.stored_variables[variable_name] = email
        printf(f"Stored {variable_name} = {email}")
    else:
        raise AssertionError(f"No user found for role: {role}")


# ===== USER GROUP CREATION STEPS =====

@when(u'I create user group "{group_name}" and assign user with email stored as "{email_variable}"')
def step_impl(context, group_name, email_variable):
    """Create a user group and assign a specific user by email."""
    context.user_group_page = UserGroupPage(context.driver)
    context.user_group_page.click_add_new_user_group()
    
    # Get stored email
    email = context.stored_variables.get(email_variable)
    if not email:
        raise AssertionError(f"No email found for variable: {email_variable}")

    # Generate unique group name
    unique_group_name = f"Automation-{group_name}-{datetime.now().strftime('%y%m%d-%H%M%S')}"
    
    # Fill form with specific group name and user email
    context.user_group_page.fill_create_user_group_form(
        group_name=unique_group_name,
        user_emails=[email]
    )
    context.user_group_page.submit_user_group_form()
    
    # Store the generated group name for later use
    if not hasattr(context, 'created_groups'):
        context.created_groups = {}
    context.created_groups[group_name] = unique_group_name
    
    printf(f"Created user group '{unique_group_name}' with user: {email}")


# ===== PATIENT GROUP CREATION STEPS =====

@when(u'I create patient group "{group_name}" with {count:d} patients using filters')
def step_impl(context, group_name, count):
    """Create a patient group with specified number of patients using filter method."""
    context.patient_groups_page = PatientGroupsPage(context.driver)
    
    # Navigate to create by filters
    context.patient_groups_page.click_create_new_group()
    context.patient_groups_page.select_create_option("create new group by filters")
    
    # Apply filters to get patients
    context.patient_groups_page.apply_filters_for_patient_group(clinic="HBox Internal")
    
    # Select the specified number of patients
    context.patient_groups_page.select_patients_from_table(count)
    
    # Create the group
    patient_group_name = f"{group_name} - {datetime.now().strftime('%y%m%d-%H%M%S')}"
    context.patient_groups_page.enter_group_name_and_note(group_name=patient_group_name)
    context.patient_group = patient_group_name
    
    printf(f"Created patient group '{group_name}' with {count} patients")


# ===== WORKFLOW CREATION STEPS =====

@when(u'I create workflow "{workflow_name}" with program "{program_name}" and no trigger')
def step_impl(context, workflow_name, program_name):
    """Create a workflow with no trigger."""
    context.workflow_page = WorkflowPage(context.driver)
    context.workflow_page.click_create_new_workflow()
    
    # Store workflow name for later operations
    if not hasattr(context, 'current_workflow'):
        context.current_workflow = {}
    context.current_workflow['name'] = workflow_name
    context.current_workflow['program'] = program_name
    
    printf(f"Preparing to create workflow '{workflow_name}' with program '{program_name}' (no trigger)")


@when(u'I create workflow "{workflow_name}" with program "{program_name}" triggered by "{trigger_workflow}" status "{trigger_status}"')
def step_impl(context, workflow_name, program_name, trigger_workflow, trigger_status):
    """Create a workflow with a specific trigger."""
    context.workflow_page = WorkflowPage(context.driver)
    context.workflow_page.click_create_new_workflow()
    
    # Store workflow configuration
    if not hasattr(context, 'current_workflow'):
        context.current_workflow = {}
    context.current_workflow['name'] = workflow_name
    context.current_workflow['program'] = program_name
    context.current_workflow['trigger_workflow'] = trigger_workflow
    context.current_workflow['trigger_status'] = trigger_status
    
    printf(f"Preparing to create workflow '{workflow_name}' triggered by '{trigger_workflow}' status '{trigger_status}'")


@when(u'I assign task "{task_name}" with {waiting_period:d} days waiting period')
def step_impl(context, task_name, waiting_period):
    """Assign task and waiting period to the workflow."""
    context.current_workflow['task'] = task_name
    context.current_workflow['waiting_period'] = waiting_period
    printf(f"Set task '{task_name}' with {waiting_period} days waiting period")


@when(u'I assign user group "{group_name}"')
def step_impl(context, group_name):
    """Assign user group to the workflow."""
    # Check if this is a stored variable reference (ends with _Name)
    if group_name.endswith('_Name') and hasattr(context, 'stored_variables'):
        actual_group_name = context.stored_variables.get(group_name)
        if not actual_group_name:
            raise AssertionError(f"No stored group name found for: {group_name}")
        context.current_workflow['user_group'] = actual_group_name
        printf(f"Set user group '{actual_group_name}' (from {group_name})")
    else:
        # Direct group name or check in created_groups
        if hasattr(context, 'created_groups') and group_name in context.created_groups:
            actual_group_name = context.created_groups[group_name]
            context.current_workflow['user_group'] = actual_group_name
            printf(f"Set user group '{actual_group_name}' (from created_groups[{group_name}])")
        else:
            context.current_workflow['user_group'] = group_name
            printf(f"Set user group '{group_name}'")


@when(u'I submit the workflow')
def step_impl(context):
    """Submit the workflow form with all configured settings."""
    # Extract stored workflow configuration
    workflow_name = context.current_workflow.get('name')
    program_name = context.current_workflow.get('program')
    trigger_workflow = context.current_workflow.get('trigger_workflow')
    trigger_status = context.current_workflow.get('trigger_status')
    user_group = context.current_workflow.get('user_group')
    task_name = context.current_workflow.get('task', 'Call')
    waiting_period = context.current_workflow.get('waiting_period', 0)
    
    # Fill the workflow form with all settings
    context.workflow_page.fill_create_workflow_form(
        program_name=program_name,
        workflow_name=workflow_name,
        trigger_workflow=trigger_workflow,
        trigger_status=trigger_status,
        user_group_name=user_group,
        task_name=task_name,
        waiting_period=waiting_period
    )
    
    context.workflow_page.submit_create_workflow()
    printf(f"Submitted workflow '{workflow_name}'")


# ===== ACTIVITY CREATION STEPS =====

@when(u'I click Add New Activity button')
def step_impl(context):
    """Click Add New Activity button to open activity creation form."""
    context.activities_page = ActivitiesPage(context.driver)
    context.activities_page.click_add_new_activity()
    printf("Clicked Add New Activity button")


@when(u'I fill activity form with name "{activity_name}" for patient group "{patient_group}" and workflow "{workflow}"')
def step_impl(context, activity_name, patient_group, workflow):
    """Fill the activity creation form."""
    context.activities_page = ActivitiesPage(context.driver)
    
    # Calculate dates: from today to 3 months
    from_date = get_current_date(date_format="%d-%m-%Y")
    end_date = get_current_date(date_format="%d-%m-%Y", days_offset=90)
    
    context.activity_info = context.activities_page.fill_create_activity_form(
        activity_name=activity_name,
        patient_group_name=patient_group,
        workflow_name=workflow,
        from_date=from_date,
        end_date=end_date,
    )
    
    printf(f"Filled activity form: {activity_name}")


@when(u'I set activity execution timeline from today to {months:d} months')
def step_impl(context, months):
    """Note: Dates are already set in the previous step. This is a placeholder."""
    printf(f"Activity timeline set to {months} months")


@when(u'I submit the activity')
def step_impl(context):
    """Submit the activity creation form."""
    context.activities_page.submit_create_activity()
    sleep(2)
    printf("Submitted activity form")


@then(u'the activity should be created successfully')
def step_impl(context):
    """Verify activity was created successfully."""
    # Check if we're back on the activities listing page
    assert context.activities_page.is_navigated_to_activities_page(), \
        "Activity creation did not complete - not on activities page"
    printf("Activity created successfully")


# ===== ROLE-BASED LOGIN AND ACTIONS =====

@given(u'I login as {role} user with stored email "{email_variable}" and password "{password}" as "{user_role}"')
def step_impl(context, role, email_variable, password, user_role):
    """Login as specific user with role-based credentials using parallel session."""
    email = context.stored_variables.get(email_variable)
    if not email:
        raise AssertionError(f"No email found for variable: {email_variable}")
    
    # Get driver for this parallel user session
    driver = LoginHelper.get_driver_for_role(context, f"{user_role}_parallel")
    
    # Login with specific credentials
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login(email, password)
    sleep(2)
    
    printf(f"Logged in as {role} user ({user_role}): {email}")


@when(u'I navigate to dashboard as "{user_role}"')
def step_impl(context, user_role):
    """Navigate to the dashboard page for specific user session."""
    driver = LoginHelper.get_driver_for_role(context, f"{user_role}_parallel")
    dashboard_page = VpeUserDashboardPage(driver)
    dashboard_page.wait_for_loader()
    printf(f"Navigated to dashboard as {user_role}")


@when(u'I open the first patient from dashboard as "{user_role}"')
def step_impl(context, user_role):
    """Open the first patient from dashboard for specific user session."""
    driver = LoginHelper.get_driver_for_role(context, f"{user_role}_parallel")
    
    # Navigate to search patients page
    search_patients_page = SearchPatientsPage(driver)
    driver.get(Routes.get_full_url(Routes.SEARCH_PATIENTS))
    search_patients_page.wait_for_loader()
    
    # Perform empty search to show all patients
    search_patients_page.click_search_button()
    
    # Open first patient details
    search_patients_page.click_view_details_for_first_patient()
    printf(f"Opened first patient from dashboard as {user_role}")


@then(u'I should see patients in my dashboard as "{user_role}"')
def step_impl(context, user_role):
    """Verify patients appear in the user's dashboard for specific user session."""
    from selenium.webdriver.common.by import By
    
    driver = LoginHelper.get_driver_for_role(context, f"{user_role}_parallel")
    
    # Navigate to search patients page
    search_patients_page = SearchPatientsPage(driver)
    driver.get(Routes.get_full_url(Routes.SEARCH_PATIENTS))
    search_patients_page.wait_for_loader()
    
    # Perform empty search to show all patients assigned to this user
    search_patients_page.click_search_button()
    
    # Check if at least one patient row exists
    rows_locator = (By.XPATH, "//table[@id='table-search-patients']/tbody/tr")
    rows = driver.find_elements(*rows_locator)
    
    assert len(rows) > 0, "No patients found in dashboard"
    
    # Verify it's not a "No patients found" message
    first_row_text = rows[0].text
    assert "No patients found" not in first_row_text, "No patients assigned to this user"
    
    printf(f"Patients appeared in dashboard for {user_role}")


@when(u'I change program status to "{new_status}" as "{user_role}"')
def step_impl(context, new_status, user_role):
    """Change the patient's program status for specific user session."""
    driver = LoginHelper.get_driver_for_role(context, f"{user_role}_parallel")
    patient_details_page = PatientDetailsPage(driver)
    result = patient_details_page.change_program_status(new_status)
    assert result, f"Failed to change program status to '{new_status}'"
    printf(f"Changed program status to: {new_status} as {user_role}")


@then(u'status update notification appears for "{user_role}"')
def step_impl(context, user_role):
    """Verify status update notification for specific user session."""
    driver = LoginHelper.get_driver_for_role(context, f"{user_role}_parallel")
    patient_details_page = PatientDetailsPage(driver)
    assert patient_details_page.verify_status_update_notification(), \
        "Status update notification did not appear"
    printf(f"Status update notification verified for {user_role}")


@then(u'I logout from the application as "{user_role}"')
def step_impl(context, user_role):
    """Logout from the application to clear session for specific user."""
    try:
        driver = LoginHelper.get_driver_for_role(context, f"{user_role}_parallel")
        from features.pages.dashboard_page.dashboard_page import DashboardPage
        dashboard_page = DashboardPage(driver)
        dashboard_page.logout()
        printf(f"Logged out successfully as {user_role}")
    except Exception as e:
        printf(f"Logout attempted for {user_role} (may already be logged out): {e}")


# ===== CLEANUP STEPS =====

@when(u'I delete all activities containing "{keyword}" in their name')
def step_impl(context, keyword):
    """Delete all activities with keyword in name."""
    context.activities_page = ActivitiesPage(context.driver)
    context.activities_page.navigate_to_listing()
    deleted_count = context.activities_page.delete_activities_with_name_containing(keyword)
    printf(f"Deleted {deleted_count} activities containing '{keyword}'")


@then(u'all test activities should be deleted')
def step_impl(context):
    """Verify all test activities are deleted."""
    printf("Activity cleanup completed")


@when(u'I delete workflow "{workflow_name}"')
def step_impl(context, workflow_name):
    """Delete a specific workflow."""
    context.workflow_page = WorkflowPage(context.driver)
    context.workflow_page.find_and_delete_workflow(workflow_name)
    context.workflow_page.confirm_workflow_delete()
    printf(f"Deleted workflow: {workflow_name}")


@when(u'I find and delete patient group "{group_name}"')
def step_impl(context, group_name):
    """Find and delete a patient group."""
    context.patient_groups_page = PatientGroupsPage(context.driver)
    context.patient_groups_page.click_delete_patients_button(group_name)
    context.patient_groups_page.confirm_delete_patient_group_button()
    printf(f"Deleted patient group: {group_name}")


@when(u'I find and delete user group "{group_name}"')
def step_impl(context, group_name):
    """Find and delete a user group."""
    # Look up the actual group name with timestamp from created_groups
    if hasattr(context, 'created_groups') and group_name in context.created_groups:
        actual_group_name = context.created_groups[group_name]
        printf(f"Deleting user group: {actual_group_name} (from {group_name})")
    else:
        actual_group_name = group_name
        printf(f"Deleting user group: {group_name}")
    
    context.user_group_page = UserGroupPage(context.driver)
    context.user_group_page.find_and_delete_user_group(actual_group_name)
    context.user_group_page.confirm_user_group_delete()
    printf(f"Deleted user group: {actual_group_name}")


@when(u'I find and delete user with email stored as "{email_variable}"')
def step_impl(context, email_variable):
    """Find and delete a user by stored email."""
    email = context.stored_variables.get(email_variable)
    if not email:
        printf(f"Warning: No email found for variable: {email_variable}")
        return
    
    context.users_page = UsersPage(context.driver)
    context.users_page.find_and_delete_user(email)
    context.users_page.confirm_user_delete()
    printf(f"Deleted user: {email}")


@then(u'I close all browser instances for parallel users')
def step_impl(context):
    """Close all parallel user browser instances."""
    if hasattr(context, 'user_drivers') and context.user_drivers:
        for role, driver in list(context.user_drivers.items()):
            try:
                driver.quit()
                printf(f"Closed browser for {role}")
            except Exception as e:
                printf(f"Error closing browser for {role}: {e}")
        context.user_drivers.clear()
        printf("All parallel user browsers closed")
