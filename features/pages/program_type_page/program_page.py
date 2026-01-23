import random
from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from features.commons.locators import ProgramPageLocators, PatientProgramStatusPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class ProgramPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def navigate_to_tab(self, tab_name):
        """Navigate to the specified tab in the Program Type page."""
        if tab_name == 'Program':
            locator = ProgramPageLocators.PROGRAM_TAB
        else:
            locator = PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_TAB

        try:
            if self.is_element_visible(ProgramPageLocators.CLEAR_SEARCH_BUTTON, timeout=2):
                self.click(ProgramPageLocators.CLEAR_SEARCH_BUTTON)
                self.wait_for_dom_stability_full()

            tab_ele = self.find_element(locator)
            if self.get_attribute(tab_ele, "aria-selected") == "true":
                printf(f"Tab '{tab_name}' is already selected.")
                return
            tab_ele.click()
            self.wait_for_loader()
            if not tab_name == 'Program':
                self.clear_field(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_SEARCH_INPUT)
                sleep(1)
        except NoSuchElementException:
            printf(f"Tab with name '{tab_name}' not found on Users Page.")
            raise

    def get_program_first_row_data(self):
        self.wait_for_loader()
        return extract_table_row_as_dict(self, ProgramPageLocators.PROGRAM_TABLE)

    def perform_program_search_by_field(self, field, value):
        try:
            printf(f"Performing search for field '{field}' with value '{value}'")
            # Click on the search type dropdown
            self.click(ProgramPageLocators.PROGRAM_SEARCH_DROPDOWN)
            sleep(1)
            # Select the desired search type option
            option_locator = ProgramPageLocators.DROPDOWN_OPTION(field)
            self.click(option_locator)
            sleep(1)
            # Enter the search value
            if field in ['Update Date', 'Last Active', 'Created Date', 'Updated Date']:
                self.click(ProgramPageLocators.PROGRAM_SEARCH_DATE_PICKER_INPUT)
                sleep(1)
                self.select_calender_date(value)
            elif field == 'Applicable Statuses':
                status_part = value.split(",")[-1].strip()
                one_word = status_part.split()[0]
                self.send_keys(ProgramPageLocators.PROGRAM_SEARCH_INPUT, one_word)
            else:
                self.send_keys(ProgramPageLocators.PROGRAM_SEARCH_INPUT, value)
            sleep(1)
            # Click the search button
            self.click(ProgramPageLocators.PROGRAM_SEARCH_BUTTON)

            return True
        except NoSuchElementException as e:
            printf(f"Error during search operation: {e}")
            return False

    def verify_program_search_results(self, search_criteria, search_value, tab_name):
        self.wait_for_loader(timeout=10)
        if tab_name == 'Program':
            table_locator = ProgramPageLocators.PROGRAM_TABLE_ROWS
        else:
            table_locator = PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_TABLE

        return verify_search_results_in_table(
            self,
            search_value,
            table_locator,
            search_criteria
        )

    def click_on_program_action_button(self, action_button):
        self.wait_for_loader()
        try:
            if action_button == "View History":
                button_locator = ProgramPageLocators.PROGRAM_HISTORY_BUTTON
            elif action_button == "Edit":
                button_locator = ProgramPageLocators.PROGRAM_EDIT_BUTTON
            elif action_button == "Delete":
                button_locator = ProgramPageLocators.PROGRAM_DELETE_BUTTON
            else:
                printf(f"Action button '{action_button}' not recognized.")
                return

            self.click(button_locator)
        except NoSuchElementException:
            printf(f"Action button '{action_button}' not found in the first row of the programs table.")
            raise

    def verify_program_operation_history_dialog(self):
        try:
            self.is_element_visible(ProgramPageLocators.PROGRAM_OPERATION_HISTORY_DIALOG, timeout=5)
            self.click(ProgramPageLocators.PROGRAM_OPERATION_HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException:
            return False

    def is_navigated_to_program_edit_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.PROGRAM_EDIT, partial=False)

    def verify_program_delete_confirmation_dialog(self):
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(ProgramPageLocators.PROGRAM_DELETE_CONFIRMATION_DIALOG, timeout=5)
            self.click(ProgramPageLocators.PROGRAM_DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def select_programs_records_per_page(self, records):
        try:
            self.custom_select_by_locator(ProgramPageLocators.PROGRAM_PAGE_LIMIT_DROPDOWN,
                                          ProgramPageLocators.DROPDOWN_OPTION(records))
        except NoSuchElementException as e:
            printf(f"Error during selecting records per page: {e}")
            raise

    def verify_program_records_per_page(self, records):
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(ProgramPageLocators.PROGRAM_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying rows per page: {e}")
            return False

    def click_add_new_program(self):
        """Click the Add New Program button."""
        try:
            self.click(ProgramPageLocators.ADD_NEW_PROGRAM_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked Add New Program button.")
        except NoSuchElementException:
            printf("Add New Program button not found.")
            raise

    def fill_create_program_form(self):
        """Fill the create program form with valid generated data."""
        try:
            program_name = f"Automation-{self.faker.word().capitalize()} Program"
            self.send_keys(ProgramPageLocators.PROGRAM_NAME_INPUT, program_name)
            
            # Click on the status dropdown to open it
            self.click(ProgramPageLocators.PROGRAM_STATUS_SELECT_DROPDOWN)
            self.wait_for_dom_stability()
            
            # Get all available status options
            status_options = self.find_elements(ProgramPageLocators.PROGRAM_STATUS_OPTIONS)
            selected_statuses = []
            
            # Select 2-3 random statuses
            num_to_select = min(3, len(status_options))

            selected_indices = random.sample(range(len(status_options)), num_to_select)
            
            for index in selected_indices:
                option = status_options[index]
                option_text = option.text.strip()
                if option_text:  # Only select if there's text
                    option.click()
                    selected_statuses.append(option_text)
            
            printf(f"Filled create program form for '{program_name}' with statuses: {selected_statuses}")
            self.click(ProgramPageLocators.PROGRAM_STATUS_SELECT_DROPDOWN)
            return {
                "name": program_name,
                "statuses": selected_statuses
            }
        except NoSuchElementException as e:
            printf(f"Error filling create program form: {e}")
            raise

    def submit_program_form(self):
        """Submit the program form (Save or Update)."""
        try:
            # Check if Update button exists (edit mode), otherwise Save
            if self.is_element_visible(ProgramPageLocators.PROGRAM_SAVE_BUTTON, timeout=2):
                self.click(ProgramPageLocators.PROGRAM_SAVE_BUTTON)
            else:
                self.click(ProgramPageLocators.PROGRAM_SAVE_BUTTON)
            self.wait_for_loader()
            printf("Submitted program form.")
        except NoSuchElementException as e:
            printf(f"Error submitting program form: {e}")
            raise

    def cancel_program_form(self):
        """Cancel the program form."""
        try:
            self.click(ProgramPageLocators.PROGRAM_CANCEL_BUTTON)
            self.wait_for_dom_stability()
            printf("Cancelled program form.")
        except NoSuchElementException as e:
            printf(f"Error cancelling program form: {e}")
            raise

    def check_program_notification(self, expected_message):
        """Check if the expected notification appears."""
        try:
            if "created" in expected_message.lower():
                locator = ProgramPageLocators.PROGRAM_CREATED_NOTIFICATION
            elif "updated" in expected_message.lower():
                locator = ProgramPageLocators.PROGRAM_UPDATED_NOTIFICATION
            elif "deleted" in expected_message.lower():
                locator = ProgramPageLocators.PROGRAM_DELETED_NOTIFICATION
            else:
                printf(f"Unknown notification type: {expected_message}")
                return False
            
            return self.is_element_visible(locator, timeout=5)
        except NoSuchElementException:
            return False

    def find_and_edit_program(self, program_name):
        """Find a program by name and click edit."""
        try:
            # Search for the program first
            self.perform_program_search_by_field("Program Name", program_name)
            self.wait_for_loader()
            
            # Click edit on the first matching row
            self.click(ProgramPageLocators.PROGRAM_EDIT_BUTTON)
            self.wait_for_dom_stability()
            printf(f"Clicked edit for program '{program_name}'.")
        except NoSuchElementException as e:
            printf(f"Error finding and editing program '{program_name}': {e}")
            raise

    def update_program_name(self, suffix):
        """Update the program name by appending a suffix."""
        try:
            new_name = f" - {suffix}"
            self.clear_field(ProgramPageLocators.PROGRAM_NAME_INPUT)
            self.send_keys(ProgramPageLocators.PROGRAM_NAME_INPUT, new_name)
            current_name = self.get_attribute(ProgramPageLocators.PROGRAM_NAME_INPUT, "value")
            printf(f"Updated program name to '{current_name}'.")
            return current_name
        except NoSuchElementException as e:
            printf(f"Error updating program name: {e}")
            raise

    def find_and_delete_program(self, program_name):
        """Find a program by name and click delete."""
        try:
            # Search for the program first
            self.perform_program_search_by_field("Program Name", program_name)
            self.wait_for_loader()
            
            # Click delete on the first matching row
            self.click(ProgramPageLocators.PROGRAM_DELETE_BUTTON)
            printf(f"Clicked delete for program '{program_name}'.")
        except NoSuchElementException as e:
            printf(f"Error finding and deleting program '{program_name}': {e}")
            raise

    def confirm_program_delete(self):
        """Confirm the program deletion in the dialog."""
        try:
            self.click(ProgramPageLocators.PROGRAM_DELETE_CONFIRM_BUTTON)
            self.wait_for_loader()
            printf("Confirmed program deletion.")
        except NoSuchElementException as e:
            printf(f"Error confirming program deletion: {e}")
            raise

    def is_returned_to_programs_page(self):
        """Check if returned to programs page after cancel."""
        return self.check_url_contains(Routes.PROGRAM_TYPE, partial=False)

    def delete_programs_with_name_containing(self, substring):
        """Delete all programs containing the substring in name."""
        deleted_count = 0
        for iteration in range(1, 11):
            printf(f"Iteration {iteration}: Searching for programs containing '{substring}' in name")
            rows = self._perform_program_search_and_get_rows(substring)
            if rows is None:
                break
            if self._delete_first_matching_program_by_name(rows, substring):
                deleted_count += 1
                printf(f" (#{deleted_count})")
            else:
                printf(f"No program with name containing '{substring}' found in current results - stopping")
                break
            if iteration == 10:
                printf("Reached maximum iterations (10) - stopping to prevent infinite loop")
        return deleted_count

    def _perform_program_search_and_get_rows(self, substring):
        """Perform search by program name containing substring and return valid rows if programs are found, else None."""
        # Clear any open modal if present
        if self.is_element_visible(ProgramPageLocators.PROGRAM_DELETE_CONFIRMATION_DIALOG, timeout=2):
            self.click(ProgramPageLocators.PROGRAM_DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            sleep(1)

        # Perform search by program name field with the substring
        self.perform_program_search_by_field("Program Name", substring)

        # Check if no programs found
        try:
            self.wait_for_loader()
            no_data_element = self.is_element_visible(ProgramPageLocators.PROGRAM_TABLE_ROWS, timeout=2)
            if not no_data_element:
                printf(f"No programs found containing '{substring}' in name - cleanup complete")
                return None
        except Exception as e:
            printf(f"Error checking for no data element: {e}")
            return None

        rows = self.find_elements(ProgramPageLocators.PROGRAM_TABLE_ROWS)
        if not rows:
            printf("No table rows found - cleanup complete")
            return None

        first_row_text = rows[0].text.strip()
        if "No programs found" in first_row_text or first_row_text == "":
            printf(f"No programs found containing '{substring}' in name - cleanup complete")
            return None

        return rows

    def _delete_first_matching_program_by_name(self, rows, substring):
        """Delete the first program in rows whose name contains the substring. Return True if deleted."""
        try:
            for row in rows:
                # Assume program name is in column 1 (td[1])
                name_cell = row.find_element(By.XPATH, ".//td[1]")
                program_name = name_cell.text.strip()
                if substring.lower() in program_name.lower():
                    # Find delete button in the last column
                    delete_button = row.find_element(By.XPATH, ".//td[last()]//button[contains(@id,'delete')]")
                    delete_button.click()
                    sleep(1)
                    self.click(ProgramPageLocators.PROGRAM_DELETE_CONFIRM_BUTTON)
                    printf(f"Successfully deleted program '{program_name}'")
                    sleep(2)
                    return True
            return False
        except Exception as e:
            printf(f"Error deleting program: {e}")
            return False