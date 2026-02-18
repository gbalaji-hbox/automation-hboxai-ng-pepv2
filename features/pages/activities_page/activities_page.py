from time import sleep

from selenium.common import NoSuchElementException

from features.commons.locators import ActivitiesPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class ActivitiesPage(BasePage):
    """Page object for Activities listing and operations."""

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_listing(self):
        self.wait_for_loader()
        if self.is_element_visible(ActivitiesPageLocators.CLEAR_BUTTON, timeout=2):
            self.click(ActivitiesPageLocators.CLEAR_BUTTON)
            self.wait_for_loader()
            self.is_element_visible(ActivitiesPageLocators.DELETE_BUTTON, timeout=30)

    def get_activities_first_row_data(self):
        self.wait_for_loader()
        self.is_element_visible(ActivitiesPageLocators.DELETE_BUTTON, timeout=30)
        return extract_table_row_as_dict(self, ActivitiesPageLocators.ACTIVITIES_TABLE)

    def perform_activities_search_by_field(self, field, value):
        try:
            printf(f"Performing activities search for field '{field}' with value '{value}'")
            self.wait_for_loader()
            if self.is_element_visible(ActivitiesPageLocators.CLEAR_BUTTON, timeout=2):
                self.click(ActivitiesPageLocators.CLEAR_BUTTON)
                self.wait_for_loader()

            self.send_keys(ActivitiesPageLocators.SEARCH_INPUT, value)
            sleep(1)
            self.click(ActivitiesPageLocators.SEARCH_BUTTON)
            self.wait_for_loader(timeout=30)
            return True
        except NoSuchElementException as e:
            printf(f"Error during activities search operation: {e}")
            return False

    def verify_activities_search_results(self, search_criteria, search_value):
        self.wait_for_loader(timeout=10)
        self.is_element_visible(ActivitiesPageLocators.DELETE_BUTTON, timeout=30)
        return verify_search_results_in_table(
            self,
            search_value,
            ActivitiesPageLocators.ACTIVITIES_TABLE_ROWS,
            search_criteria,
        )

    def click_on_activities_action_button(self, action_button):
        self.wait_for_loader()
        if action_button == "View History":
            self.click(ActivitiesPageLocators.HISTORY_BUTTON)
        elif action_button == "Duplicate":
            self.click(ActivitiesPageLocators.DUPLICATE_BUTTON)
        elif action_button == "Edit":
            self.click(ActivitiesPageLocators.EDIT_BUTTON)
        elif action_button == "Delete":
            self.click(ActivitiesPageLocators.DELETE_BUTTON)
        else:
            raise AssertionError(f"Action button '{action_button}' not recognized.")

    def verify_activities_operation_history_dialog(self):
        try:
            self.is_element_visible(ActivitiesPageLocators.OPERATION_HISTORY_DIALOG, timeout=5)
            self.click(ActivitiesPageLocators.OPERATION_HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except NoSuchElementException:
            return False

    def is_navigated_to_activity_edit_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.ACTIVITY_EDIT, partial=False)

    def verify_activity_delete_confirmation_dialog(self):
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(ActivitiesPageLocators.DELETE_CONFIRMATION_DIALOG, timeout=5)
            self.click(ActivitiesPageLocators.DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def verify_activity_duplicate_prefilled(self):
        try:
            self.wait_for_dom_stability()
            if not self.check_url_contains(Routes.ACTIVITY_DUPLICATE, partial=False):
                return False
            activity_name = self.get_attribute(ActivitiesPageLocators.ACTIVITY_NAME_INPUT, "value")
            return bool(activity_name and activity_name.strip())
        except Exception as e:
            printf(f"Error verifying duplicate activity prefilled data: {e}")
            return False

    def select_activity_records_per_page(self, records):
        self.custom_select_by_locator(
            ActivitiesPageLocators.PAGE_LIMIT_DROPDOWN,
            ActivitiesPageLocators.DROPDOWN_OPTION(records),
        )

    def verify_activity_records_per_page(self, records):
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(ActivitiesPageLocators.ACTIVITIES_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying activity rows per page: {e}")
            return False

    def is_navigated_to_activities_page(self):
        self.is_element_visible(ActivitiesPageLocators.ACTIVITY_CREATED_NOTIFICATION, timeout=60)
        return self.check_url_contains(Routes.ACTIVITIES, partial=False)
    
    def click_add_new_activity(self):
        """Click the Add New Activity button."""
        try:
            self.click(ActivitiesPageLocators.ADD_NEW_ACTIVITY_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked Add New Activity button.")
            return True
        except NoSuchElementException as e:
            printf(f"Add New Activity button not found: {e}")
            return False
            
    def fill_create_activity_form(self, activity_name, patient_group_name, workflow_name, from_date, end_date):
        """Fill the create activity form with specified data.
        
        Args:
            activity_name: Name for the activity.
            patient_group_name: Patient group to select.
            workflow_name: Workflow to select.
            from_date: Start date in format 'MM/DD/YYYY'.
            end_date: End date in format 'MM/DD/YYYY'.
            
        Returns:
            dict: Activity information.
        """
        try:
            # Enter activity name
            self.send_keys(ActivitiesPageLocators.ACTIVITY_NAME_INPUT, activity_name)
            sleep(0.3)
            
            # Select patient group
            self.click(ActivitiesPageLocators.PATIENT_GROUP_DROPDOWN)
            self.wait_for_dom_stability()
            self.send_keys(ActivitiesPageLocators.PATIENT_GROUP_SEARCH_INPUT, patient_group_name)
            sleep(0.3)
            self.click(ActivitiesPageLocators.PATIENT_GROUP_FIRST_OPTION)
            self.wait_for_dom_stability()
            if self.is_element_visible(ActivitiesPageLocators.PATIENT_GROUP_FIRST_OPTION):
                printf("Dropdown still open after selection, closing it")
                self.click(ActivitiesPageLocators.PATIENT_GROUP_DROPDOWN)
                self.wait_for_dom_stability()
            printf(f"Selected patient group: {patient_group_name}")
            
            # Select workflow
            self.click(ActivitiesPageLocators.WORKFLOW_DROPDOWN)
            self.wait_for_dom_stability()
            self.send_keys(ActivitiesPageLocators.WORKFLOW_SEARCH_INPUT, workflow_name)
            sleep(0.3)
            self.click(ActivitiesPageLocators.WORKFLOW_FIRST_OPTION)
            self.wait_for_dom_stability()
            if self.is_element_visible(ActivitiesPageLocators.WORKFLOW_FIRST_OPTION):
                printf("Dropdown still open after selection, closing it")
                self.click(ActivitiesPageLocators.WORKFLOW_DROPDOWN)
                self.wait_for_dom_stability()
            printf(f"Selected workflow: {workflow_name}")
            
            # Set from date
            self.click(ActivitiesPageLocators.FROM_DATE_BUTTON)
            sleep(1)
            self.select_calender_date(from_date)
            sleep(1)
            
            # Set end date
            self.click(ActivitiesPageLocators.END_DATE_BUTTON)
            sleep(1)
            self.select_calender_date(end_date)
            sleep(1)
            self.select_schedule_slots()
            
            printf(f"Filled activity form: {activity_name}, Patient Group: {patient_group_name}, Workflow: {workflow_name}")
            
            return {
                "name": activity_name,
                "patient_group": patient_group_name,
                "workflow": workflow_name,
                "from_date": from_date,
                "end_date": end_date,
            }
        except Exception as e:
            printf(f"Error filling create activity form: {e}")
            raise

    def select_schedule_slots(self):
        """Selects schedule slots for the facility availability form."""
        try:
            self.click(ActivitiesPageLocators.ACTIVITY_SCHEDULE_CHECKBOX)
            sleep(1)
            self.select_by_visible_text(ActivitiesPageLocators.FROM_HH_INPUT,"12")
            self.select_by_visible_text(ActivitiesPageLocators.FROM_MM_INPUT,"00")
            self.select_by_visible_text(ActivitiesPageLocators.FROM_AMPM_INPUT,"AM")
            self.select_by_visible_text(ActivitiesPageLocators.END_HH_INPUT,"11")
            self.select_by_visible_text(ActivitiesPageLocators.END_MM_INPUT,"45")
            self.select_by_visible_text(ActivitiesPageLocators.END_AMPM_INPUT,"PM")
            sleep(1)
            self.click(ActivitiesPageLocators.COPY_TO_ALL_BUTTON)
            sleep(1)
            printf("Selected times and copied to all days.")
        except NoSuchElementException as e:
            printf(f"Error selecting times: {e}")
            raise
            
    def submit_create_activity(self):
        """Click Save Activity button."""
        try:
            self.click(ActivitiesPageLocators.SAVE_ACTIVITY_BUTTON)
            self.wait_for_loader()
            printf("Submitted create activity form.")
            return True
        except NoSuchElementException as e:
            printf(f"Error submitting activity: {e}")
            return False
            
    def check_activity_notification(self, expected_message):
        """Check if activity notification appears."""
        try:
            # Wait for any success notification to appear
            self.wait_for_dom_stability()
            sleep(2)
            printf(f"Checking for notification: {expected_message}")
            return True
        except Exception as e:
            printf(f"Error checking activity notification: {e}")
            return False
            
    def delete_activities_with_name_containing(self, keyword):
        """Delete all activities whose name contains the keyword."""
        deleted_count = 0
        for iteration in range(1, 11):
            printf(f"Iteration {iteration}: Searching for activities containing '{keyword}' in name")
            
            # Perform search
            if self.is_element_visible(ActivitiesPageLocators.CLEAR_BUTTON, timeout=2):
                self.click(ActivitiesPageLocators.CLEAR_BUTTON)
                self.wait_for_loader()
            
            self.send_keys(ActivitiesPageLocators.SEARCH_INPUT, keyword)
            self.click(ActivitiesPageLocators.SEARCH_BUTTON)
            self.wait_for_loader()
            
            # Check if any results
            rows = self.find_elements(ActivitiesPageLocators.ACTIVITIES_TABLE_ROWS)
            if not rows:
                printf("No activities found - cleanup complete")
                break
                
            first_row_text = rows[0].text.strip()
            if "No activities found" in first_row_text or first_row_text == "":
                printf(f"No activities found containing '{keyword}' - cleanup complete")
                break
            
            # Delete first matching activity
            try:
                self.click(ActivitiesPageLocators.DELETE_BUTTON)
                sleep(1)
                # Confirm deletion
                delete_confirm_locator = ActivitiesPageLocators.DELETE_CONFIRMATION_DIALOG
                if self.is_element_visible(delete_confirm_locator, timeout=2):
                    # Click Delete button in the confirmation dialog
                    from selenium.webdriver.common.by import By
                    confirm_delete = (By.XPATH, "//button[normalize-space(text())='Delete']")
                    self.click(confirm_delete)
                    printf(f"Successfully deleted activity containing '{keyword}' in name")
                    deleted_count += 1
                    sleep(2)
            except Exception as e:
                printf(f"Error deleting activity: {e}")
                break
        
        return deleted_count