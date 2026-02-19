from time import sleep

from selenium.common import NoSuchElementException

from features.commons.locators import ScheduledAppointmentsPageLocators, DashboardPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check, to_ddmmyyyy


class ScheduledAppointmentsPage(BasePage):
    """Page object for the Scheduled Appointments page."""

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_listing(self):
        """Navigate to scheduled appointments listing and clear any filters."""
        self.wait_for_loader()
        if self.is_element_visible(ScheduledAppointmentsPageLocators.RESET_BUTTON, timeout=2):
            self.click(ScheduledAppointmentsPageLocators.RESET_BUTTON)
            self.wait_for_loader()

    def click_on_tab(self, tab_name):
        """Click on the specified tab (Virtual or In-Person)."""
        try:
            if self.is_element_visible(DashboardPageLocators.NOTIFICATION_POPUP, timeout=2):
                self.click(DashboardPageLocators.NOTIFICATION_CLOSE_BUTTON)
                sleep(1)

            if tab_name == "Virtual":
                tab_locator = ScheduledAppointmentsPageLocators.VIRTUAL_TAB
            elif tab_name == "In-Person":
                tab_locator = ScheduledAppointmentsPageLocators.IN_PERSON_TAB
            else:
                raise ValueError(f"Unknown tab name: {tab_name}")

            if self.get_attribute(tab_locator, "aria-selected") == "true":
                printf(f"Tab '{tab_name}' is already selected.")
                return
            self.click(tab_locator)
            self.wait_for_dom_stability()
        except NoSuchElementException:
            printf(f"Tab with name '{tab_name}' not found on Scheduled Appointments Page.")
            raise

    def is_tab_active(self, tab_name):
        """Check if the specified tab is active."""
        try:
            if tab_name == "Virtual":
                tab_locator = ScheduledAppointmentsPageLocators.VIRTUAL_TAB
            elif tab_name == "In-Person":
                tab_locator = ScheduledAppointmentsPageLocators.IN_PERSON_TAB
            else:
                return False

            tab_ele = self.find_element(tab_locator)
            return self.get_attribute(tab_ele, "aria-selected") == "true"
        except NoSuchElementException:
            return False

    def is_table_displayed(self):
        """Check if the scheduled appointments table is displayed with records."""
        try:
            self.wait_for_loader()
            rows = self.get_number_of_table_rows(ScheduledAppointmentsPageLocators.SCHEDULED_APPOINTMENTS_TABLE_ROWS)
            return rows > 0
        except NoSuchElementException:
            return False

    def get_first_row_data(self):
        """Get the first row data from the scheduled appointments table."""
        self.wait_for_loader()
        return extract_table_row_as_dict(self, ScheduledAppointmentsPageLocators.SCHEDULED_APPOINTMENTS_TABLE)

    def perform_search_by_field(self, field, value):
        """Perform search by specified field and value."""
        try:
            printf(f"Performing scheduled appointments search for field '{field}' with value '{value}'")
            self.wait_for_loader()
            field_locator_map = {
                "Patient Name": ScheduledAppointmentsPageLocators.PATIENT_NAME_SEARCH_INPUT,
                "Appointment Date": ScheduledAppointmentsPageLocators.APPOINTMENT_DATE_BUTTON,
                "Clinic Name": ScheduledAppointmentsPageLocators.CLINIC_NAME_SEARCH_INPUT,
                "User Name": ScheduledAppointmentsPageLocators.USER_NAME_SEARCH_INPUT,
                "Facility Name": ScheduledAppointmentsPageLocators.FACILITY_NAME_SEARCH_INPUT,
            }

            locator = field_locator_map.get(field)
            if self.is_element_visible(ScheduledAppointmentsPageLocators.RESET_BUTTON, timeout=2):
                self.click(ScheduledAppointmentsPageLocators.RESET_BUTTON)
                self.wait_for_loader()

            if not locator:
                printf(f"Unsupported search field: {field}")
                return False
            if field == "Appointment Date":
                self.click(locator)
                sleep(1)
                date_str = to_ddmmyyyy(value)
                self.select_calender_date(date_str)
                sleep(1)
            else:
                self.send_keys(locator, value)

            sleep(1)

            # Click search button
            self.click(ScheduledAppointmentsPageLocators.SEARCH_BUTTON)
            self.wait_for_loader()
            return True
        except NoSuchElementException as e:
            printf(f"Error during scheduled appointments search operation: {e}")
            return False

    def verify_search_results(self, search_criteria, search_value):
        """Verify search results contain the matching data."""
        self.wait_for_loader(timeout=10)
        return verify_search_results_in_table(
            self,
            search_value,
            ScheduledAppointmentsPageLocators.SCHEDULED_APPOINTMENTS_TABLE_ROWS,
            search_criteria,
        )

    def click_patient_name_button(self):
        """Click on the patient name button in the first row."""
        try:
            self.wait_for_loader()
            self.click(ScheduledAppointmentsPageLocators.PATIENT_NAME_BUTTON)
            self.wait_for_dom_stability()
        except NoSuchElementException:
            printf("Patient name button not found in the table.")
            raise

    def is_navigated_to_patient_details(self):
        """Check if navigated to the patient details page (ES Dashboard)."""
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.PATIENT_DETAILS, partial=True)

    def select_records_per_page(self, records):
        """Select number of records per page from pagination dropdown."""
        try:
            self.select_by_visible_text(ScheduledAppointmentsPageLocators.PAGE_LIMIT_DROPDOWN, records)
            self.wait_for_loader()
        except NoSuchElementException as e:
            printf(f"Error selecting records per page: {e}")
            raise

    def verify_records_per_page(self, records):
        """Verify the number of rows displayed per page matches expected count."""
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(ScheduledAppointmentsPageLocators.SCHEDULED_APPOINTMENTS_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying scheduled appointments rows per page: {e}")
            return False