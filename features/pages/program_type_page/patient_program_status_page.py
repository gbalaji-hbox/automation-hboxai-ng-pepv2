from time import sleep

from selenium.common import NoSuchElementException

from features.commons.locators import ProgramPageLocators, PatientProgramStatusPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class PatientProgramStatusPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

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