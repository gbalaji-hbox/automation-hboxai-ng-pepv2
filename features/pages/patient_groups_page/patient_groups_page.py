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