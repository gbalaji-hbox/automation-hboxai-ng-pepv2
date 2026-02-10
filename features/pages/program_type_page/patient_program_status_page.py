from time import sleep

from faker import Faker
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from features.commons.locators import PatientProgramStatusPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class PatientProgramStatusPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def get_patient_program_status_first_row_data(self):
        self.wait_for_loader()
        return extract_table_row_as_dict(self, PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_TABLE)

    def perform_patient_program_status_search_by_field(self, field, value):
        try:
            printf(f"Performing search for field '{field}' with value '{value}'")
            self.send_keys(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_SEARCH_INPUT, value)
            sleep(1)
            return True
        except NoSuchElementException as e:
            printf(f"Error during search operation: {e}")
            return False

    def verify_patient_program_status_search_results(self, search_criteria, search_value):
        self.wait_for_loader(timeout=10)
        return verify_search_results_in_table(
            self,
            search_value,
            PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_TABLE_ROWS,
            search_criteria
        )

    def click_on_patient_program_status_action_button(self, action_button):
        self.wait_for_loader()
        try:
            if action_button == "View History":
                button_locator = PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_HISTORY_BUTTON
            elif action_button == "Edit":
                button_locator = PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_EDIT_BUTTON
            elif action_button == "Delete":
                button_locator = PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETE_BUTTON
            else:
                printf(f"Action button '{action_button}' not recognized.")
                return

            self.click(button_locator)
        except NoSuchElementException:
            printf(f"Action button '{action_button}' not found in the first row of the patient program status table.")
            raise

    def verify_patient_program_status_operation_history_dialog(self):
        try:
            self.is_element_visible(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_OPERATION_HISTORY_DIALOG, timeout=5)
            sleep(1)
            self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_OPERATION_HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException:
            return False

    def is_navigated_to_patient_program_status_edit_page(self):
        self.wait_for_dom_stability()
        # Assuming the edit page URL contains 'patient-program-status' or similar
        return self.check_url_contains(Routes.PATIENT_PROGRAM_STATUS_EDIT, partial=False)

    def verify_patient_program_status_delete_confirmation_dialog(self):
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETE_CONFIRMATION_DIALOG, timeout=5)
            self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def select_patient_program_status_records_per_page(self, records):
        try:
            self.custom_select_by_locator(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_PAGE_LIMIT_DROPDOWN,
                                          PatientProgramStatusPageLocators.DROPDOWN_OPTION(records))
        except NoSuchElementException as e:
            printf(f"Error during selecting records per page: {e}")
            raise

    def verify_patient_program_status_records_per_page(self, records):
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying rows per page: {e}")
            return False

    def click_add_new_patient_program_status(self):
        """Click the Add New Patient Program Status button."""
        try:
            self.click(PatientProgramStatusPageLocators.ADD_NEW_PATIENT_PROGRAM_STATUS_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked Add New Patient Program Status button.")
        except NoSuchElementException:
            printf("Add New Patient Program Status button not found.")
            raise

    def fill_create_patient_program_status_form(self):
        """Fill the create patient program status form with valid generated data."""
        try:
            patient_program_status_name = f"Automation-{self.faker.word().capitalize()} Status"
            self.send_keys(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_NAME_INPUT, patient_program_status_name)

            printf(f"Filled create patient program status form for '{patient_program_status_name}'")
            return {
                "name": patient_program_status_name
            }
        except NoSuchElementException as e:
            printf(f"Error filling create patient program status form: {e}")
            raise

    def submit_patient_program_status_form(self, button_name):
        """Submit the patient program status form (Save or Update)."""
        try:
            if  button_name == "Save Status":
                self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_SAVE_BUTTON)
            elif button_name == "Update Status":
                self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_UPDATE_BUTTON)
            elif button_name == "Cancel":
                self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_CANCEL_BUTTON)
            else:
                printf(f"Button name '{button_name}' not recognized.")
                return
            self.wait_for_loader()
        except NoSuchElementException as e:
            printf(f"Error submitting patient program status form: {e}")
            raise

    def cancel_patient_program_status_form(self):
        """Cancel the patient program status form."""
        try:
            self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_CANCEL_BUTTON)
            self.wait_for_dom_stability()
            printf("Cancelled patient program status form.")
        except NoSuchElementException as e:
            printf(f"Error cancelling patient program status form: {e}")
            raise

    def check_patient_program_status_notification(self, expected_message):
        """Check if the expected patient program status notification appears."""
        try:
            if "created" in expected_message.lower():
                locator = PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_CREATED_NOTIFICATION
            elif "updated" in expected_message.lower():
                locator = PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_UPDATED_NOTIFICATION
            elif "deleted" in expected_message.lower():
                locator = PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETED_NOTIFICATION
            else:
                printf(f"Unknown notification type: {expected_message}")
                return False

            return self.is_element_visible(locator, timeout=5)
        except NoSuchElementException:
            return False

    def find_and_edit_patient_program_status(self, patient_program_status_name):
        """Find a patient program status by name and click edit."""
        try:
            # Search for the patient program status first
            self.perform_patient_program_status_search_by_field("Status Name", patient_program_status_name)
            self.wait_for_loader()

            # Click edit on the first matching row
            self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_EDIT_BUTTON)
            self.wait_for_dom_stability()
            printf(f"Clicked edit for patient program status '{patient_program_status_name}'.")
        except NoSuchElementException as e:
            printf(f"Error finding and editing patient program status '{patient_program_status_name}': {e}")
            raise

    def update_patient_program_status_name(self, suffix):
        """Update the patient program status name by appending a suffix."""
        try:
            current_name = self.get_attribute(self.find_element(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_NAME_INPUT), "value")
            new_name = f"{current_name} {suffix}"
            self.clear_field(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_NAME_INPUT)
            self.send_keys(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_NAME_INPUT, new_name)
            printf(f"Updated patient program status name to '{new_name}'.")
            return new_name
        except NoSuchElementException as e:
            printf(f"Error updating patient program status name: {e}")
            raise

    def find_and_delete_patient_program_status(self, patient_program_status_name):
        """Find a patient program status by name and click delete."""
        try:
            # Search for the patient program status first
            self.perform_patient_program_status_search_by_field("Status Name", patient_program_status_name)
            self.wait_for_loader()

            # Click delete on the first matching row
            self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETE_BUTTON)
            printf(f"Clicked delete for patient program status '{patient_program_status_name}'.")
        except NoSuchElementException as e:
            printf(f"Error finding and deleting patient program status '{patient_program_status_name}': {e}")
            raise

    def confirm_patient_program_status_delete(self):
        """Confirm the patient program status deletion in the dialog."""
        try:
            self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETE_CONFIRM_BUTTON)
            self.wait_for_loader()
            printf("Confirmed patient program status deletion.")
        except NoSuchElementException as e:
            printf(f"Error confirming patient program status deletion: {e}")
            raise

    def delete_patient_program_statuses_with_name_containing(self, substring):
        """Delete all patient program statuses containing the substring in name."""
        deleted_count = 0
        for iteration in range(1, 11):
            printf(f"Iteration {iteration}: Searching for patient program statuses containing '{substring}' in name")
            rows = self._perform_patient_program_status_search_and_get_rows(substring)
            if rows is None:
                break
            if self._delete_first_matching_patient_program_status_by_name(rows, substring):
                deleted_count += 1
                printf(f" (#{deleted_count})")
            else:
                printf(f"No patient program status with name containing '{substring}' found in current results - stopping")
                break
        if iteration == 10:
            printf("Reached maximum iterations (10) - stopping to prevent infinite loop")
        return deleted_count

    def _perform_patient_program_status_search_and_get_rows(self, substring):
        """Perform search by patient program status name containing substring and return valid rows if statuses are found, else None."""
        # Clear any open modal if present
        if self.is_element_visible(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETE_CONFIRMATION_DIALOG, timeout=2):
            self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            sleep(1)

        # Perform search by status name field with the substring
        self.perform_patient_program_status_search_by_field("Status Name", substring)

        # Check if no statuses found
        try:
            self.wait_for_loader()
            no_data_element = self.is_element_visible(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_TABLE_ROWS, timeout=2)
            if not no_data_element:
                printf(f"No patient program statuses found containing '{substring}' in name - cleanup complete")
                return None
        except Exception as e:
            printf(f"Error checking for no data element: {e}")
            return None

        rows = self.find_elements(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_TABLE_ROWS)
        if not rows:
            printf("No table rows found - cleanup complete")
            return None

        first_row_text = rows[0].text.strip()
        if "No statuses found" in first_row_text or first_row_text == "":
            printf(f"No patient program statuses found containing '{substring}' in name - cleanup complete")
            return None

        return rows

    def _delete_first_matching_patient_program_status_by_name(self, rows, substring):
        """Delete the first patient program status in rows whose name contains the substring. Return True if deleted."""
        try:
            for row in rows:
                # Assume status name is in column 1 (td[1])
                name_cell = row.find_element(By.XPATH, ".//td[1]")
                status_name = name_cell.text.strip()
                if substring.lower() in status_name.lower():
                    # Find delete button in the last column
                    delete_button = row.find_element(By.XPATH, ".//td[last()]//button[contains(@id,'delete')]")
                    delete_button.click()
                    sleep(1)
                    self.click(PatientProgramStatusPageLocators.PATIENT_PROGRAM_STATUS_DELETE_CONFIRM_BUTTON)
                    printf(f"Successfully deleted patient program status '{status_name}'")
                    sleep(2)
                    return True
            return False
        except Exception as e:
            printf(f"Error deleting patient program status: {e}")
            return False

    def is_returned_to_patient_program_status_page(self):
        """Check if returned to patient program status page after cancel."""
        return self.check_url_contains(Routes.PROGRAM_TYPE, partial=False)