from time import sleep

from faker.proxy import Faker
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from features.commons.locators import PatientGroupsPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, verify_search_results_in_table, row_count_check, get_current_date


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
            self.type(PatientGroupsPageLocators.SEARCH_INPUT, value)
            self.click(PatientGroupsPageLocators.SEARCH_BUTTON)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Failed to perform search: {e}")
            return False

    def verify_search_results(self, search_criteria, search_value, table_name):
        """Verify that the search results are correctly filtered."""
        return verify_search_results_in_table(self, PatientGroupsPageLocators.PATIENT_GROUPS_TABLE, search_criteria, search_value)

    def click_action_button(self, button_type):
        """Click on the specified action button for the first row."""
        try:
            if button_type == "View History":
                self.click(PatientGroupsPageLocators.HISTORY_BUTTON)
            elif button_type == "View":
                self.click(PatientGroupsPageLocators.VIEW_BUTTON)
            elif button_type == "Edit":
                self.click(PatientGroupsPageLocators.EDIT_BUTTON)
            elif button_type == "Delete":
                self.click(PatientGroupsPageLocators.DELETE_BUTTON)
            elif button_type == "Archive":
                self.click(PatientGroupsPageLocators.ARCHIVE_BUTTON)
            self.wait_for_loader()
            return True
        except NoSuchElementException:
            printf(f"Action button '{button_type}' not found.")
            return False

    def verify_history_dialog_opens(self):
        """Verify that the history dialog is open."""
        return self.is_element_visible(PatientGroupsPageLocators.HISTORY_DIALOG)

    def verify_delete_dialog_opens(self):
        """Verify that the delete confirmation dialog is open."""
        return self.is_element_visible(PatientGroupsPageLocators.DELETE_DIALOG)

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

    def click_create_new_group(self):
        """Click on the Create New Group button."""
        self.click(PatientGroupsPageLocators.CREATE_NEW_GROUP_BUTTON)
        self.wait_for_loader()
        """Select an option from the Create New Group menu."""
        try:
            if option == "Create New Group By EMRs":
                self.click(PatientGroupsPageLocators.CREATE_BY_EMRS_OPTION)
            elif option == "Create New Group By Filters":
                self.click(PatientGroupsPageLocators.CREATE_BY_FILTERS_OPTION)
            elif option == "Create New Group By Excel":
                self.click(PatientGroupsPageLocators.CREATE_BY_EXCEL_OPTION)
            self.wait_for_loader()
            return True
        except NoSuchElementException:
            printf(f"Create option '{option}' not found.")
            return False