from datetime import datetime
from time import sleep

from selenium.common.exceptions import NoSuchElementException

from features.commons.locators import SearchPatientsPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class SearchPatientsPage(BasePage):
    """Page object for the Search Patients (Global Search) page."""

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_search_patients(self):
        """Navigate to the Search Patients page and wait for the results table to load."""
        self.click(SearchPatientsPageLocators.RESET_BUTTON)
        self.wait_for_loader()


    def extract_first_patient_data(self) -> dict:
        try:
            self.navigate_to_search_patients()
            self.wait_for_loader()
            patient_data = extract_table_row_as_dict(self, SearchPatientsPageLocators.PATIENTS_TABLE)
            printf(f"Extracted patient data from first row: {patient_data}")
            return patient_data
        except NoSuchElementException as e:
            printf(f"Error extracting patient data from first row: {e}")
            return {}

    def perform_search_by_field(self, field: str, value: str) -> bool:
        try:
            printf(f"Performing patient search for field '{field}' with value '{value}'")
            if not self.get_attribute(SearchPatientsPageLocators.SEARCH_INPUT, "value") == "":
                self.click(SearchPatientsPageLocators.RESET_BUTTON)
            self.wait_for_loader()

            self.click(SearchPatientsPageLocators.SEARCH_TYPE_DROPDOWN)
            self.click(SearchPatientsPageLocators.SEARCH_TYPE_OPTION(field))
            sleep(1)
            if field.lower() == 'dob':
                return self.perform_dob_search(value)
            elif field.lower() == 'clinic name':
                self.select_by_visible_text(SearchPatientsPageLocators.CLINIC_DROPDOWN, value)
                sleep(0.3)
                self.click(SearchPatientsPageLocators.SEARCH_BUTTON)
                self.wait_for_loader(timeout=30)
                return True
            else:
                self.send_keys(SearchPatientsPageLocators.SEARCH_INPUT, value)
                self.click(SearchPatientsPageLocators.SEARCH_BUTTON)
                self.wait_for_loader(timeout=30)
                return True
        except NoSuchElementException as e:
            printf(f"Error performing patient search for field '{field}': {e}")
            return False
        
    def perform_dob_search(self, dob_value: str) -> bool:
        try:
            # Parse the DOB value (format: YYYY-MM-DD)
            date_parts = dob_value.split('-')
            if len(date_parts) != 3:
                printf(f"Invalid DOB format: {dob_value}. Expected YYYY-MM-DD")
                return False

            year, month, day = date_parts

            # Convert numeric month to full month name (e.g. "01" -> "January")
            month_full_name = datetime.strptime(month.zfill(2), "%m").strftime("%B")

            # Select day as zero-padded string (e.g. "05")
            day_formatted = day.zfill(2)

            self.select_by_visible_text(SearchPatientsPageLocators.MONTH_SELECT_DROPDOWN, month_full_name)
            sleep(0.5)

            self.select_by_visible_text(SearchPatientsPageLocators.DAY_SELECT_DROPDOWN, day_formatted)
            sleep(0.5)

            self.select_by_visible_text(SearchPatientsPageLocators.YEAR_SELECT_DROPDOWN, year)
            sleep(0.5)

            self.click(SearchPatientsPageLocators.SEARCH_BUTTON)
            self.wait_for_loader(timeout=30)
            printf(f"Performed DOB search: Year={year}, Month={month_full_name}, Day={day_formatted}")
            return True

        except Exception as e:
            printf(f"Error performing DOB search: {e}")
            return False

    def verify_search_results_contain_patient_data(self, field: str, value: str) -> bool:
        self.wait_for_loader(timeout=10)
        return verify_search_results_in_table(
            self,
            value,
            SearchPatientsPageLocators.PATIENTS_TABLE_ROWS,
            field,
        )

    def search_for_term(self, term: str) -> bool:
        try:
            printf(f"Searching for term: '{term}'")
            self.wait_for_loader()
            self.send_keys(SearchPatientsPageLocators.SEARCH_INPUT, term)
            self.click(SearchPatientsPageLocators.SEARCH_BUTTON)
            self.wait_for_loader(timeout=30)
            return True
        except NoSuchElementException as e:
            printf(f"Error searching for term '{term}': {e}")
            return False

    def is_no_results_message_displayed(self) -> bool:
        return self.is_element_visible(SearchPatientsPageLocators.NO_RESULTS_MESSAGE, timeout=10)

    def click_reset_button(self):
        """Click the Reset button and wait for the results to reload."""
        self.click(SearchPatientsPageLocators.RESET_BUTTON)
        self.wait_for_loader()

    def is_search_cleared_and_results_displayed(self) -> bool:
        try:
            self.wait_for_loader(timeout=10)
            search_input_value = self.get_attribute(
                SearchPatientsPageLocators.SEARCH_INPUT, "value"
            )
            input_cleared = search_input_value == "" or search_input_value is None
            rows_present = (
                self.get_number_of_table_rows(SearchPatientsPageLocators.PATIENTS_TABLE_ROWS) > 0
            )
            printf(f"Search input cleared: {input_cleared}, rows present: {rows_present}")
            return input_cleared and rows_present
        except Exception as e:
            printf(f"Error checking search cleared state: {e}")
            return False

    def select_rows_per_page(self, rows: str):
        self.select_by_visible_text(SearchPatientsPageLocators.PAGE_LIMIT_DROPDOWN, rows)
        self.wait_for_loader()

    def verify_rows_per_page(self, rows: str) -> bool:
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(
                SearchPatientsPageLocators.PATIENTS_TABLE_ROWS
            )
            printf(f"Expected rows per page: {rows}, Actual rows displayed: {actual_count}")
            return row_count_check(rows, actual_count)
        except Exception as e:
            printf(f"Error verifying rows per page: {e}")
            return False

    def click_view_details_for_first_patient(self):
        """Click the View Details action button on the first patient row."""
        self.wait_for_loader()
        self.is_element_visible(SearchPatientsPageLocators.VIEW_DETAILS_BUTTON, timeout=15)
        self.click(SearchPatientsPageLocators.VIEW_DETAILS_BUTTON)
        self.wait_for_loader()

    def is_patient_details_page_loaded(self) -> bool:
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.PATIENT_DETAILS, partial=False)

    def click_back_button(self):
        """Click the Back button on the patient details page."""
        self.click(SearchPatientsPageLocators.BACK_BUTTON)
        self.wait_for_loader()

    def is_back_on_search_patients_page(self) -> bool:
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.SEARCH_PATIENTS, partial=False)
