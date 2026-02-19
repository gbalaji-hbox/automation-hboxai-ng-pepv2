from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from features.commons.locators import UsersPageLocators, UserGroupPageLocators, DashboardPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check, get_current_date


class UsersPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def click_on_tab(self, tab_name):
        """Click on the specified tab in the users page."""
        if self.is_element_visible(DashboardPageLocators.NOTIFICATION_POPUP, timeout=2):
            self.click(DashboardPageLocators.NOTIFICATION_CLOSE_BUTTON)
            sleep(1)

        if tab_name == 'User':
            tab_locator = UsersPageLocators.USER_TAB
        else:
            tab_locator = UserGroupPageLocators.USER_GROUP_TAB

        try:
            if self.is_element_visible(UsersPageLocators.CLEAR_SEARCH_BUTTON, timeout=2):
                self.click(UsersPageLocators.CLEAR_SEARCH_BUTTON)
                self.wait_for_dom_stability_full()

            tab_ele = self.find_element(tab_locator)
            if self.get_attribute(tab_ele, "aria-selected") == "true":
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
            if self.is_element_visible(UsersPageLocators.CLEAR_SEARCH_BUTTON, timeout=2):
                self.click(UsersPageLocators.CLEAR_SEARCH_BUTTON)
                self.wait_for_dom_stability_full()
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
            self.custom_select_by_locator(UsersPageLocators.PAGE_LIMIT_DROPDOWN,
                                          UsersPageLocators.SEARCH_TYPE_OPTION(count))
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

    def fill_create_user_form(self, user_role=None, email=None, password=None):
        """Fill the create user form with valid generated data or specific values.
        
        Args:
            user_role: Optional specific role (ES, CS, PE, etc.). If None, defaults to ES.
            email: Optional specific email. If None, generates automation email.
            password: Optional specific password. If None, defaults to Password123.
            
        Returns:
            dict: User information including all fields.
        """
        try:
            first_name = f"Automation-{self.faker.first_name()}"
            last_name = self.faker.last_name()

            if email is None:
                email = f"{first_name.lower()}.{last_name.lower()}@hbox.ai"

            phone = self.faker.numerify(text="##########")

            if password is None:
                password = "Password123"

            if user_role is None:
                user_type = "ES"
            else:
                user_type = user_role

            self.send_keys(UsersPageLocators.FIRST_NAME_INPUT, first_name)
            self.send_keys(UsersPageLocators.LAST_NAME_INPUT, last_name)
            self.send_keys(UsersPageLocators.EMAIL_INPUT, email)
            self.send_keys(UsersPageLocators.PHONE_INPUT, phone)
            self.send_keys(UsersPageLocators.PASSWORD_INPUT, password)
            self.select_user_type(user_type)
            if not email is None:
                self.select_dates(days_offset=60)
            else:
                self.select_dates()
            self.select_times()
            printf(f"Filled create user form for {first_name} {last_name} with role {user_type}.")
            return {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "password": password,
                "user_type": user_type
            }
        except NoSuchElementException as e:
            printf(f"Error filling create user form: {e}")
            raise

    def select_user_type(self, user_type):
        """Select user type from combobox."""
        try:
            self.custom_select_by_locator(UsersPageLocators.USER_TYPE_COMBOBOX,
                                          UsersPageLocators.SEARCH_TYPE_OPTION(user_type))
            printf(f"Selected user type: {user_type}")
        except NoSuchElementException as e:
            printf(f"Error selecting user type: {e}")
            raise

    def select_dates(self, days_offset=1):
        """Select from and end dates."""
        try:
            start_date = get_current_date(date_format="%d-%m-%Y")
            end_date = get_current_date(date_format="%d-%m-%Y", days_offset=days_offset)
            self.scroll_to_visible_element(UsersPageLocators.FROM_DATE_BUTTON,
                                           container_locator=UsersPageLocators.MAIN_DIV)
            sleep(0.5)
            self.click(UsersPageLocators.FROM_DATE_BUTTON)
            sleep(1)
            self.select_calender_date(start_date)
            sleep(1)
            self.click(UsersPageLocators.END_DATE_BUTTON)
            sleep(1)
            self.select_calender_date(end_date)
            sleep(1)
            self.click(UsersPageLocators.END_DATE_BUTTON)
            printf(f"Selected dates: From {start_date} To {end_date}.")
        except NoSuchElementException as e:
            printf(f"Error selecting dates: {e}")
            raise

    def select_times(self):
        """Select from and end times for the slots"""
        try:
            self.click(UsersPageLocators.SCHEDULE_DAY_CHECKBOX)
            sleep(1)
            self.select_by_visible_text(UsersPageLocators.START_TIME_HOUR_SELECT, "12")
            self.select_by_visible_text(UsersPageLocators.START_TIME_MINUTE_SELECT, "00")
            self.select_by_visible_text(UsersPageLocators.START_TIME_AM_PM_SELECT, "AM")
            self.select_by_visible_text(UsersPageLocators.END_TIME_HOUR_SELECT, "11")
            self.select_by_visible_text(UsersPageLocators.END_TIME_MINUTE_SELECT, "45")
            self.select_by_visible_text(UsersPageLocators.END_TIME_AM_PM_SELECT, "PM")
            sleep(1)
            self.click(UsersPageLocators.COPY_TO_ALL_DAYS_BUTTON)
            sleep(1)
            printf("Selected times and copied to all days.")
        except NoSuchElementException as e:
            printf(f"Error selecting times: {e}")
            raise

    def submit_user_form(self):
        """Click Save button."""
        try:
            self.click(UsersPageLocators.SAVE_BUTTON)
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

    def check_user_notification(self, message):
        """Check if notification appears."""
        try:
            self.is_element_visible(UsersPageLocators.USER_CREATE_SUCCESS, timeout=5)
            printf(f"Notification '{message}' appeared.")
            return True
        except NoSuchElementException:
            printf(f"Notification '{message}' not found.")
            return False

    def find_and_edit_user(self, email):
        """Find user by email and click edit."""
        try:
            self.wait_for_loader()
            self.perform_search_by_field("Email", email)
            self.click(UsersPageLocators.EDIT_BUTTON)
            printf(f"Found and clicked edit for user {email}.")
        except NoSuchElementException as e:
            printf(f"Error finding user {email}: {e}")
            raise

    def update_user_last_name(self, new_last_name):
        """Update last name in edit form."""
        try:
            new_last_name = " " + new_last_name
            self.send_keys(UsersPageLocators.LAST_NAME_INPUT, new_last_name)
            last_name = self.get_attribute(UsersPageLocators.LAST_NAME_INPUT, "value")
            printf(f"Updated last name to {last_name}.")
        except NoSuchElementException as e:
            printf(f"Error updating last name: {e}")
            raise

    def find_and_delete_user(self, email):
        """Find user by email and delete."""
        try:
            self.wait_for_loader()
            self.perform_search_by_field("Email Address", email)
            self.click(UsersPageLocators.DELETE_BUTTON)
            printf(f"Deleting user {email}.")
        except NoSuchElementException as e:
            printf(f"Error deleting user {email}: {e}")
            raise

    def confirm_user_delete(self):
        """Confirm user deletion in dialog."""
        try:
            self.click(UsersPageLocators.DELETE_CONFIRM_BUTTON)
            printf("Confirmed user deletion.")
        except NoSuchElementException as e:
            printf(f"Error confirming user deletion: {e}")
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

    def get_field_locator(self, field_name):
        """Get locator for a field by name."""
        mappings = {
            "first name": UsersPageLocators.FIRST_NAME_INPUT,
            "last name": UsersPageLocators.LAST_NAME_INPUT,
            "email": UsersPageLocators.EMAIL_INPUT,
            "phone number": UsersPageLocators.PHONE_INPUT,
            "password": UsersPageLocators.PASSWORD_INPUT,
        }
        return mappings[field_name.lower()]

    def get_expected_message(self, field_name):
        """Get expected validation error message for a field."""
        messages = {
            "first name": "First name is required",
            "last name": "Last name is required",
            "email": "Please enter a valid email address",
            "phone number": "Phone number must be at least 10 digits",
            "password": "Password must be at least 6 characters",
        }
        return messages[field_name.lower()]

    def enter_text_in_field(self, field_name, text):
        """Enter text in a specific field."""
        try:
            locator = self.get_field_locator(field_name)
            self.send_keys(locator, text)
            printf(f"Entered '{text}' in {field_name} field.")
        except NoSuchElementException:
            printf(f"{field_name} field not found.")
            raise

    def clear_field(self, field_name):
        """Clear a specific field."""
        try:
            locator = self.get_field_locator(field_name)
            self.send_key_down(locator, "BACKSPACE")
            self.send_key_down(locator, "TAB")
            printf(f"Cleared {field_name} field.")
        except NoSuchElementException:
            printf(f"{field_name} field not found.")
            raise

    def check_validation_error_for_field(self, field_name, expected_message):
        """Check if validation error message appears for a field."""
        try:
            if self.is_element_visible(UsersPageLocators.VALIDATION_ERROR(expected_message), timeout=5):
                printf(f"Validation error '{expected_message}' appeared for {field_name}.")
                return True
            else:
                printf(f"Validation error '{expected_message}' not found for {field_name}.")
                return False
        except Exception:
            printf(f"Error checking validation error for {field_name}.")
            return False

    def delete_users_with_email_containing(self, keyword):
        """Delete all users whose email contains the keyword."""
        deleted_count = 0
        for iteration in range(1, 11):
            printf(f"Iteration {iteration}: Searching for users containing '{keyword}' in email")
            rows = self._perform_search_and_get_user_rows(keyword)
            if rows is None:
                break
            if self._delete_first_matching_user_by_email(rows, keyword):
                deleted_count += 1
                printf(f" (#{deleted_count})")
            else:
                printf(f"No user with email containing '{keyword}' found in current results - stopping")
                break
        if iteration == 10:
            printf("Reached maximum iterations (10) - stopping to prevent infinite loop")
        return deleted_count

    def _perform_search_and_get_user_rows(self, keyword):
        """Perform search by email containing keyword and return valid rows if users are found, else None."""
        # Clear any open modal if present

        if self.is_element_visible(UsersPageLocators.DELETE_DIALOG, timeout=2):
            self.click(UsersPageLocators.DELETE_DIALOG_CANCEL_BUTTON)
            sleep(1)

        # Perform search by email field with the keyword (assuming search supports partial match)
        self.perform_search_by_field("Email Address", keyword)

        # Check if "No users found" message or similar
        try:
            # Assuming no data is indicated by no rows or specific message
            self.wait_for_loader()
            no_data_element = self.is_element_visible(UsersPageLocators.USERS_TABLE_ROWS, timeout=2)
            if not no_data_element:
                printf(f"No users found containing '{keyword}' in email - cleanup complete")
                return None
        except Exception as e:
            printf(f"Error checking for no data element: {e}")
            return None

        rows = self.find_elements(UsersPageLocators.USERS_TABLE_ROWS)
        if not rows:
            printf("No table rows found - cleanup complete")
            return None

        first_row_text = rows[0].text.strip()
        if "No users found" in first_row_text or first_row_text == "":
            printf(f"No users found containing '{keyword}' in email - cleanup complete")
            return None

        return rows

    def _delete_first_matching_user_by_email(self, rows, keyword):
        """Delete the first user in rows whose email contains the keyword. Return True if deleted."""
        try:
            for row in rows:
                # Assume email is in column 3 (td[3])
                email_cell = row.find_element(By.XPATH, ".//td[2]")
                email = email_cell.text.strip()
                if keyword.lower() in email.lower():
                    # Find delete button in column 6
                    delete_button = row.find_element(By.XPATH, ".//td[6]//button[contains(@id,'delete')]")
                    delete_button.click()
                    sleep(1)
                    self.click(UsersPageLocators.DELETE_CONFIRM_BUTTON)
                    printf(f"Successfully deleted user '{email}'")
                    sleep(2)
                    return True
            return False
        except Exception as e:
            printf(f"Error deleting user: {e}")
            return False

    def is_returned_to_users_page(self):
        """Check if navigated back to the Users page."""
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.USERS_PAGE, partial=False)
