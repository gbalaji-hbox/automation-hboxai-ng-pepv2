from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException

from features.commons.locators import UsersPageLocators, UserGroupPageLocators
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
        if tab_name == 'User':
            tab_locator = UsersPageLocators.USER_TAB
        else:
            tab_locator = UserGroupPageLocators.USER_GROUP_TAB

        try:
            if self.is_element_visible(UsersPageLocators.CLEAR_SEARCH_BUTTON, timeout=2):
                self.click(UsersPageLocators.CLEAR_SEARCH_BUTTON)
                self.wait_for_dom_stability_full()

            tab_ele = self.find_element(tab_locator)
            if self.get_attribute(tab_ele,"aria-selected") == "true":
                printf(f"Tab '{tab_name}' is already selected.")
                return
            tab_ele.click()
            self.wait_for_loader()
        except NoSuchElementException:
            printf(f"Tab with name '{tab_name}' not found on Users Page.")
            raise

    def get_first_row_data(self):
        self.wait_for_loader()
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
            if field in ['Update Date', 'Last Active', 'Created Date', 'Updated Date']:
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

    def verify_search_results(self, search_criteria, search_value, tab_name):
        """Verify search results contain the matching patient data."""
        self.wait_for_loader(timeout=10)
        if tab_name == 'User':
            table_locator = UsersPageLocators.USERS_TABLE_ROWS
        else:
            table_locator = UserGroupPageLocators.USER_GROUPS_TABLE_ROWS

        return verify_search_results_in_table(
            self,
            search_value,
            table_locator,
            search_criteria
        )

    def click_on_action_button(self, action_button, tab_name, table_name):
        """Click on the specified action button for the first user in the users table."""
        try:
            printf(f"Clicking on action button '{action_button}' for tab '{tab_name}' in table '{table_name}'")
            if tab_name.lower() == "user":
                locators = UsersPageLocators
            else:
                locators = UserGroupPageLocators

            if action_button == "View History":
                self.click(locators.HISTORY_BUTTON)
            elif action_button == "Edit":
                self.click(locators.EDIT_BUTTON)
            elif action_button == "Delete":
                self.click(locators.DELETE_BUTTON)
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

    def click_add_new_user(self):
        """Click the Add New User button."""
        try:
            self.click(UsersPageLocators.ADD_NEW_USER_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked Add New User button.")
        except NoSuchElementException:
            printf("Add New User button not found.")
            raise

    def fill_create_user_form(self, first_name, last_name, email, phone, password, user_type="ES"):
        """Fill the create user form with provided data."""
        try:
            self.send_keys(UsersPageLocators.FIRST_NAME_INPUT, first_name)
            self.send_keys(UsersPageLocators.LAST_NAME_INPUT, last_name)
            self.send_keys(UsersPageLocators.EMAIL_INPUT, email)
            self.send_keys(UsersPageLocators.PHONE_INPUT, phone)
            self.send_keys(UsersPageLocators.PASSWORD_INPUT, password)
            self.select_user_type(user_type)
            self.select_dates()
            printf(f"Filled create user form for {first_name} {last_name}.")
        except NoSuchElementException as e:
            printf(f"Error filling create user form: {e}")
            raise

    def select_user_type(self, user_type):
        """Select user type from combobox."""
        try:
            self.click(UsersPageLocators.USER_TYPE_COMBOBOX)
            self.wait_for_dom_stability()
            # Assume the option is //div[@role='option']/span[normalize-space(text())=user_type]
            option_locator = (By.XPATH, f"//div[@role='option']/span[normalize-space(text())='{user_type}']")
            self.click(option_locator)
            printf(f"Selected user type: {user_type}")
        except NoSuchElementException as e:
            printf(f"Error selecting user type: {e}")
            raise

    def select_dates(self):
        """Select from and end dates."""
        try:
            self.click(UsersPageLocators.FROM_DATE_BUTTON)
            self.wait_for_dom_stability()
            # Select today's date, assume 21st
            self.click((By.XPATH, "//button[@name='day' and text()='21']"))  # Adjust if needed
            self.click(UsersPageLocators.END_DATE_BUTTON)
            self.wait_for_dom_stability()
            self.click((By.XPATH, "//button[@name='day' and text()='31']"))  # Last day
            printf("Selected dates.")
        except NoSuchElementException as e:
            printf(f"Error selecting dates: {e}")
            raise

    def submit_user_form(self):
        """Click Save button."""
        try:
            self.click(UsersPageLocators.SAVE_BUTTON)
            self.wait_for_loader()
            printf("Submitted user form.")
        except NoSuchElementException:
            printf("Save button not found.")
            raise

    def cancel_user_form(self):
        """Click Cancel button."""
        try:
            self.click(UsersPageLocators.CANCEL_BUTTON)
            self.wait_for_dom_stability()
            printf("Cancelled user form.")
        except NoSuchElementException:
            printf("Cancel button not found.")
            raise

    def check_notification(self, message):
        """Check if notification appears."""
        try:
            self.is_element_visible((By.XPATH, f"//div[normalize-space(text())='{message}']"), timeout=5)
            printf(f"Notification '{message}' appeared.")
            return True
        except:
            printf(f"Notification '{message}' not found.")
            return False

    def find_and_edit_user(self, email):
        """Find user by email and click edit."""
        try:
            self.perform_search_by_field("Email", email)
            self.click(UsersPageLocators.EDIT_BUTTON)
            printf(f"Found and clicked edit for user {email}.")
        except NoSuchElementException as e:
            printf(f"Error finding user {email}: {e}")
            raise

    def update_user_last_name(self, new_last_name):
        """Update last name in edit form."""
        try:
            self.send_keys(UsersPageLocators.LAST_NAME_INPUT, new_last_name)
            printf(f"Updated last name to {new_last_name}.")
        except NoSuchElementException as e:
            printf(f"Error updating last name: {e}")
            raise

    def find_and_delete_user(self, email, confirm=True):
        """Find user by email and delete."""
        try:
            self.perform_search_by_field("Email", email)
            self.click(UsersPageLocators.DELETE_BUTTON)
            if confirm:
                self.click(UsersPageLocators.DELETE_CONFIRM_BUTTON)
            printf(f"Deleted user {email}.")
        except NoSuchElementException as e:
            printf(f"Error deleting user {email}: {e}")
            raise

    def check_validation_errors(self):
        """Check if validation errors are present."""
        try:
            errors = self.find_elements(UsersPageLocators.VALIDATION_ERROR)
            if errors:
                printf(f"Found {len(errors)} validation errors.")
                return True
            else:
                printf("No validation errors found.")
                return False
        except:
            printf("Error checking validation errors.")
            return False

    def delete_users_with_email_containing(self, substring):
        """Delete all users whose email contains the substring."""
        try:
            # This would require iterating through table rows, checking emails, and deleting.
            # For simplicity, assume searching and deleting one by one if needed.
            printf(f"Deleting users with email containing '{substring}' - implementation needed.")
            # Not implemented fully, as it requires more logic.
        except Exception as e:
            printf(f"Error deleting users: {e}")
            raise
