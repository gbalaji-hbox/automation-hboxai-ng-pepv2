from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException

from features.commons.locators import WorkflowStatusPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class WorkflowStatusPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def navigate_to_tab(self):
        if not self.get_attribute(WorkflowStatusPageLocators.WORKFLOW_STATUS_SEARCH_INPUT, "value") == "":
            self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_CLEAR_BUTTON)
            self.wait_for_loader()

        self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_TAB)
        self.wait_for_loader()

    def get_workflow_status_first_row_data(self):
        self.wait_for_loader()
        return extract_table_row_as_dict(self, WorkflowStatusPageLocators.WORKFLOW_STATUS_TABLE)

    def perform_workflow_status_search_by_field(self, field, value):
        try:
            printf(f"Performing workflow status search for field '{field}' with value '{value}'")
            if self.get_attribute(WorkflowStatusPageLocators.WORKFLOW_STATUS_SEARCH_INPUT, "value") != "":
                self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_CLEAR_BUTTON)
                self.wait_for_loader()

            self.send_keys(WorkflowStatusPageLocators.WORKFLOW_STATUS_SEARCH_INPUT, value)
            sleep(1)
            self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_SEARCH_BUTTON)
            self.wait_for_loader()
            return True
        except NoSuchElementException as e:
            printf(f"Error during workflow status search operation: {e}")
            return False

    def verify_workflow_status_search_results(self, search_criteria, search_value):
        self.wait_for_loader(timeout=10)
        return verify_search_results_in_table(
            self,
            search_value,
            WorkflowStatusPageLocators.WORKFLOW_STATUS_TABLE_ROWS,
            search_criteria
        )

    def click_on_workflow_status_action_button(self, action_button):
        self.wait_for_loader()
        if action_button == "View History":
            self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_HISTORY_BUTTON)
        elif action_button == "Edit":
            self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_EDIT_BUTTON)
        elif action_button == "Delete":
            self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_DELETE_BUTTON)
        else:
            raise AssertionError(f"Action button '{action_button}' not recognized.")

    def verify_workflow_status_operation_history_dialog(self):
        try:
            self.is_element_visible(WorkflowStatusPageLocators.OPERATION_HISTORY_DIALOG, timeout=5)
            self.click(WorkflowStatusPageLocators.OPERATION_HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException:
            return False

    def is_navigated_to_workflow_status_edit_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.WORKFLOW_STATUS_EDIT, partial=False)

    def verify_workflow_status_delete_confirmation_dialog(self):
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(WorkflowStatusPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=5)
            self.click(WorkflowStatusPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def select_workflow_status_records_per_page(self, records):
        self.custom_select_by_locator(
            WorkflowStatusPageLocators.PAGE_LIMIT_DROPDOWN,
            WorkflowStatusPageLocators.DROPDOWN_OPTION(records)
        )

    def verify_workflow_status_records_per_page(self, records):
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(WorkflowStatusPageLocators.WORKFLOW_STATUS_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying workflow status rows per page: {e}")
            return False

    def click_add_new_workflow_status(self):
        self.click(WorkflowStatusPageLocators.ADD_NEW_WORKFLOW_STATUS_BUTTON)
        self.is_clickable(WorkflowStatusPageLocators.WORKFLOW_STATUS_NAME_INPUT)
        self.wait_for_dom_stability()

    def fill_create_workflow_status_form(self):
        workflow_status_name = f"Automation Workflow Status {self.faker.word().capitalize()}"
        self.send_keys(WorkflowStatusPageLocators.WORKFLOW_STATUS_NAME_INPUT, workflow_status_name)
        return workflow_status_name

    def submit_create_workflow_status(self):
        self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_SAVE_BUTTON)

    def find_and_edit_workflow_status(self, workflow_status_name):
        try:
            printf(f"Finding workflow status with name '{workflow_status_name}' to edit")
            self.wait_for_loader()
            self.perform_workflow_status_search_by_field("Workflow Status Name", workflow_status_name)
            self.wait_for_loader()
            self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_EDIT_BUTTON_BY_NAME(workflow_status_name))
            self.wait_for_dom_stability()
        except NoSuchElementException as e:
            printf(f"Error finding workflow status '{workflow_status_name}' for editing: {e}")
            raise

    def update_workflow_status_name(self, suffix):
        current_name = self.get_attribute(WorkflowStatusPageLocators.WORKFLOW_STATUS_NAME_INPUT, "value")
        edited_name = f"{current_name} {suffix}".strip()
        self.react_clear(WorkflowStatusPageLocators.WORKFLOW_STATUS_NAME_INPUT)
        self.send_keys(WorkflowStatusPageLocators.WORKFLOW_STATUS_NAME_INPUT, edited_name)
        return edited_name

    def submit_update_workflow_status(self):
        self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_UPDATE_BUTTON)

    def cancel_workflow_status_form(self):
        self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_CANCEL_BUTTON)
        self.wait_for_dom_stability()

    def find_and_delete_workflow_status(self, workflow_status_name):
        self.wait_for_loader()
        self.perform_workflow_status_search_by_field("Workflow Status Name", workflow_status_name)
        self.wait_for_loader()
        self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_DELETE_BUTTON_BY_NAME(workflow_status_name))

    def confirm_workflow_status_delete(self):
        self.click(WorkflowStatusPageLocators.DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON)

    def check_workflow_status_notification(self, expected_message):
        message = expected_message.lower()
        if "created" in message:
            locator = WorkflowStatusPageLocators.WORKFLOW_STATUS_CREATED_NOTIFICATION
        elif "updated" in message:
            locator = WorkflowStatusPageLocators.WORKFLOW_STATUS_UPDATED_NOTIFICATION
        elif "deleted" in message:
            locator = WorkflowStatusPageLocators.WORKFLOW_STATUS_DELETED_NOTIFICATION
        else:
            return False

        return self.is_element_visible(locator, timeout=15)

    def is_navigated_to_workflow_tasks_page(self):
        self.wait_for_loader(loader_locators=WorkflowStatusPageLocators.DELETE_CONFIRMATION_DIALOG)
        return self.check_url_contains(Routes.WORKFLOW_TASKS, partial=False)

    def is_workflow_status_present_in_table(self, workflow_status_name):
        row_locator = (
            "xpath",
            f"//table[.//th[normalize-space()='Workflow Status Name']]//tbody//tr[td[1][normalize-space()='{workflow_status_name}']]",
        )
        return self.is_element_visible(row_locator, timeout=3)

    def has_workflow_status_with_name_containing(self, substring):
        rows = self.find_elements(WorkflowStatusPageLocators.WORKFLOW_STATUS_TABLE_ROWS)
        if not rows:
            return False

        for row in rows:
            row_name = row.find_element("xpath", "./td[1]").text.strip()
            if substring.lower() in row_name.lower():
                return True
        return False

    def delete_workflow_statuses_with_name_containing(self, substring):
        try:
            deleted_count = 0
            for iteration in range(1, 11):
                printf(f"Iteration {iteration}: Searching for workflow statuses containing '{substring}' in name")
                rows = self._perform_workflow_status_search_and_get_rows(substring)
                if rows is None:
                    break

                if self._delete_first_matching_workflow_status_by_name(rows, substring):
                    deleted_count += 1
                    printf(f" (#{deleted_count})")
                else:
                    printf(f"No workflow status with name containing '{substring}' found in current results - stopping")
                    break

                if iteration == 10:
                    printf("Reached maximum iterations (10) - stopping to prevent infinite loop")

            return deleted_count
        except Exception as e:
            printf(f"Error in workflow status cleanup for substring '{substring}': {e}")
            return 0

    def _perform_workflow_status_search_and_get_rows(self, substring):
        try:
            self.navigate_to_tab()
            if self.is_element_visible(WorkflowStatusPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=2):
                self.click(WorkflowStatusPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)

            self.wait_for_loader()
            self.perform_workflow_status_search_by_field("Workflow Status Name", substring)
            self.wait_for_loader(timeout=30)

            rows = self.find_elements(WorkflowStatusPageLocators.WORKFLOW_STATUS_TABLE_ROWS)
            if not rows:
                printf(f"No workflow statuses found containing '{substring}' in name - cleanup complete")
                return None

            first_row_text = rows[0].text.strip()
            if "No workflow statuses found" in first_row_text or first_row_text == "":
                printf(f"No workflow statuses found containing '{substring}' in name - cleanup complete")
                return None

            return rows
        except Exception as e:
            printf(f"Error while searching workflow statuses for cleanup: {e}")
            return None

    def _delete_first_matching_workflow_status_by_name(self, rows, substring):
        try:
            for row in rows:
                name_cell = row.find_element("xpath", ".//td[1]")
                workflow_status_name = name_cell.text.strip()
                if substring.lower() in workflow_status_name.lower():
                    delete_button = row.find_element("xpath", ".//td[last()]//button[contains(@id,'delete')]")
                    delete_button.click()
                    self.wait_for_dom_stability()
                    self.click(WorkflowStatusPageLocators.DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON)
                    self.wait_for_loader(loader_locators=WorkflowStatusPageLocators.DELETE_CONFIRMATION_DIALOG)
                    printf(f"Successfully deleted workflow status '{workflow_status_name}'")
                    return True

            return False
        except Exception as e:
            printf(f"Error deleting workflow status: {e}")
            return False
