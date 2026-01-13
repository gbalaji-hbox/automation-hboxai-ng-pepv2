from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException

from features.commons.locators import UsersPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class UsersPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def click_on_tab(self, tab_name):
        """Click on the specified tab in the users page."""
        try:
            if self.is_element_visible(UsersPageLocators.CLEAR_SEARCH_BUTTON):
                self.click(UsersPageLocators.CLEAR_SEARCH_BUTTON)
                self.wait_for_loader(timeout=10)

            tab_ele = self.find_element(UsersPageLocators.USER_TABS(tab_name))
            if self.get_attribute(tab_ele,"aria-selected"):
                printf(f"Tab '{tab_name}' is already selected.")
                return
            tab_ele.click()
        except NoSuchElementException:
            printf(f"Tab with name '{tab_name}' not found on Users Page.")
            raise

    def get_first_row_data(self):
        return extract_table_row_as_dict(self, UsersPageLocators.USERS_TABLE)

    def perform_search_by_field(self, field, value):
        """Perform search in the users table by specified field and value."""
        try:
            printf(f"Performing search for field '{field}' with value '{value}'")
            # Click on the search type dropdown
            self.click(UsersPageLocators.SEARCH_TYPE_DROPDOWN)
            sleep(1)
            # Select the desired search type option
            option_locator = UsersPageLocators.SEARCH_TYPE_OPTION(field)
            self.click(option_locator)
            sleep(1)
            # Enter the search value
            if field in ['Update Date', 'Last Active']:
                self.click(UsersPageLocators.SEARCH_DATEPICKER_INPUT)
                sleep(1)
                self.select_calender_date(value)
            else:
                self.send_keys(UsersPageLocators.SEARCH_INPUT, value)
            sleep(1)
            # Click the search button
            self.click(UsersPageLocators.SEARCH_BUTTON)

            return True
        except NoSuchElementException as e:
            printf(f"Error during search operation: {e}")
            return False

    def verify_search_results(self, search_criteria, search_value):
        """Verify search results contain the matching patient data."""
        self.wait_for_loader(timeout=10)
        return verify_search_results_in_table(
            self,
            search_value,
            UsersPageLocators.USERS_TABLE_ROWS,
            search_criteria
        )

    def click_on_action_button(self, action_button):
        """Click on the specified action button for the first user in the users table."""
        try:
            if action_button == "View History":
                self.click(UsersPageLocators.HISTORY_BUTTON)
            elif action_button == "Edit":
                self.click(UsersPageLocators.EDIT_BUTTON)
            elif action_button == "Delete":
                self.click(UsersPageLocators.DELETE_BUTTON)
            else:
                printf(f"Action button '{action_button}' is not recognized.")
                raise ValueError(f"Unknown action button: {action_button}")
        except NoSuchElementException:
            printf(f"Action button '{action_button}' not found in Users Table.")
            raise

    def is_user_history_dialog_open(self):
        """Check if the User Operation History dialog is open."""
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(UsersPageLocators.HISTORY_DIALOG)
            self.click(UsersPageLocators.HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except Exception as e:
            printf(f"Error during user history dialog: {e}")
            return False

    def is_navigated_to_edit_user_page(self):
        """Check if navigated to the Edit User page."""
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.EDIT_USER, partial=False)

    def is_delete_confirmation_dialog_open(self):
        """Check if the confirmation dialog appears."""
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(UsersPageLocators.DELETE_DIALOG)
            self.click(UsersPageLocators.DELETE_DIALOG_CANCEL_BUTTON)
            return True
        except Exception as e:
            printf(f"Error during user history dialog: {e}")
            return False

    def select_records_per_page(self, count):
        """Select number of records per page from pagination dropdown."""
        try:
            self.custom_select_by_locator(UsersPageLocators.PAGE_LIMIT_DROPDOWN, UsersPageLocators.SEARCH_TYPE_OPTION(count))
        except NoSuchElementException as e:
            printf(f"Error during selecting records per page: {e}")
            raise

    def verify_rows_per_page(self, expected_count):
        """Verify the number of rows displayed per page matches expected count."""
        try:
            self.wait_for_loader()
            actual_count = self.get_number_of_table_rows(UsersPageLocators.USERS_TABLE_ROWS)
            printf(f"Expected rows per page: {expected_count}, Actual rows displayed: {actual_count}")
            return row_count_check(expected_count, actual_count)
        except Exception as e:
            printf(f"Error verifying rows per page: {e}")
            return False
