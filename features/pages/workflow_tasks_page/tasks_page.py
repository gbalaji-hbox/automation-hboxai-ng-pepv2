from time import sleep

from selenium.common import NoSuchElementException

from features.commons.locators import TasksPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class TasksPage(BasePage):

    def navigate_to_tab(self):
        if not self.get_attribute(TasksPageLocators.TASKS_SEARCH_INPUT, "value") == "":
            self.click(TasksPageLocators.TASK_CLEAR_BUTTON)
            self.wait_for_loader(timeout=10)

        self.click(TasksPageLocators.TASKS_TAB)
        self.wait_for_loader()

    def get_tasks_first_row_data(self):
        self.wait_for_loader()
        return extract_table_row_as_dict(self, TasksPageLocators.TASKS_TABLE)

    def perform_tasks_search_by_field(self, field, value):
        try:
            printf(f"Performing tasks search for field '{field}' with value '{value}'")
            self.send_keys(TasksPageLocators.TASKS_SEARCH_INPUT, value)
            sleep(1)
            self.click(TasksPageLocators.TASKS_SEARCH_BUTTON)
            self.wait_for_loader()
            return True
        except NoSuchElementException as e:
            printf(f"Error during tasks search operation: {e}")
            return False

    def verify_tasks_search_results(self, search_criteria, search_value):
        self.wait_for_loader(timeout=10)
        return verify_search_results_in_table(
            self,
            search_value,
            TasksPageLocators.TASKS_TABLE_ROWS,
            search_criteria
        )

    def click_on_tasks_action_button(self, action_button):
        self.wait_for_loader()
        if action_button == "View History":
            self.click(TasksPageLocators.TASKS_HISTORY_BUTTON)
        elif action_button == "Edit":
            self.click(TasksPageLocators.TASKS_EDIT_BUTTON)
        elif action_button == "Delete":
            self.click(TasksPageLocators.TASKS_DELETE_BUTTON)
        else:
            raise AssertionError(f"Action button '{action_button}' not recognized.")

    def verify_tasks_operation_history_dialog(self):
        try:
            self.is_element_visible(TasksPageLocators.OPERATION_HISTORY_DIALOG, timeout=5)
            self.click(TasksPageLocators.OPERATION_HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException:
            return False

    def is_navigated_to_task_edit_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.TASK_EDIT, partial=False)

    def verify_task_delete_confirmation_dialog(self):
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(TasksPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=5)
            self.click(TasksPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def select_tasks_records_per_page(self, records):
        self.custom_select_by_locator(
            TasksPageLocators.PAGE_LIMIT_DROPDOWN,
            TasksPageLocators.DROPDOWN_OPTION(records)
        )

    def verify_tasks_records_per_page(self, records):
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(TasksPageLocators.TASKS_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying tasks rows per page: {e}")
            return False
