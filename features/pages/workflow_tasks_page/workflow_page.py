from selenium.common import NoSuchElementException

from features.commons.locators import WorkflowPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class WorkflowPage(BasePage):

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
