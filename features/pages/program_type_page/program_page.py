from time import sleep

from selenium.common import NoSuchElementException

from features.commons.locators import ProgramPageLocators, PatientProgramStatusPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class ProgramPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

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