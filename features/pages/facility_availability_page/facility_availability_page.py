from datetime import datetime, timedelta
from time import sleep

from selenium.common import NoSuchElementException

from features.commons.locators import FacilityAvailabilityPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check, get_current_date


class FacilityAvailabilityPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_listing(self):
        self.wait_for_loader()
        if self.is_element_visible(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_CLEAR_BUTTON, timeout=2):
            self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_CLEAR_BUTTON)
            self.wait_for_loader()
            self.is_element_visible(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_DELETE_BUTTON, timeout=30)

    def get_facility_availability_first_row_data(self):
        self.wait_for_loader()
        self.is_element_visible(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_DELETE_BUTTON, timeout=30)
        return extract_table_row_as_dict(self, FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_TABLE)

    def perform_facility_availability_search_by_field(self, field, value):
        try:
            printf(f"Performing facility availability search for field '{field}' with value '{value}'")
            self.wait_for_loader()

            self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_SEARCH_DROPDOWN)
            self.click(FacilityAvailabilityPageLocators.DROPDOWN_OPTION(field))

            if self.is_element_visible(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_CLEAR_BUTTON, timeout=2):
                self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_CLEAR_BUTTON)
                self.wait_for_loader()

            self.send_keys(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_SEARCH_INPUT, value)
            self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_SEARCH_BUTTON)
            self.wait_for_loader(timeout=30)
            return True
        except NoSuchElementException as e:
            printf(f"Error during facility availability search operation: {e}")
            return False

    def verify_facility_availability_search_results(self, search_criteria, search_value):
        self.wait_for_loader(timeout=10)
        self.is_element_visible(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_DELETE_BUTTON, timeout=30)
        return verify_search_results_in_table(
            self,
            search_value,
            FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_TABLE_ROWS,
            search_criteria,
        )

    def click_on_facility_availability_action_button(self, action_button):
        self.wait_for_loader()
        if action_button == "View History":
            self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_HISTORY_BUTTON)
        elif action_button == "Edit":
            self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_EDIT_BUTTON)
        elif action_button == "Delete":
            self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_DELETE_BUTTON)
        else:
            raise AssertionError(f"Action button '{action_button}' not recognized.")

    def verify_facility_availability_operation_history_dialog(self):
        try:
            self.is_element_visible(FacilityAvailabilityPageLocators.OPERATION_HISTORY_DIALOG, timeout=5)
            self.click(FacilityAvailabilityPageLocators.OPERATION_HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException:
            return False

    def is_navigated_to_facility_availability_edit_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.FACILITY_AVAILABILITY_EDIT, partial=False)

    def verify_facility_availability_delete_confirmation_dialog(self):
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(FacilityAvailabilityPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=5)
            self.click(FacilityAvailabilityPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def select_facility_availability_records_per_page(self, records):
        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.PAGE_LIMIT_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION(records),
        )

    def verify_facility_availability_records_per_page(self, records):
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying facility availability rows per page: {e}")
            return False

    def click_add_new_facility_availability(self):
        try:
            self.wait_for_loader()
            self.is_element_visible(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_PAGINATION, timeout=30)
            self.click(FacilityAvailabilityPageLocators.ADD_NEW_FACILITY_AVAILABILITY_BUTTON)
            self.check_url_contains(Routes.ADD_FACILITY_AVAILABILITY, partial=False)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException as e:
            printf(f"Error clicking 'Add Facility Availability' button: {e}")
            return False

    def fill_create_facility_availability_form(self, clinic_name = "HBox Internal",facility_name = "facility_02", timezone = "US/Pacific"):
        """Fills the create facility availability form with provided or default data and returns the filled data as a dictionary."""

        start_date = get_current_date(days_offset=0, years_offset=1)
        end_date = get_current_date(days_offset=30, years_offset=1)

        try:
            self.click(FacilityAvailabilityPageLocators.SELECT_CLINIC_DROPDOWN)
            self.wait_for_dom_stability()
            self.send_keys(FacilityAvailabilityPageLocators.SELECT_SEARCH_CLINIC_INPUT, clinic_name)
            self.wait_for_dom_stability()
            sleep(1)
            self.click(FacilityAvailabilityPageLocators.FACILITY_DROPDOWN_OPTION(clinic_name))
            self.wait_for_dom_stability()
            sleep(1)

            self.click(FacilityAvailabilityPageLocators.SELECT_FACILITY_DROPDOWN)
            self.wait_for_dom_stability()
            self.click(FacilityAvailabilityPageLocators.DROPDOWN_OPTION(facility_name))
            sleep(1)

            self.click(FacilityAvailabilityPageLocators.FROM_DATE_BUTTON)
            self.wait_for_dom_stability()
            self.select_calender_date(start_date)
            sleep(1)
            self.click(FacilityAvailabilityPageLocators.TO_DATE_BUTTON)
            self.wait_for_dom_stability()
            self.select_calender_date(end_date)
            sleep(1)

            self.click(FacilityAvailabilityPageLocators.TIMEZONE_DROPDOWN)
            self.wait_for_dom_stability()
            self.click(FacilityAvailabilityPageLocators.DROPDOWN_OPTION(timezone))
            self.wait_for_dom_stability()

            sleep(1)

            self.select_schedule_slots()

            return {
                "clinic": clinic_name,
                "facility": facility_name,
                "start_date": start_date,
                "end_date": end_date,
                "timezone": timezone,
            }
        except Exception as e:
            printf(f"Error filling create facility availability form: {e}")
            return None

    def select_schedule_slots(self):
        """Selects schedule slots for the facility availability form."""
        try:
            self.click(FacilityAvailabilityPageLocators.SCHEDULE_DAY_CHECKBOX)
            sleep(1)
            self.select_by_visible_text(FacilityAvailabilityPageLocators.START_TIME_HOUR_SELECT,"12")
            self.select_by_visible_text(FacilityAvailabilityPageLocators.START_TIME_MINUTE_SELECT,"00")
            self.select_by_visible_text(FacilityAvailabilityPageLocators.START_TIME_AM_PM_SELECT,"AM")
            self.select_by_visible_text(FacilityAvailabilityPageLocators.END_TIME_HOUR_SELECT,"11")
            self.select_by_visible_text(FacilityAvailabilityPageLocators.END_TIME_MINUTE_SELECT,"45")
            self.select_by_visible_text(FacilityAvailabilityPageLocators.END_TIME_AM_PM_SELECT,"PM")
            sleep(1)
            self.click(FacilityAvailabilityPageLocators.COPY_TO_ALL_DAYS_BUTTON)
            sleep(1)
            printf("Selected times and copied to all days.")
        except NoSuchElementException as e:
            printf(f"Error selecting times: {e}")
            raise

    def submit_create_facility_availability(self):
        try:
            self.click(FacilityAvailabilityPageLocators.CREATE_FACILITY_AVAILABILITY_BUTTON)
            return True
        except NoSuchElementException as e:
            printf(f"Error submitting create facility availability form: {e}")
            return False

    def find_and_edit_facility_availability(self, facility_availability_data):
        try:
            self.navigate_to_listing()
            self.perform_facility_availability_search_by_field("Facility Name", facility_availability_data["facility"])
            self.wait_for_loader()
            self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_EDIT_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException as e:
            printf(f"Error finding and clicking edit for facility availability: {e}")
            return False

    def update_facility_availability_end_date(self, current_end_date):
        try:
            self.click(FacilityAvailabilityPageLocators.TO_DATE_BUTTON)
            self.wait_for_dom_stability()
            new_end_date = get_current_date(days_offset=60, years_offset=1)
            self.select_calender_date(new_end_date)
            return new_end_date
        except NoSuchElementException as e:
            printf(f"Error updating facility availability end date: {e}")
            return current_end_date

    def submit_update_facility_availability(self):
        try:
            self.click(FacilityAvailabilityPageLocators.UPDATE_FACILITY_AVAILABILITY_BUTTON)
            return True
        except NoSuchElementException as e:
            printf(f"Error submitting update facility availability form: {e}")
            return False

    def find_and_delete_facility_availability(self, facility_availability_data):
        try:
            self.navigate_to_listing()
            self.perform_facility_availability_search_by_field("Facility Name", facility_availability_data["facility"])
            self.wait_for_loader()
            self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_DELETE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException as e:
            printf(f"Error finding and clicking delete for facility availability: {e}")
            return False

    def confirm_facility_availability_delete(self):
        try:
            self.click(FacilityAvailabilityPageLocators.DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException as e:
            printf(f"Error confirming facility availability delete: {e}")
            return False

    def cancel_facility_availability_form(self):
        self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_FORM_CANCEL_BUTTON)
        self.wait_for_dom_stability()

    def check_facility_availability_notification(self, expected_message):
        message = expected_message.lower()
        if "created" in message:
            locator = FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_CREATED_NOTIFICATION
        elif "updated" in message:
            locator = FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_UPDATED_NOTIFICATION
        elif "delete" in message:
            locator = FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_DELETE_NOTIFICATION
        else:
            return False
        return self.is_element_visible(locator, timeout=15)

    def is_navigated_to_facility_availability_page(self):
        return self.check_url_contains(Routes.FACILITY_AVAILABILITY, partial=False)
