from time import sleep

from selenium.common import NoSuchElementException

from features.commons.locators import ActivitiesPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class ActivitiesPage(BasePage):
    """Page object for Activities listing and operations."""

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_listing(self):
        self.wait_for_loader()
        if self.is_element_visible(ActivitiesPageLocators.CLEAR_BUTTON, timeout=2):
            self.click(ActivitiesPageLocators.CLEAR_BUTTON)
            self.wait_for_loader()
            self.is_element_visible(ActivitiesPageLocators.DELETE_BUTTON, timeout=30)

    def get_activities_first_row_data(self):
        self.wait_for_loader()
        self.is_element_visible(ActivitiesPageLocators.DELETE_BUTTON, timeout=30)
        return extract_table_row_as_dict(self, ActivitiesPageLocators.ACTIVITIES_TABLE)

    def perform_activities_search_by_field(self, field, value):
        try:
            printf(f"Performing activities search for field '{field}' with value '{value}'")
            self.wait_for_loader()
            if self.is_element_visible(ActivitiesPageLocators.CLEAR_BUTTON, timeout=2):
                self.click(ActivitiesPageLocators.CLEAR_BUTTON)
                self.wait_for_loader()

            self.send_keys(ActivitiesPageLocators.SEARCH_INPUT, value)
            sleep(1)
            self.click(ActivitiesPageLocators.SEARCH_BUTTON)
            self.wait_for_loader(timeout=30)
            return True
        except NoSuchElementException as e:
            printf(f"Error during activities search operation: {e}")
            return False

    def verify_activities_search_results(self, search_criteria, search_value):
        self.wait_for_loader(timeout=10)
        self.is_element_visible(ActivitiesPageLocators.DELETE_BUTTON, timeout=30)
        return verify_search_results_in_table(
            self,
            search_value,
            ActivitiesPageLocators.ACTIVITIES_TABLE_ROWS,
            search_criteria,
        )

    def click_on_activities_action_button(self, action_button):
        self.wait_for_loader()
        if action_button == "View History":
            self.click(ActivitiesPageLocators.HISTORY_BUTTON)
        elif action_button == "Duplicate":
            self.click(ActivitiesPageLocators.DUPLICATE_BUTTON)
        elif action_button == "Edit":
            self.click(ActivitiesPageLocators.EDIT_BUTTON)
        elif action_button == "Delete":
            self.click(ActivitiesPageLocators.DELETE_BUTTON)
        else:
            raise AssertionError(f"Action button '{action_button}' not recognized.")

    def verify_activities_operation_history_dialog(self):
        try:
            self.is_element_visible(ActivitiesPageLocators.OPERATION_HISTORY_DIALOG, timeout=5)
            self.click(ActivitiesPageLocators.OPERATION_HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException:
            return False

    def is_navigated_to_activity_edit_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.ACTIVITY_EDIT, partial=False)

    def verify_activity_delete_confirmation_dialog(self):
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(ActivitiesPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=5)
            self.click(ActivitiesPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def verify_activity_duplicate_prefilled(self):
        try:
            self.wait_for_dom_stability()
            if not self.check_url_contains(Routes.ACTIVITY_DUPLICATE, partial=False):
                return False
            activity_name = self.get_attribute(ActivitiesPageLocators.ACTIVITY_NAME_INPUT, "value")
            return bool(activity_name and activity_name.strip())
        except Exception as e:
            printf(f"Error verifying duplicate activity prefilled data: {e}")
            return False

    def select_activity_records_per_page(self, records):
        self.custom_select_by_locator(
            ActivitiesPageLocators.PAGE_LIMIT_DROPDOWN,
            ActivitiesPageLocators.DROPDOWN_OPTION(records),
        )

    def verify_activity_records_per_page(self, records):
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(ActivitiesPageLocators.ACTIVITIES_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying activity rows per page: {e}")
            return False

    def is_navigated_to_activities_page(self):
        return self.check_url_contains(Routes.ACTIVITIES, partial=False)