import random
from datetime import datetime, timedelta
from time import sleep

from selenium.webdriver.common.by import By

from features.commons.locators import UserDashboardPageLocators
from features.pages.base_page import BasePage
from utils.logger import printf


class UserDashboardPage(BasePage):
    """Page object for VPE User Dashboard page."""

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_dashboard(self, page_name="dashboard"):
        """Navigate to the main dashboard page."""
        self.click_dynamic_hamburger_menu_option(page_name)

    def click_dynamic_hamburger_menu_option(self, option_name):
        """Click on a dynamic option in the hamburger menu."""
        try:
            dynamic_locator = UserDashboardPageLocators.HAMBURGER_MENU_OPTION(option_text=option_name)
            self.is_element_visible(dynamic_locator, timeout=2)
            return self.click(dynamic_locator)
        except Exception as e:
            printf(f"Error clicking dynamic menu option '{option_name}': {e}")
            return False

    def wait_for_patient_details_to_load(self):
        """Wait for patient details to load in the dashboard."""
        try:
            self.is_element_visible(UserDashboardPageLocators.PATIENT_INFORMATION_PANEL, timeout=30)
            printf("Patient details loaded successfully.")
            return True
        except Exception as e:
            printf(f"Error waiting for patient details to load: {e}")
            return False

    def set_enrollment_status(self, enrollment_status):
        """Set the enrollment status for a patient."""
        try:
            self.click(UserDashboardPageLocators.ENROLLMENT_STATUS_DROPDOWN)
            self.wait_for_dom_stability()
            self.send_keys(UserDashboardPageLocators.ENROLLMENT_STATUS_SEARCH_INPUT, enrollment_status)
            sleep(0.3)
            self.click(UserDashboardPageLocators.ENROLLMENT_STATUS_OPTION(enrollment_status))
            self.wait_for_dom_stability()
            printf(f"Enrollment status set to '{enrollment_status}'.")
        except Exception as e:
            printf(f"Error setting enrollment status: {e}")

    def set_workflow_status(self, workflow_status):
        """Set the workflow status for a patient."""
        try:
            self.click(UserDashboardPageLocators.WORKFLOW_STATUS_DROPDOWN)
            self.wait_for_dom_stability()
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION(workflow_status))
            self.wait_for_dom_stability()
            printf(f"Workflow status set to '{workflow_status}'.")
        except Exception as e:
            printf(f"Error setting workflow status: {e}")

    def set_appointment_type(self, appointment_type):
        """Set the appointment type for a patient."""
        try:
            self.custom_select_by_locator(UserDashboardPageLocators.APPOINTMENT_TYPE_DROPDOWN,
                                          UserDashboardPageLocators.DROP_DOWN_OPTION(appointment_type))
            printf(f"Appointment type set to '{appointment_type}'.")
        except Exception as e:
            printf(f"Error setting appointment type: {e}")

    def set_first_available_resource(self, user_name):
        """Select the first available resource for a patient."""
        try:
            self.click(UserDashboardPageLocators.SELECT_RESOURCE_DROPDOWN)
            self.wait_for_dom_stability()
            self.send_keys(UserDashboardPageLocators.DROP_DOWN_OPTION_SEARCH, user_name)
            self.wait_for_dom_stability()
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION(user_name))
            printf("First available resource selected.")
        except Exception as e:
            printf(f"Error selecting first available resource: {e}")

    def set_first_available_facility(self):
        """Select the first available facility for a patient."""
        try:
            self.click(UserDashboardPageLocators.SELECT_FACILITY_DROPDOWN)
            self.wait_for_dom_stability()
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION("facility_01"))
            printf("First available facility selected.")
        except Exception as e:
            printf(f"Error selecting first available facility: {e}")

    def set_available_appointment_date_and_slot(self):
        """Select the available appointment date and slot for a patient."""
        try:
            self.click(UserDashboardPageLocators.APPOINTMENT_DATE_BUTTON)
            self.wait_for_dom_stability()
            selected = False

            for month_offset in range(3):
                if self.is_element_visible(UserDashboardPageLocators.NEXT_AVAILABLE_DAY(1), timeout=2):
                    self.click(UserDashboardPageLocators.NEXT_AVAILABLE_DAY(1))
                    self.wait_for_dom_stability()
                    selected = True
                    break

                printf(f"No available appointment date found in month offset {month_offset}.")

                if month_offset < 2:
                    self.click(UserDashboardPageLocators.APPOINTMENT_NEXT_MONTH_BUTTON)
                    self.wait_for_loader()
                    sleep(0.2)

            if not selected:
                raise Exception("No available appointment date found in current or next two months.")

            self.wait_for_loader()
            self.is_element_visible(UserDashboardPageLocators.AVAILABLE_SLOTS_TEXT)
            self.scroll_to_visible_element(UserDashboardPageLocators.COMMENT_TEXTAREA)
            printf(f"Available appointment slot visible.")
            self.click(UserDashboardPageLocators.APPOINTMENT_TIME_BUTTON)
            self.wait_for_dom_stability()

            if not self.is_element_visible(UserDashboardPageLocators.AVAILABLE_SLOTS_TEXT, timeout=5):
                raise Exception("No available appointment time slots found.")

            slot_text = self.get_text(UserDashboardPageLocators.AVAILABLE_SLOTS_TEXT)
            slot_text = slot_text.replace("to", "-").replace("–", "-")
            slot_parts = [part.strip() for part in slot_text.split("-") if part.strip()]
            if len(slot_parts) < 2:
                raise Exception(f"Unexpected slot text format: '{slot_text}'")

            start_time_str = slot_parts[0]
            end_time_str = slot_parts[1]

            slot_start_time = datetime.strptime(start_time_str, "%I:%M %p")
            slot_end_time = datetime.strptime(end_time_str, "%I:%M %p")

            total_minutes = int((slot_end_time - slot_start_time).total_seconds() / 60)
            if total_minutes < 15:
                raise Exception("Available slot is shorter than 15 minutes.")

            available_starts = list(range(0, total_minutes - 15 + 1, 15))
            offset_minutes = random.choice(available_starts)
            start_time = slot_start_time + timedelta(minutes=offset_minutes)
            end_time = start_time + timedelta(minutes=15)

            start_hh = start_time.strftime("%I")
            start_mm = start_time.strftime("%M")
            start_period = start_time.strftime("%p")
            end_hh = end_time.strftime("%I")
            end_mm = end_time.strftime("%M")
            end_period = end_time.strftime("%p")

            self.click(UserDashboardPageLocators.START_HH_INPUT)
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION(start_hh))
            self.click(UserDashboardPageLocators.START_MM_INPUT)
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION(start_mm))
            self.click(UserDashboardPageLocators.START_PERIOD_INPUT)
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION(start_period))

            self.click(UserDashboardPageLocators.END_HH_INPUT)
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION(end_hh))
            self.click(UserDashboardPageLocators.END_MM_INPUT)
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION(end_mm))
            self.click(UserDashboardPageLocators.END_PERIOD_INPUT)
            self.click(UserDashboardPageLocators.DROP_DOWN_OPTION(end_period))

            sleep(1)
            self.click(UserDashboardPageLocators.APPLY_SLOT_BUTTON)

            printf("Available appointment date and 15-minute slot selected.")
        except Exception as e:
            printf(f"Error selecting available appointment date and slot: {e}")

    def set_comment_for_engagement(self):
        """Enter a comment for the patient engagement."""
        try:
            comment = "This is a test comment for the patient engagement."
            self.send_keys(UserDashboardPageLocators.COMMENT_TEXTAREA, comment)
            printf("Comment for engagement entered.")
        except Exception as e:
            printf(f"Error entering comment for engagement: {e}")

    def save_patient_enrollment(self):
        """Save the patient enrollment."""
        try:
            self.click(UserDashboardPageLocators.SAVE_BUTTON)
            self.wait_for_dom_stability()
            printf("Patient enrollment saved.")
        except Exception as e:
            printf(f"Error saving patient enrollment: {e}")

    def is_patient_enrollment_saved(self):
        """Check if the patient enrollment was saved successfully."""
        try:
            return self.is_element_visible(UserDashboardPageLocators.PATIENT_ENROLLMENT_SAVED_NOTIFICATION, timeout=30)
        except Exception as e:
            printf(f"Error checking if patient enrollment was saved: {e}")
            return False
    def click_on_next_patient_button(self):
        """Click on the Next Patient button."""
        try:
            self.click(UserDashboardPageLocators.NEXT_PATIENT_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked on Next Patient button.")
        except Exception as e:
            printf(f"Error clicking on Next Patient button: {e}")

    def is_next_patient_loaded(self):
        """Check if the next patient details are visible in the dashboard."""
        try:
            return self.is_element_visible(UserDashboardPageLocators.NEXT_PATIENT_BUTTON_DISABLED, timeout=30)
        except Exception as e:
            printf(f"Error checking if next patient details are visible: {e}")
            return False