from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from features.commons.locators import PatientGroupsPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check


class PatientGroupsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    def get_first_row_data(self):
        self.wait_for_loader()
        return extract_table_row_as_dict(self, PatientGroupsPageLocators.PATIENT_GROUPS_TABLE)

    def perform_search_by_field(self, field, value):
        """Perform search in the patient groups table by specified field and value."""
        try:
            printf(f"Performing search for field '{field}' with value '{value}'")
            # For patient groups, the search is by Group Name, and input is direct
            self.send_keys(PatientGroupsPageLocators.SEARCH_INPUT, value)
            self.click(PatientGroupsPageLocators.SEARCH_BUTTON)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Failed to perform search: {e}")
            return False

    def verify_search_results(self, search_criteria, search_value):
        """Verify that the search results are correctly filtered."""
        return verify_search_results_in_table(
            self,
            search_value,
            PatientGroupsPageLocators.PATIENT_GROUPS_TABLE_ROWS,
            search_criteria
        )

    def click_action_button(self, button_type):
        """Click on the specified action button for the first row."""
        try:
            if button_type == "View History":
                self.click(PatientGroupsPageLocators.HISTORY_BUTTON)
            elif button_type == "Edit":
                self.click(PatientGroupsPageLocators.EDIT_BUTTON)
            elif button_type == "Delete":
                self.click(PatientGroupsPageLocators.DELETE_BUTTON)
            elif button_type == "Archive":
                self.click(PatientGroupsPageLocators.ARCHIVE_BUTTON)
            elif button_type == "Duplicate":
                self.click(PatientGroupsPageLocators.DUPLICATE_BUTTON)
            self.wait_for_loader()
            return True
        except NoSuchElementException:
            printf(f"Action button '{button_type}' not found.")
            return False

    def verify_history_dialog_opens(self):
        """Verify that the history dialog is open."""
        result = self.is_element_visible(PatientGroupsPageLocators.HISTORY_DIALOG)
        sleep(1)
        self.click(PatientGroupsPageLocators.HISTORY_DIALOG_CLOSE_BUTTON)
        return result

    def is_navigated_to_edit_page(self):
        """Verify that the Edit Patient Group page is loaded."""
        result = self.check_url_contains(Routes.EDIT_PATIENT_GROUP, partial=False)
        sleep(1)
        self.navigate_back()
        return result

    def verify_delete_dialog_opens(self):
        """Verify that the delete confirmation dialog is open."""
        result = self.is_element_visible(PatientGroupsPageLocators.DELETE_DIALOG)
        sleep(1)
        self.click(PatientGroupsPageLocators.DELETE_DIALOG_CANCEL_BUTTON)
        return result

    def verify_archive_dialog_opens(self):
        """Verify that the archive confirmation dialog is open."""
        result = self.is_element_visible(PatientGroupsPageLocators.ARCHIVE_DIALOG)
        sleep(1)
        self.click(PatientGroupsPageLocators.ARCHIVE_DIALOG_CANCEL_BUTTON)
        return result

    def is_navigated_to_duplicate_page(self):
        """Verify that the Duplicate Patient Group details page is loaded."""
        result = self.check_url_contains(Routes.DUPLICATE_PATIENT_GROUP, partial=False)
        sleep(1)
        self.navigate_back()
        return result

    def select_records_per_page(self, records):
        """Select the number of records to display per page."""
        try:
            self.click(PatientGroupsPageLocators.PAGE_LIMIT_DROPDOWN)
            option_locator = (By.XPATH, f"//div[@role='option']/span[normalize-space(text())='{records}']")
            self.click(option_locator)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Failed to select records per page: {e}")
            return False

    def verify_patient_group_records_per_page(self, records):
        """Verify that the table displays the expected number of records per page."""
        try:
            self.wait_for_loader()
            self.wait_for_dom_stability_full()
            actual_count = self.get_number_of_table_rows(PatientGroupsPageLocators.PATIENT_GROUPS_TABLE_ROWS)
            printf(f"Expected rows per page: {records}, Actual rows displayed: {actual_count}")
            return row_count_check(records, actual_count)
        except Exception as e:
            printf(f"Error verifying rows per page: {e}")
            return False

    def click_create_new_group(self):
        """Click on the 'Create New Group' button."""
        try:
            self.wait_for_loader()
            self.is_element_visible(PatientGroupsPageLocators.HISTORY_BUTTON)
            self.click(PatientGroupsPageLocators.CREATE_NEW_GROUP_BUTTON)
            self.wait_for_dom_stability()
            return True
        except Exception as e:
            printf(f"Failed to click 'Create New Group' button: {e}")
            return False

    def select_create_option(self, option):
        """Select an option from the create menu."""
        try:
            # Map accepted option strings (lowercased) to locator constants
            option_map = {
                "create new group by emrs": PatientGroupsPageLocators.CREATE_BY_EMRS_OPTION,
                "create new group by filters": PatientGroupsPageLocators.CREATE_BY_FILTERS_OPTION,
                "create new group by excel": PatientGroupsPageLocators.CREATE_BY_EXCEL_OPTION,
            }

            key = option.strip().lower()
            option_locator = option_map.get(key)
            if not option_locator:
                printf(f"Unknown create option '{option}'. Available options: {list(option_map.keys())}")
                return False

            self.click(option_locator)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Failed to select create option '{option}': {e}")
            return False

    def verify_navigation_to_create_page(self, page):
        """Verify that navigation to the expected create page occurred."""
        try:
            page_routes = {
                "Create Group By EMRs": Routes.CREATE_NEW_PATIENT_GROUP_BY_EMRS,
                "Create Group By Filters": Routes.CREATE_NEW_PATIENT_GROUP_BY_FILTERS,
                "Create Group By Excel": Routes.CREATE_NEW_PATIENT_GROUP_BY_EXCEL,
            }
            expected_route = page_routes.get(page)
            if not expected_route:
                printf(f"Unknown page '{page}'. Available pages: {list(page_routes.keys())}")
                return False

            result = self.check_url_contains(expected_route, partial=False)
            sleep(1)
            self.click(PatientGroupsPageLocators.BREADCRUMBS_BACK_BUTTON)
            return result
        except Exception as e:
            printf(f"Failed to verify navigation to create page '{page}': {e}")
            return False

    def click_archived_groups(self):
        """Click on the 'Archived Groups' button."""
        try:
            self.click(PatientGroupsPageLocators.ARCHIVED_GROUPS_BUTTON)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Failed to click 'Archived Groups' button: {e}")
            return False

    def verify_navigation_to_archived_groups_page(self):
        """Verify that navigation to the Archived Patient Groups page occurred."""
        try:
            result = self.check_url_contains(Routes.ARCHIVED_PATIENT_GROUPS, partial=False)
            sleep(1)
            self.click(PatientGroupsPageLocators.BREADCRUMBS_BACK_BUTTON)
            return result
        except Exception as e:
            printf(f"Failed to verify navigation to Archived Patient Groups page: {e}")
            return False

    def apply_filters_for_patient_group(self, clinic=None, facility=None, provider=None):
        """Apply filters for creating patient group by filters."""
        try:
            self.wait_for_loader()
            if clinic:
                self.click(PatientGroupsPageLocators.FILTER_BUTTON)
                self.wait_for_dom_stability()
                self.click(PatientGroupsPageLocators.FILTERS_CLINIC_DROPDOWN)
                self.wait_for_dom_stability()
                self.send_keys(PatientGroupsPageLocators.FILTER_DROPDOWN_SEARCH_INPUT, clinic)
                self.wait_for_dom_stability()
                self.click(PatientGroupsPageLocators.FILTER_DROPDOWN_SEARCH_OPTION(clinic))
                self.wait_for_dom_stability()

            self.click(PatientGroupsPageLocators.CREATE_BY_FILTERS_APPLY_BUTTON)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Failed to apply filters: {e}")
            return False

    def select_patients_from_table(self, count=2):
        """Select the first 'count' patients from the patient selection table."""
        try:
            for i in range(1, count + 1):
                self.click(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(i))
            return True
        except Exception as e:
            printf(f"Failed to select patients: {e}")
            return False

    def extract_emr_ids_from_selected_patients(self, count=2):
        """Extract EMR IDs from the first 'count' selected patients."""
        emr_ids = []
        try:
            self.is_element_visible(PatientGroupsPageLocators.FILTER_APPLIED_NOTIFICATION)
            sleep(5)
            for i in range(1, count + 1):
                emr_element = self.find_element(PatientGroupsPageLocators.PATIENT_TABLE_ROW_EMR(i))
                emr_id = emr_element.text.strip()
                emr_ids.append(emr_id)
            printf(f"Extracted EMR IDs: {emr_ids}")
            return emr_ids
        except Exception as e:
            printf(f"Failed to extract EMR IDs: {e}")
            return []

    def return_to_patient_groups_page(self):
        """Return to the Patient Groups page."""
        try:
            self.click(PatientGroupsPageLocators.BREADCRUMBS_BACK_BUTTON)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Failed to return to Patient Groups page: {e}")
            return False

    def click_create_group_button(self):
        """Click the Create Group button."""
        try:
            self.click(PatientGroupsPageLocators.CREATE_GROUP_BUTTON)
            self.wait_for_dom_stability()
            return True
        except Exception as e:
            printf(f"Failed to click Create Group button: {e}")
            return False

    def enter_group_name_and_note(self):
        """Enter group name and save the patient group."""
        try:
            group_name = f"Automation Group {self.faker.unique.random_int(1000, 9999)}"
            note = f"Note for {group_name} created by automation test. \
            \nThis group was created to verify the functionality of creating patient groups by filters."
            self.click_create_group_button()
            self.send_keys(PatientGroupsPageLocators.GROUP_NAME_INPUT, group_name)
            if note:
                self.send_keys(PatientGroupsPageLocators.GROUP_NOTE_TEXTAREA, note)
            self.click(PatientGroupsPageLocators.GROUP_NAME_SAVE_BUTTON)
            return group_name
        except Exception as e:
            printf(f"Failed to name and save patient group: {e}")
            return False

    def create_patient_group_by_emrs(self, clinic, emr_ids):
        """Create patient group by EMRs."""
        try:
            # Select clinic
            self.click(PatientGroupsPageLocators.CREATE_BY_EMRS_CLINIC_DROPDOWN)
            self.wait_for_dom_stability()
            self.send_keys(PatientGroupsPageLocators.FILTER_DROPDOWN_SEARCH_INPUT, clinic)
            self.wait_for_dom_stability()
            self.click(PatientGroupsPageLocators.CREATE_BY_EMRS_CLINIC_OPTION(clinic))
            self.wait_for_dom_stability()

            # Enter EMR IDs
            emr_string = ", ".join(emr_ids)
            self.send_keys(PatientGroupsPageLocators.CREATE_BY_EMRS_TEXTBOX, emr_string)

            # Apply
            self.click(PatientGroupsPageLocators.CREATE_BY_EMRS_APPLY_BUTTON)
            self.is_element_visible(PatientGroupsPageLocators.EMR_SEARCH_COMPLETED_NOTIFICATION)
            return True
        except Exception as e:
            printf(f"Failed to create patient group by EMRs: {e}")
            return False

    def verify_group_created_successfully(self):
        """Verify that the patient group was created successfully."""
        try:
            return self.is_element_visible(PatientGroupsPageLocators.GROUP_CREATED_NOTIFICATION)
        except Exception as e:
            printf(f"Failed to verify group creation: {e}")
            return False

    def find_group_and_click_edit(self, group_name):
        """Find the created patient group in the list and click edit."""
        try:
            self.wait_for_dom_stability_full()
            self.perform_search_by_field("Group Name", group_name)
            sleep(1)
            self.wait_for_dom_stability()
            self.click_action_button("Edit")
            self.is_element_visible(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(1), timeout=10)
            return True
        except Exception as e:
            printf(f"Failed to find group '{group_name}' and click edit: {e}")
            return False

    def update_group_name(self):
        """Update the patient group name."""
        try:
            self.click(PatientGroupsPageLocators.GROUP_NAME_EDIT_BUTTON)
            self.wait_for_dom_stability()
            new_group_name = f"{self.get_attribute(PatientGroupsPageLocators.GROUP_NAME_EDIT_FIELD, "value")} - Edited"
            self.send_keys(PatientGroupsPageLocators.GROUP_NAME_EDIT_FIELD, new_group_name)
            sleep(1)
            self.click(PatientGroupsPageLocators.GROUP_NAME_EDIT_SAVE_BUTTON)
            return new_group_name
        except Exception as e:
            printf(f"Failed to update group name: {e}")
            return False

    def verify_group_name_updated_successfully(self):
        """Verify that the patient group name was updated successfully."""
        try:
            return self.is_element_visible(PatientGroupsPageLocators.GROUP_NAME_UPDATED_NOTIFICATION)
        except Exception as e:
            printf(f"Failed to verify group name update: {e}")
            return False

    def click_add_patients_button(self):
        """Click the add patients button for the edited patient group."""
        try:
            self.is_element_visible(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(1), timeout=10)
            self.click(PatientGroupsPageLocators.GROUP_ADD_PATIENTS_BUTTON)
            self.wait_for_dom_stability()
            self.check_url_contains(Routes.ADD_PATIENTS_TO_GROUP, partial=False)
            return True
        except Exception as e:
            printf(f"Failed to click add patients button: {e}")
            return False

    def select_patients(self):
        """Select patients to add to the group."""
        try:
            self.is_element_visible(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(1), timeout=10)
            self.click(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(1))
            return True
        except Exception as e:
            printf(f"Failed to select patients: {e}")
            return False

    def click_add_selected_button(self):
        """Click the add selected button to add patients to the group."""
        try:
            self.click(PatientGroupsPageLocators.GROUP_ADD_SELECTED_BUTTON)
            return True
        except Exception as e:
            printf(f"Failed to click add selected button: {e}")
            return False

    def verify_patients_added_successfully(self):
        """Verify that the patients were added to the patient group successfully."""
        try:
            return self.is_element_visible(PatientGroupsPageLocators.GROUP_PATIENT_ADDED_NOTIFICATION)
        except Exception as e:
            printf(f"Failed to verify patients added: {e}")
            return False

    def click_remove_patients_button(self):
        """Click the remove patients button for the edited patient group."""
        try:
            self.is_element_visible(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(1), timeout=10)
            self.click(PatientGroupsPageLocators.GROUP_REMOVE_PATIENTS_BUTTON)
            self.wait_for_dom_stability()
            return True
        except Exception as e:
            printf(f"Failed to click remove patients button: {e}")
            return False

    def select_patient_to_remove(self):
        """Select the first patient in the table to be removed."""
        try:
            self.is_element_visible(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(1), timeout=10)
            self.click(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(1))
            return True
        except Exception as e:
            printf(f"Failed to select patient to remove: {e}")
            return False

    def click_remove_selected_button(self):
        """Click the remove selected button to remove patients from the group."""
        try:
            self.click(PatientGroupsPageLocators.GROUP_REMOVE_SELECTED_BUTTON)
            return True
        except Exception as e:
            printf(f"Failed to click remove selected button: {e}")
            return False

    def verify_patients_removed_successfully(self):
        """Verify that the patients were removed from the patient group successfully."""
        try:
            return self.is_element_visible(PatientGroupsPageLocators.GROUP_PATIENT_REMOVED_NOTIFICATION)
        except Exception as e:
            printf(f"Failed to verify patients removed: {e}")
            return False

    def return_to_patient_groups_list(self):
        """Return to the patient groups list page."""
        try:
            self.click(PatientGroupsPageLocators.EDIT_BACK_BUTTON)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Failed to return to patient groups list: {e}")
            return False

    def click_delete_patients_button(self, updated_group_name):
        """Click the delete button for the edited patient group."""
        try:
            self.is_element_visible(PatientGroupsPageLocators.PATIENT_TABLE_ROW_CHECKBOX(1), timeout=10)
            self.perform_search_by_field("Group Name", updated_group_name)
            sleep(1)
            self.wait_for_dom_stability()
            self.click_action_button("Delete")
            self.is_element_visible(PatientGroupsPageLocators.DELETE_DIALOG)
            return True
        except Exception as e:
            printf(f"Failed to click delete button: {e}")
            return False

    def confirm_delete_patient_group_button(self):
        """Click the confirm delete button to delete the patient group."""
        try:
            self.click(PatientGroupsPageLocators.DELETE_DIALOG_DELETE_BUTTON)
            return True
        except Exception as e:
            printf(f"Failed to click confirm delete button: {e}")
            return False

    def verify_the_group_deleted_successfully(self):
        """Verify that the patient group was deleted successfully."""
        try:
            return self.is_element_visible(PatientGroupsPageLocators.GROUP_DELETED_NOTIFICATION)
        except Exception as e:
            printf(f"Failed to verify patient group deletion: {e}")
            return False

    def delete_all_automation_patient_groups(self, keyword):
        """Delete all patient groups containing 'Automation' in their name."""
        deleted_count = 0
        self.is_element_visible(PatientGroupsPageLocators.HISTORY_BUTTON)
        for iteration in range(1, 11):
            printf(f"Iteration {iteration}: Searching for patient groups containing '{keyword}' in name")
            rows = self._perform_search_and_get_patient_group_rows(keyword)
            if rows is None:
                break
            if self._delete_first_matching_patient_group_by_name(rows, keyword):
                deleted_count += 1
                printf(f" (#{deleted_count})")
            else:
                printf(f"No Patient group with name containing '{keyword}' found in current results - stopping")
                break
        if iteration == 10:
            printf("Reached maximum iterations (10) - stopping to prevent infinite loop")
        return deleted_count

    def _perform_search_and_get_patient_group_rows(self, keyword):
        """Perform search for patient groups containing keyword and return table rows."""
        try:
            if self.get_attribute(PatientGroupsPageLocators.SEARCH_INPUT, "value"):
                printf("Clearing existing search input before performing new search")
                self.clear_field(PatientGroupsPageLocators.SEARCH_INPUT)
                self.click(PatientGroupsPageLocators.SEARCH_BUTTON)
                sleep(1)

            self.perform_search_by_field("Group Name", keyword)
            self.wait_for_loader()
            rows = self.find_elements(PatientGroupsPageLocators.PATIENT_GROUPS_TABLE_ROWS)
            return rows
        except Exception as e:
            printf(f"Failed to perform search and get rows for '{keyword}': {e}")
            return None

    def _delete_first_matching_patient_group_by_name(self, rows, keyword):
        """Delete the first patient group in the rows that contains the keyword in its name."""
        try:
            for row in rows:
                name_cell = row.find_element(By.XPATH, ".//td[1]")
                name = name_cell.text.strip()
                if keyword in name:
                    delete_button = row.find_element(By.XPATH, ".//td[4]//button[contains(@id,'delete')]")
                    delete_button.click()
                    sleep(1)
                    self.click(PatientGroupsPageLocators.DELETE_DIALOG_DELETE_BUTTON)
                    printf(f"Successfully deleted user group '{name}'")
                    self.is_element_visible(PatientGroupsPageLocators.GROUP_DELETED_NOTIFICATION)
                    return True
            return False  # No matching group found in current rows
        except Exception as e:
            printf(f"Failed to delete first matching patient group: {e}")
            return False