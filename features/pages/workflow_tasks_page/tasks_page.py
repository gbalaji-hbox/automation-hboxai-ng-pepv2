from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException

from features.commons.locators import TasksPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class TasksPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

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
            self.wait_for_loader()
            self.send_keys(TasksPageLocators.TASKS_SEARCH_INPUT, value)
            sleep(1)
            self.click(TasksPageLocators.TASKS_SEARCH_BUTTON)
            self.wait_for_loader(timeout=30)
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

    def click_add_new_task(self):
        self.click(TasksPageLocators.ADD_NEW_TASK_BUTTON)
        self.is_clickable(TasksPageLocators.TASK_NAME_INPUT)
        self.wait_for_dom_stability()

    def fill_create_task_form(self):
        task_name = f"Automation Task {self.faker.word().capitalize()}"
        self.send_keys(TasksPageLocators.TASK_NAME_INPUT, task_name)
        return task_name

    def submit_create_task(self):
        self.click(TasksPageLocators.TASK_SAVE_BUTTON)

    def find_and_edit_task(self, task_name):
        self.perform_tasks_search_by_field("Task Name", task_name)
        self.wait_for_loader()
        self.click(TasksPageLocators.TASK_EDIT_BUTTON_BY_NAME(task_name))
        self.wait_for_dom_stability()

    def update_task_name(self, suffix):
        current_name = self.get_attribute(TasksPageLocators.TASK_NAME_INPUT, "value")
        edited_name = f"{current_name} {suffix}".strip()
        self.react_clear(TasksPageLocators.TASK_NAME_INPUT)
        self.send_keys(TasksPageLocators.TASK_NAME_INPUT, edited_name)
        return edited_name

    def submit_update_task(self):
        self.click(TasksPageLocators.TASK_UPDATE_BUTTON)

    def cancel_task_form(self):
        self.click(TasksPageLocators.TASK_CANCEL_BUTTON)
        self.wait_for_dom_stability()

    def find_and_delete_task(self, task_name):
        self.perform_tasks_search_by_field("Task Name", task_name)
        self.wait_for_loader()
        self.click(TasksPageLocators.TASK_DELETE_BUTTON_BY_NAME(task_name))

    def confirm_task_delete(self):
        self.click(TasksPageLocators.DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON)

    def check_task_notification(self, expected_message):
        message = expected_message.lower()
        if "created" in message:
            locator = TasksPageLocators.TASK_CREATED_NOTIFICATION
        elif "updated" in message:
            locator = TasksPageLocators.TASK_UPDATED_NOTIFICATION
        elif "deleted" in message:
            locator = TasksPageLocators.TASK_DELETED_NOTIFICATION
        else:
            return False

        return self.is_element_visible(locator, timeout=15)

    def is_navigated_to_workflow_tasks_page(self):
        self.wait_for_loader(loader_locators=TasksPageLocators.DELETE_CONFIRMATION_DIALOG)
        return self.check_url_contains(Routes.WORKFLOW_TASKS, partial=False)

    def is_task_present_in_table(self, task_name):
        row_locator = (
            "xpath",
            f"//table[.//th[normalize-space()='Task Name']]//tbody//tr[td[1][normalize-space()='{task_name}']]",
        )
        return self.is_element_visible(row_locator, timeout=3)

    def has_task_with_name_containing(self, substring):
        rows = self.find_elements(TasksPageLocators.TASKS_TABLE_ROWS)
        if not rows:
            return False

        for row in rows:
            row_name = row.find_element("xpath", "./td[1]").text.strip()
            if substring.lower() in row_name.lower():
                return True
        return False

    def delete_tasks_with_name_containing(self, substring):
        try:
            deleted_count = 0
            for iteration in range(1, 11):
                printf(f"Iteration {iteration}: Searching for tasks containing '{substring}' in name")
                rows = self._perform_tasks_search_and_get_rows(substring)
                if rows is None:
                    break

                if self._delete_first_matching_task_by_name(rows, substring):
                    deleted_count += 1
                    printf(f" (#{deleted_count})")
                else:
                    printf(f"No task with name containing '{substring}' found in current results - stopping")
                    break

                if iteration == 10:
                    printf("Reached maximum iterations (10) - stopping to prevent infinite loop")

            return deleted_count
        except Exception as e:
            printf(f"Error in task cleanup for substring '{substring}': {e}")
            return 0

    def _perform_tasks_search_and_get_rows(self, substring):
        try:
            self.navigate_to_tab()
            if self.is_element_visible(TasksPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=2):
                self.click(TasksPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)

            self.wait_for_loader()
            self.perform_tasks_search_by_field("Task Name", substring)
            self.wait_for_loader(timeout=30)

            rows = self.find_elements(TasksPageLocators.TASKS_TABLE_ROWS)
            if not rows:
                printf(f"No tasks found containing '{substring}' in name - cleanup complete")
                return None

            first_row_text = rows[0].text.strip()
            if "No tasks found" in first_row_text or first_row_text == "":
                printf(f"No tasks found containing '{substring}' in name - cleanup complete")
                return None

            return rows
        except Exception as e:
            printf(f"Error while searching tasks for cleanup: {e}")
            return None

    def _delete_first_matching_task_by_name(self, rows, substring):
        try:
            for row in rows:
                name_cell = row.find_element("xpath", ".//td[1]")
                task_name = name_cell.text.strip()
                if substring.lower() in task_name.lower():
                    delete_button = row.find_element("xpath", ".//td[last()]//button[contains(@id,'delete')]")
                    delete_button.click()
                    self.wait_for_dom_stability()
                    self.click(TasksPageLocators.DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON)
                    self.wait_for_loader(loader_locators=TasksPageLocators.DELETE_CONFIRMATION_DIALOG)
                    printf(f"Successfully deleted task '{task_name}'")
                    return True

            return False
        except Exception as e:
            printf(f"Error deleting task: {e}")
            return False
