from selenium.common import NoSuchElementException

from features.commons.locators import WorkflowStatusPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class WorkflowStatusPage(BasePage):

    def navigate_to_tab(self):
        self.click(WorkflowStatusPageLocators.WORKFLOW_STATUS_TAB)
        self.wait_for_loader()

    def get_workflow_status_first_row_data(self):
        self.wait_for_loader()
        return extract_table_row_as_dict(self, WorkflowStatusPageLocators.WORKFLOW_STATUS_TABLE)

    def perform_workflow_status_search_by_field(self, field, value):
        try:
            printf(f"Performing workflow status search for field '{field}' with value '{value}'")
            self.send_keys(WorkflowStatusPageLocators.WORKFLOW_STATUS_SEARCH_INPUT, value)
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
