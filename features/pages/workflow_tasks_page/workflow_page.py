from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException

from features.commons.locators import WorkflowPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class WorkflowPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def navigate_to_tab(self):
        if not self.get_attribute(WorkflowPageLocators.WORKFLOW_SEARCH_INPUT, "value") == "":
            self.refresh_page()
            self.wait_for_loader(timeout=10)

        self.click(WorkflowPageLocators.WORKFLOW_TAB)
        self.wait_for_loader()

    def get_workflow_first_row_data(self):
        self.wait_for_loader()
        return extract_table_row_as_dict(self, WorkflowPageLocators.WORKFLOW_TABLE)

    def perform_workflow_search_by_field(self, field, value):
        try:
            printf(f"Performing workflow search for field '{field}' with value '{value}'")
            self.wait_for_loader()
            self.click(WorkflowPageLocators.WORKFLOW_SEARCH_DROPDOWN)
            self.click(WorkflowPageLocators.DROPDOWN_OPTION(field))
            if field == "Assigned User Group":
                self.custom_select_by_locator(
                    WorkflowPageLocators.WORKFLOW_ASSIGNED_GROUP_DROPDOWN,
                    WorkflowPageLocators.WORKFLOW_ASSIGNED_GROUP_OPTION(value)
                )
            else:
                self.send_keys(WorkflowPageLocators.WORKFLOW_SEARCH_INPUT, value)
                self.click(WorkflowPageLocators.WORKFLOW_SEARCH_BUTTON)
            self.wait_for_loader()
            return True
        except NoSuchElementException as e:
            printf(f"Error during workflow search operation: {e}")
            return False

    def verify_workflow_search_results(self, search_criteria, search_value):
        self.wait_for_loader(timeout=10)
        return verify_search_results_in_table(
            self,
            search_value,
            WorkflowPageLocators.WORKFLOW_TABLE_ROWS,
            search_criteria
        )

    def click_on_workflow_action_button(self, action_button):
        self.wait_for_loader()
        if action_button == "View History":
            self.click(WorkflowPageLocators.WORKFLOW_HISTORY_BUTTON)
        elif action_button == "Edit":
            self.click(WorkflowPageLocators.WORKFLOW_EDIT_BUTTON)
        elif action_button == "Delete":
            self.click(WorkflowPageLocators.WORKFLOW_DELETE_BUTTON)
        else:
            raise AssertionError(f"Action button '{action_button}' not recognized.")

    def verify_workflow_operation_history_dialog(self):
        try:
            self.is_element_visible(WorkflowPageLocators.OPERATION_HISTORY_DIALOG, timeout=5)
            self.click(WorkflowPageLocators.OPERATION_HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException:
            return False

    def is_navigated_to_workflow_edit_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.WORKFLOW_EDIT, partial=False)

    def verify_workflow_delete_confirmation_dialog(self):
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(WorkflowPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=5)
            self.click(WorkflowPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def select_workflow_records_per_page(self, records):
        self.custom_select_by_locator(
            WorkflowPageLocators.PAGE_LIMIT_DROPDOWN,
            WorkflowPageLocators.DROPDOWN_OPTION(records)
        )

    def verify_workflow_records_per_page(self, records):
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(WorkflowPageLocators.WORKFLOW_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying workflow rows per page: {e}")
            return False

    def click_create_new_workflow(self):
        try:
            self.click(WorkflowPageLocators.CREATE_NEW_WORKFLOW_BUTTON)
            self.is_clickable(WorkflowPageLocators.APPLICABLE_PROGRAMS_DROPDOWN)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException as e:
            printf(f"Create New Workflow button not found: {e}")
            return False

    def _select_first_dropdown_option(self, dropdown_locator):
        try:
            self.click(dropdown_locator)
            option = self.find_element(WorkflowPageLocators.DROPDOWN_FIRST_OPTION)
            option_text = option.text.strip()
            option.click()
            sleep(1)
            self.wait_for_dom_stability()
            if self.is_element_visible(WorkflowPageLocators.DROPDOWN_FIRST_OPTION):
                printf("First option still visible after selection, attempting to click dropdown again to close it")
                self.click(dropdown_locator)
                sleep(1)
            return option_text
        except NoSuchElementException as e:
            printf(f"Failed selecting first option for dropdown {dropdown_locator}: {e}")
            return None
            
    def _select_dropdown_option_by_text(self, dropdown_locator, option_text, option2 = False):
        """Select a specific dropdown option by its text value.
        
        Args:
            dropdown_locator: The locator for the dropdown button.
            option_text: The text of the option to select.
            
        Returns:
            The text of the selected option or None if not found.
        """
        try:
            self.click(dropdown_locator)
            sleep(1)
            self.wait_for_dom_stability()
            if option2:
                option_locator = WorkflowPageLocators.APPLICABLE_PROGRAM_OPTION(option_text)
            else:
                option_locator = WorkflowPageLocators.DROPDOWN_OPTION(option_text)

            self.click(option_locator)
            sleep(1)
            self.wait_for_dom_stability()
            if self.is_element_visible(WorkflowPageLocators.DROPDOWN_FIRST_OPTION):
                printf("First option still visible after selection, attempting to click dropdown again to close it")
                self.click(dropdown_locator)
                sleep(1)
            printf(f"Selected dropdown option: {option_text}")
            return option_text
        except NoSuchElementException as e:
            printf(f"Failed selecting dropdown option '{option_text}': {e}")
            return None

    def fill_create_workflow_form(self, program_name=None, workflow_name=None, trigger_workflow=None, trigger_status=None, user_group_name=None, task_name="Call", waiting_period=0):
        """Fill the create workflow form with optional specific values.
        
        Args:
            program_name: Optional specific program name (e.g., 'CCM'). If None, selects first.
            workflow_name: Optional workflow name. If None, generates automation name.
            trigger_workflow: Optional trigger workflow name. If None, selects first or removes trigger.
            trigger_status: Optional trigger status name. If None, selects first or removes trigger.
            user_group_name: Optional user group name. If None, selects first.
            task_name: Task name (default: 'Call').
            waiting_period: Waiting period in days (default: 0).
            
        Returns:
            dict: Workflow information including all settings.
        """
        try:
            if workflow_name is None:
                workflow_name = f"Automation Workflow {self.faker.word().capitalize()}"
            self.send_keys(WorkflowPageLocators.WORKFLOW_NAME_INPUT, workflow_name)

            # Select program
            if program_name:
                program = self._select_dropdown_option_by_text(WorkflowPageLocators.APPLICABLE_PROGRAMS_DROPDOWN, program_name, option2=True)
            else:
                program = self._select_first_dropdown_option(WorkflowPageLocators.APPLICABLE_PROGRAMS_DROPDOWN)
            
            # Handle trigger configuration
            if trigger_workflow is None and trigger_status is None:
                # No trigger - remove trigger rows
                printf("No trigger specified - removing trigger rows")
                self.remove_all_trigger_rows()
                trigger_workflow_result = None
                trigger_status_result = None
            else:
                # Select trigger workflow and status
                if trigger_workflow:
                    trigger_workflow_result = self._select_dropdown_option_by_text(WorkflowPageLocators.TRIGGER_WORKFLOW_DROPDOWN, trigger_workflow, option2=True)
                else:
                    trigger_workflow_result = self._select_first_dropdown_option(WorkflowPageLocators.TRIGGER_WORKFLOW_DROPDOWN)
                
                if trigger_status:
                    trigger_status_result = self._select_dropdown_option_by_text(WorkflowPageLocators.TRIGGER_STATUS_DROPDOWN, trigger_status, option2=True)
                else:
                    trigger_status_result = self._select_first_dropdown_option(WorkflowPageLocators.TRIGGER_STATUS_DROPDOWN)

            # Set task and waiting period
            self.select_task_and_waiting_period(task_name, waiting_period)
            self.add_and_remove_additional_attempt()

            # Select user group
            if user_group_name:
                self.click(WorkflowPageLocators.USER_GROUP_DROPDOWN)
                sleep(0.3)
                self.send_keys(WorkflowPageLocators.USER_GROUP_OPTION_SEARCH_INPUT, user_group_name)
                sleep(0.5)
                self.click(WorkflowPageLocators.APPLICABLE_PROGRAM_OPTION(user_group_name))
                sleep(0.3)
                self.click(WorkflowPageLocators.USER_GROUP_DROPDOWN)
                user_group = user_group_name
            else:
                user_group = self._select_first_dropdown_option(WorkflowPageLocators.USER_GROUP_DROPDOWN)

            printf(f"Filled workflow form: Name={workflow_name}, Program={program}, Trigger Workflow={trigger_workflow_result}, Trigger Status={trigger_status_result}, User Group={user_group}")
            
            return {
                "name": workflow_name,
                "program": program,
                "trigger_workflow": trigger_workflow_result,
                "trigger_status": trigger_status_result,
                "task": task_name,
                "waiting_period": waiting_period,
                "user_group": user_group,
            }
        except NoSuchElementException as e:
            printf(f"Error filling create workflow form: {e}")
            raise
            
    def remove_all_trigger_rows(self):
        """Remove all trigger rows from the workflow form."""
        try:
            # Try to remove trigger rows while they exist
            for _ in range(5):  # Safety limit
                if self.is_element_visible(WorkflowPageLocators.TRIGGER_ROW_DELETE_BUTTON, timeout=1):
                    self.click(WorkflowPageLocators.TRIGGER_ROW_DELETE_BUTTON)
                    self.wait_for_dom_stability()
                    sleep(0.5)
                else:
                    break
            printf("Removed all trigger rows")
            return True
        except Exception as e:
            printf(f"Error removing trigger rows: {e}")
            return False

    def add_and_remove_additional_trigger(self):
        try:
            self.click(WorkflowPageLocators.ADD_TRIGGER_BUTTON)
            self.wait_for_dom_stability()
            if self.is_element_visible(WorkflowPageLocators.SECOND_TRIGGER_ROW_DELETE_BUTTON, timeout=2):
                self.click(WorkflowPageLocators.SECOND_TRIGGER_ROW_DELETE_BUTTON)
            return True
        except NoSuchElementException as e:
            printf(f"Error adding/removing additional trigger: {e}")
            return False

    def select_task_and_waiting_period(self, task_name, waiting_period):
        try:
            self.click(WorkflowPageLocators.ATTEMPT_TASK_DROPDOWN)
            self.click(WorkflowPageLocators.ATTEMPT_TASK_OPTION(task_name))
            self.clear_field(WorkflowPageLocators.ATTEMPT_WAITING_PERIOD_INPUT)
            self.send_keys(WorkflowPageLocators.ATTEMPT_WAITING_PERIOD_INPUT, str(waiting_period))
            return True
        except NoSuchElementException as e:
            printf(f"Error setting task and waiting period: {e}")
            return False

    def add_and_remove_additional_attempt(self):
        try:
            self.click(WorkflowPageLocators.ADD_ATTEMPT_BUTTON)
            self.wait_for_dom_stability()
            if self.is_element_visible(WorkflowPageLocators.SECOND_ATTEMPT_DELETE_BUTTON, timeout=2):
                self.click(WorkflowPageLocators.SECOND_ATTEMPT_DELETE_BUTTON)
            return True
        except NoSuchElementException as e:
            printf(f"Error adding/removing additional attempt: {e}")
            return False

    def submit_create_workflow(self):
        try:
            self.click(WorkflowPageLocators.CREATE_WORKFLOW_BUTTON)
            return True
        except NoSuchElementException as e:
            printf(f"Error submitting create workflow: {e}")
            return False

    def update_workflow_name(self, suffix):
        try:
            current_name = self.get_attribute(WorkflowPageLocators.WORKFLOW_NAME_INPUT, "value")
            new_name = f"{current_name} {suffix}".strip()
            self.react_clear(WorkflowPageLocators.WORKFLOW_NAME_INPUT)
            self.send_keys(WorkflowPageLocators.WORKFLOW_NAME_INPUT, new_name)
            return new_name
        except NoSuchElementException as e:
            printf(f"Error updating workflow name: {e}")
            raise

    def remove_trigger_row(self):
        try:
            self.click(WorkflowPageLocators.TRIGGER_ROW_DELETE_BUTTON)
            self.wait_for_dom_stability()
            if self.is_element_visible(WorkflowPageLocators.TRIGGER_ROW_DELETE_BUTTON, timeout=2):
                self.click(WorkflowPageLocators.TRIGGER_ROW_DELETE_BUTTON)
            return True
        except NoSuchElementException as e:
            printf(f"Error removing trigger row: {e}")
            return False

    def submit_update_workflow(self):
        try:
            self.click(WorkflowPageLocators.UPDATE_WORKFLOW_BUTTON)
            return True
        except NoSuchElementException as e:
            printf(f"Error submitting update workflow: {e}")
            return False

    def cancel_workflow_form(self):
        try:
            self.click(WorkflowPageLocators.WORKFLOW_CANCEL_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException as e:
            printf(f"Error cancelling workflow form: {e}")
            return False

    def check_workflow_notification(self, expected_message):
        try:
            message = expected_message.lower()
            if "created" in message:
                locator = WorkflowPageLocators.WORKFLOW_CREATED_NOTIFICATION
            elif "updated" in message:
                locator = WorkflowPageLocators.WORKFLOW_UPDATED_NOTIFICATION
            elif "deleted" in message:
                locator = WorkflowPageLocators.WORKFLOW_DELETED_NOTIFICATION
            else:
                printf(f"Unknown workflow notification type: {expected_message}")
                return False

            return self.is_element_visible(locator, timeout=15)
        except NoSuchElementException:
            return False

    def find_and_edit_workflow(self, workflow_name):
        try:
            self.wait_for_loader()
            self.perform_workflow_search_by_field("Workflow Name", workflow_name)
            self.wait_for_loader()
            self.click(WorkflowPageLocators.WORKFLOW_EDIT_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException as e:
            printf(f"Error finding/editing workflow '{workflow_name}': {e}")
            raise

    def find_and_delete_workflow(self, workflow_name):
        try:
            self.wait_for_loader()
            self.perform_workflow_search_by_field("Workflow Name", workflow_name)
            self.wait_for_loader()
            self.click(WorkflowPageLocators.WORKFLOW_DELETE_BUTTON)
            return True
        except NoSuchElementException as e:
            printf(f"Error finding/deleting workflow '{workflow_name}': {e}")
            raise

    def confirm_workflow_delete(self):
        try:
            self.click(WorkflowPageLocators.DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON)
            self.wait_for_loader(loader_locators=WorkflowPageLocators.DELETE_CONFIRMATION_DIALOG)
            return True
        except NoSuchElementException as e:
            printf(f"Error confirming workflow deletion: {e}")
            raise

    def delete_workflows_with_name_containing(self, substring):
        deleted_count = 0
        for iteration in range(1, 11):
            printf(f"Iteration {iteration}: Searching for workflows containing '{substring}' in name")
            rows = self._perform_workflow_search_and_get_rows(substring)
            if rows is None:
                break
            if self._delete_first_matching_workflow_by_name(rows, substring):
                deleted_count += 1
                printf(f" (#{deleted_count})")
            else:
                printf(f"No workflow with name containing '{substring}' found in current results - stopping")
                break
            if iteration == 10:
                printf("Reached maximum iterations (10) - stopping to prevent infinite loop")
        return deleted_count

    def _perform_workflow_search_and_get_rows(self, substring):
        if self.is_element_visible(WorkflowPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=2):
            self.click(WorkflowPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)

        self.perform_workflow_search_by_field("Workflow Name", substring)

        try:
            self.wait_for_loader()
            no_data_element = self.is_element_visible(WorkflowPageLocators.WORKFLOW_TABLE_ROWS, timeout=2)
            if not no_data_element:
                printf(f"No workflows found containing '{substring}' in name - cleanup complete")
                return None
        except Exception as e:
            printf(f"Error checking for no data element: {e}")
            return None

        rows = self.find_elements(WorkflowPageLocators.WORKFLOW_TABLE_ROWS)
        if not rows:
            printf("No workflow table rows found - cleanup complete")
            return None

        first_row_text = rows[0].text.strip()
        if "No workflows found" in first_row_text or first_row_text == "":
            printf(f"No workflows found containing '{substring}' in name - cleanup complete")
            return None

        return rows

    def _delete_first_matching_workflow_by_name(self, rows, substring):
        try:
            for row in rows:
                name_cell = row.find_element("xpath", ".//td[1]")
                workflow_name = name_cell.text.strip()
                if substring.lower() in workflow_name.lower():
                    delete_button = row.find_element("xpath", ".//td[last()]//button[contains(@id,'delete')]")
                    delete_button.click()
                    self.wait_for_dom_stability()
                    self.click(WorkflowPageLocators.DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON)
                    self.wait_for_loader(loader_locators=WorkflowPageLocators.DELETE_CONFIRMATION_DIALOG)
                    printf(f"Successfully deleted workflow '{workflow_name}'")
                    return True
            return False
        except Exception as e:
            printf(f"Error deleting workflow: {e}")
            return False

    def is_returned_to_workflow_page(self):
        return self.check_url_contains(Routes.WORKFLOW_TASKS, partial=False)
