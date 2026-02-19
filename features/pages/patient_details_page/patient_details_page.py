from time import sleep

from selenium.common import NoSuchElementException

from features.commons.locators import PatientDetailsPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf


class PatientDetailsPage(BasePage):
    """Page object for the Patient Details Page (ES Dashboard)."""

    def __init__(self, driver):
        super().__init__(driver)

    def is_on_patient_details_page(self):
        """Check if currently on the patient details page."""
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.PATIENT_DETAILS, partial=True)

    def change_program_status(self, new_status):
        """Change the program status for the patient.
        
        Args:
            new_status: The new status to set (e.g., 'Consent', 'Enrolled', etc.).
            
        Returns:
            bool: True if status was changed successfully, False otherwise.
        """
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability()
            
            # Click on program status dropdown
            printf(f"Attempting to change program status to: {new_status}")
            self.click(PatientDetailsPageLocators.PROGRAM_STATUS_DROPDOWN)
            sleep(1)
            self.wait_for_dom_stability()
            
            # Select the new status
            status_option = PatientDetailsPageLocators.PROGRAM_STATUS_OPTION(new_status)
            self.click(status_option)
            sleep(1)
            self.wait_for_dom_stability()
            
            # Save the change
            self.click(PatientDetailsPageLocators.SAVE_CHANGES_BUTTON)
            self.wait_for_loader()
            self.wait_for_dom_stability()
            sleep(2)
            
            printf(f"Successfully changed program status to: {new_status}")
            return True
            
        except NoSuchElementException as e:
            printf(f"Error changing program status to '{new_status}': {e}")
            return False
    
    def verify_status_update_notification(self):
        """Verify that the status update notification appears."""
        try:
            self.is_element_visible(PatientDetailsPageLocators.STATUS_UPDATED_NOTIFICATION, timeout=10)
            printf("Status update notification appeared.")
            return True
        except NoSuchElementException:
            printf("Status update notification not found.")
            return False
    
    def get_patient_emr_id(self):
        """Get the patient's EMR ID from the page."""
        try:
            emr_element = self.find_element(PatientDetailsPageLocators.PATIENT_EMR_ID)
            emr_id = emr_element.text.strip()
            printf(f"Patient EMR ID: {emr_id}")
            return emr_id
        except NoSuchElementException as e:
            printf(f"Error getting patient EMR ID: {e}")
            return None
    
    def navigate_back_to_dashboard(self):
        """Navigate back to the dashboard from patient details page."""
        try:
            self.click(PatientDetailsPageLocators.BACK_TO_DASHBOARD_BUTTON)
            self.wait_for_loader()
            self.wait_for_dom_stability()
            printf("Navigated back to dashboard.")
            return True
        except NoSuchElementException:
            # If button not found, navigate via URL
            printf("Back button not found, navigating via URL")
            self.navigate_to_url(Routes.get_full_url(Routes.DASHBOARD))
            self.wait_for_loader()
            return True
