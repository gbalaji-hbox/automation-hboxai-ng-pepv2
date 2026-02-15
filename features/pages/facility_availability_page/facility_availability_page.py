import random
from datetime import datetime, timedelta

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from features.commons.locators import FacilityAvailabilityPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


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
        add_button_locator = (By.XPATH, "//button[normalize-space()='Add New Facility Availability']")
        self.click(add_button_locator)
        self.is_clickable(FacilityAvailabilityPageLocators.SELECT_CLINIC_DROPDOWN)
        self.wait_for_dom_stability()

    def fill_create_facility_availability_form(self):
        clinic_name = "HBox Internal"
        facility_name = "facility_02"
        base_year = datetime.now().year + random.randint(3, 8)
        start_date = datetime(base_year, 2, 1)
        end_date = datetime(base_year + 1, 1, 31)

        start_date_text = start_date.strftime("%m/%d/%Y")
        end_date_text = end_date.strftime("%m/%d/%Y")

        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.SELECT_CLINIC_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION(clinic_name),
        )
        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.SELECT_FACILITY_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION(facility_name),
        )

        self.click(FacilityAvailabilityPageLocators.FROM_DATE_BUTTON)
        self.select_calender_date(start_date_text)
        self.click(FacilityAvailabilityPageLocators.TO_DATE_BUTTON)
        self.select_calender_date(end_date_text)

        monday_state = self.get_attribute(FacilityAvailabilityPageLocators.MONDAY_CHECKBOX, "aria-checked")
        if str(monday_state).lower() != "true":
            self.click(FacilityAvailabilityPageLocators.MONDAY_CHECKBOX)

        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.MONDAY_START_HOUR_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION("09"),
        )
        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.MONDAY_START_MINUTE_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION("00"),
        )
        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.MONDAY_START_PERIOD_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION("AM"),
        )
        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.MONDAY_END_HOUR_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION("05"),
        )
        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.MONDAY_END_MINUTE_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION("00"),
        )
        self.custom_select_by_locator(
            FacilityAvailabilityPageLocators.MONDAY_END_PERIOD_DROPDOWN,
            FacilityAvailabilityPageLocators.DROPDOWN_OPTION("PM"),
        )

        return {
            "clinic": clinic_name,
            "facility": facility_name,
            "start_date": start_date_text,
            "end_date": end_date_text,
        }

    def submit_create_facility_availability(self):
        self.click(FacilityAvailabilityPageLocators.CREATE_FACILITY_AVAILABILITY_BUTTON)

    def find_and_edit_facility_availability(self, facility_availability_data):
        self.navigate_to_listing()
        self.perform_facility_availability_search_by_field("Facility Name", facility_availability_data["facility"])
        self.wait_for_loader()
        self.click(
            FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_EDIT_BUTTON_BY_VALUES(
                facility_availability_data["clinic"],
                facility_availability_data["facility"],
                facility_availability_data["start_date"],
                facility_availability_data["end_date"],
            )
        )
        self.wait_for_dom_stability()

    def update_facility_availability_end_date(self, current_end_date):
        old_end_date = datetime.strptime(current_end_date, "%m/%d/%Y")
        updated_end_date = (old_end_date + timedelta(days=30)).strftime("%m/%d/%Y")
        self.click(FacilityAvailabilityPageLocators.TO_DATE_BUTTON)
        self.select_calender_date(updated_end_date)
        return updated_end_date

    def submit_update_facility_availability(self):
        self.click(FacilityAvailabilityPageLocators.UPDATE_FACILITY_AVAILABILITY_BUTTON)

    def find_and_delete_facility_availability(self, facility_availability_data):
        self.navigate_to_listing()
        self.perform_facility_availability_search_by_field("Facility Name", facility_availability_data["facility"])
        self.wait_for_loader()
        self.click(
            FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_DELETE_BUTTON_BY_VALUES(
                facility_availability_data["clinic"],
                facility_availability_data["facility"],
                facility_availability_data["start_date"],
                facility_availability_data["end_date"],
            )
        )

    def confirm_facility_availability_delete(self):
        self.click(FacilityAvailabilityPageLocators.DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON)

    def cancel_facility_availability_form(self):
        self.click(FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_FORM_CANCEL_BUTTON)
        self.wait_for_dom_stability()

    def check_facility_availability_notification(self, expected_message):
        message = expected_message.lower()
        if "created" in message:
            locator = FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_CREATED_NOTIFICATION
        elif "updated" in message:
            locator = FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_UPDATED_NOTIFICATION
        elif "delete failed" in message:
            locator = FacilityAvailabilityPageLocators.FACILITY_AVAILABILITY_DELETE_FAILED_NOTIFICATION
        else:
            return False
        return self.is_element_visible(locator, timeout=15)

    def is_navigated_to_facility_availability_page(self):
        return self.check_url_contains(Routes.FACILITY_AVAILABILITY, partial=False)
