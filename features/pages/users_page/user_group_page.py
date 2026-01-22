from time import sleep

from faker.proxy import Faker
from selenium.webdriver.common.by import By

from features.commons.locators import UserGroupPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, row_count_check


class UserGroupPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def get_first_row_data(self):
        return extract_table_row_as_dict(self, UserGroupPageLocators.USER_GROUPS_TABLE)

    def is_user_group_history_dialog_open(self):
        """Check if the User Operation History dialog is open."""
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(UserGroupPageLocators.HISTORY_DIALOG)
            self.click(UserGroupPageLocators.HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except Exception as e:
            printf(f"Error during user history dialog: {e}")
            return False

    def is_navigated_to_edit_user_group_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.EDIT_GROUP, partial=False)

    def is_delete_confirmation_dialog_open(self):
        """Check if the confirmation dialog appears."""
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(UserGroupPageLocators.DELETE_DIALOG)
            self.click(UserGroupPageLocators.DELETE_DIALOG_CANCEL_BUTTON)
            return True
        except Exception as e:
            printf(f"Error during user history dialog: {e}")
            return False

    def verify_rows_per_page(self, expected_count):
        """Verify the number of rows displayed per page matches expected count."""
        try:
            self.wait_for_loader()
            actual_count = self.get_number_of_table_rows(UserGroupPageLocators.USER_GROUPS_TABLE)
            printf(f"Expected rows per page: {expected_count}, Actual rows displayed: {actual_count}")
            return row_count_check(expected_count, actual_count)
        except Exception as e:
            printf(f"Error verifying rows per page: {e}")
            return False

    def click_add_new_user_group(self):
        """Click the Add New User Group button."""
        try:
            self.click(UserGroupPageLocators.ADD_NEW_USER_GROUP_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked Add New User Group button.")
        except Exception as e:
            printf("Add New User Group button not found.")
            raise

    def fill_create_user_group_form(self):
        """Fill the create user group form with valid generated data."""
        try:
            name = f"Automation-Test Group {self.faker.unique.random_int(1000, 9999)}"
            self.send_keys(UserGroupPageLocators.GROUP_NAME_INPUT, name)
            # Add users
            self.click(UserGroupPageLocators.ADD_USERS_BUTTON)
            self.wait_for_dom_stability()
            # Select a user, e.g., test_user_1512
            self.add_users_by_type(count=2, user_type="ES")
            printf(f"Filled create user group form for {name}.")
            return {"name": name}
        except Exception as e:
            printf(f"Error filling create user group form: {e}")
            raise

    def add_users_by_type(self, count=1, user_type="ES"):
        """Add users to the group by type."""
        try:
            self.wait_for_dom_stability()
            self.custom_select_by_locator(UserGroupPageLocators.ADD_USERS_FILTER_DROPDOWN, UserGroupPageLocators.ADD_USER_FILTER_OPTION("User Type"))
            self.wait_for_dom_stability()
            self.send_keys(UserGroupPageLocators.ADD_USERS_SEARCH_INPUT, user_type)
            self.wait_for_dom_stability()
            user_checkboxes = self.find_elements(UserGroupPageLocators.ADD_USER_SELECTION_CHECKBOX)
            selected = 0
            for checkbox in user_checkboxes:
                checkbox.click()
                selected += 1
                if selected >= count:
                    break
                    
            self.wait_for_dom_stability()
            self.click(UserGroupPageLocators.ADD_USERS_ADD_BUTTON)
            self.wait_for_dom_stability()
            printf(f"Added {selected} users of type {user_type} to the group.")
        except Exception as e:
            printf(f"Error adding users by type: {e}")
            raise

    def submit_user_group_form(self):
        """Click Save button."""
        try:
            self.click(UserGroupPageLocators.SAVE_BUTTON)
            printf("Submitted user group form.")
        except Exception as e:
            printf("Save button not found.")
            raise

    def cancel_user_group_form(self):
        """Click Cancel button."""
        try:
            self.click(UserGroupPageLocators.CANCEL_BUTTON)
            self.wait_for_dom_stability()
            printf("Cancelled user group form.")
        except Exception as e:
            printf("Cancel button not found.")
            raise

    def check_group_notification(self, message):
        """Check if notification appears."""
        locator_map = {
            "User Group Created": UserGroupPageLocators.USER_GROUP_CREATED_SUCCESS,
            "User group updated successfully": UserGroupPageLocators.USER_GROUP_UPDATED_SUCCESS,
            "User group deleted successfully": UserGroupPageLocators.USER_GROUP_DELETED_SUCCESS,
        }
        try:
            self.is_element_visible(locator_map[message], timeout=5)
            printf(f"Notification '{message}' appeared.")
            return True
        except Exception as e:
            printf(f"Notification '{message}' not found.")
            return False

    def find_and_edit_user_group(self, name):
        """Find user group by name and click edit."""
        try:
            self.wait_for_loader()
            self.perform_search_by_field("Group Name", name)
            self.click(UserGroupPageLocators.EDIT_BUTTON)
            printf(f"Found and clicked edit for user group {name}.")
        except Exception as e:
            printf(f"Error finding user group {name}: {e}")
            raise

    def update_user_group_name(self, suffix):
        """Update name in edit form."""
        try:
            new_name = " " + suffix
            self.send_keys(UserGroupPageLocators.GROUP_NAME_INPUT, new_name)
            current_name = self.get_attribute(UserGroupPageLocators.GROUP_NAME_INPUT, "value")
            printf(f"Updated user group name to {current_name}.")
            return current_name
        except Exception as e:
            printf(f"Error updating user group name: {e}")
            raise

    def find_and_delete_user_group(self, name):
        """Find user group by name and delete."""
        try:
            self.wait_for_loader()
            self.perform_search_by_field("Group Name", name)
            self.click(UserGroupPageLocators.DELETE_BUTTON)
            printf(f"Deleting user group {name}.")
        except Exception as e:
            printf(f"Error deleting user group {name}: {e}")
            raise

    def confirm_user_group_delete(self):
        """Confirm user group deletion in dialog."""
        try:
            self.click(UserGroupPageLocators.DELETE_CONFIRM_BUTTON)
            printf("Confirmed user group deletion.")
        except Exception as e:
            printf(f"Error confirming user group deletion: {e}")
            raise

    def delete_user_groups_with_name_containing(self, keyword):
        """Delete all user groups whose name contains the keyword."""
        deleted_count = 0
        for iteration in range(1, 11):
            printf(f"Iteration {iteration}: Searching for user groups containing '{keyword}' in name")
            rows = self._perform_search_and_get_user_group_rows(keyword)
            if rows is None:
                break
            if self._delete_first_matching_user_group_by_name(rows, keyword):
                deleted_count += 1
                printf(f" (#{deleted_count})")
            else:
                printf(f"No user group with name containing '{keyword}' found in current results - stopping")
                break
        if iteration == 10:
            printf("Reached maximum iterations (10) - stopping to prevent infinite loop")
        return deleted_count

    def _perform_search_and_get_user_group_rows(self, keyword):
        """Perform search by name containing keyword and return valid rows if groups are found, else None."""
        if self.is_element_visible(UserGroupPageLocators.DELETE_DIALOG, timeout=2):
            self.click(UserGroupPageLocators.DELETE_DIALOG_CANCEL_BUTTON)

        self.perform_search_by_field("Group Name", keyword)

        try:
            self.wait_for_loader()
            no_data_element = self.is_element_visible(UserGroupPageLocators.USER_GROUPS_TABLE_ROWS, timeout=2)
            if not no_data_element:
                printf(f"No user groups found containing '{keyword}' in name - cleanup complete")
                return None
        except Exception as e:
            printf(f"Error checking for no data element: {e}")
            return None

        rows = self.find_elements(UserGroupPageLocators.USER_GROUPS_TABLE_ROWS)
        if not rows:
            printf("No table rows found - cleanup complete")
            return None

        first_row_text = rows[0].text.strip()
        if "No groups found" in first_row_text or first_row_text == "":
            printf(f"No user groups found containing '{keyword}' in name - cleanup complete")
            return None

        return rows

    def _delete_first_matching_user_group_by_name(self, rows, keyword):
        """Delete the first user group in rows whose name contains the keyword. Return True if deleted."""
        try:
            for row in rows:
                name_cell = row.find_element(By.XPATH, ".//td[1]")
                name = name_cell.text.strip()
                if keyword.lower() in name.lower():
                    delete_button = row.find_element(By.XPATH, ".//td[5]//button[contains(@id,'delete')]")
                    delete_button.click()
                    sleep(1)
                    self.click(UserGroupPageLocators.DELETE_CONFIRM_BUTTON)
                    printf(f"Successfully deleted user group '{name}'")
                    sleep(2)
                    return True
            return False
        except Exception as e:
            printf(f"Error deleting user group: {e}")
            return False

    def perform_search_by_field(self, field, value):
        """Perform search in the user groups table by specified field and value."""
        try:
            printf(f"Performing search for field '{field}' with value '{value}'")
            self.click(UserGroupPageLocators.SEARCH_TYPE_DROPDOWN)
            from time import sleep
            sleep(1)
            option_locator = UserGroupPageLocators.SEARCH_TYPE_OPTION(field)
            self.click(option_locator)
            sleep(1)
            self.send_keys(UserGroupPageLocators.SEARCH_INPUT, value)
            sleep(1)
            self.click(UserGroupPageLocators.SEARCH_BUTTON)
            return True
        except Exception as e:
            printf(f"Error during search operation: {e}")
            return False