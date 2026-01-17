from time import sleep

from selenium.webdriver.common.by import By
from features.commons.locators import ProgramTypePageLocators
from features.pages.base_page import BasePage
from utils.logger import printf


class ProgramTypePage(BasePage):
    """Page object for the Program Type & Patient Program Status page."""

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_program_type(self):
        """Navigate to the program type page."""
        from features.commons.routes import Routes
        self.driver.get(Routes.get_full_url(Routes.PROGRAM_TYPE))

    def verify_page_title(self, expected_title="Program Type & Patient Program Status"):
        """Verify the page title."""
        try:
            title_element = self.find_element(ProgramTypePageLocators.PAGE_TITLE)
            actual_title = title_element.text
            return actual_title == expected_title
        except Exception as e:
            printf(f"Error verifying page title: {e}")
            return False

    def verify_program_tab_active(self):
        """Verify Program tab is active by default."""
        try:
            program_tab = self.find_element(ProgramTypePageLocators.PROGRAM_TAB)
            return "active" in program_tab.get_attribute("class").lower() or program_tab.get_attribute("aria-selected") == "true"
        except Exception as e:
            printf(f"Error verifying program tab active: {e}")
            return False

    def verify_patient_program_status_tab_inactive(self):
        """Verify Patient Program Status tab is inactive by default."""
        try:
            status_tab = self.find_element(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_TAB)
            return not ("active" in status_tab.get_attribute("class").lower() or status_tab.get_attribute("aria-selected") == "true")
        except Exception as e:
            printf(f"Error verifying status tab inactive: {e}")
            return False

    def switch_to_patient_program_status_tab(self):
        """Switch to Patient Program Status tab."""
        self.click(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_TAB)
        self.wait_for_loader()

    def verify_patient_program_status_tab_active(self):
        """Verify Patient Program Status tab is active after switching."""
        try:
            status_tab = self.find_element(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_TAB)
            return "active" in status_tab.get_attribute("class").lower() or status_tab.get_attribute("aria-selected") == "true"
        except Exception as e:
            printf(f"Error verifying status tab active: {e}")
            return False

    def verify_program_tab_inactive(self):
        """Verify Program tab is inactive after switching."""
        try:
            program_tab = self.find_element(ProgramTypePageLocators.PROGRAM_TAB)
            return not ("active" in program_tab.get_attribute("class").lower() or program_tab.get_attribute("aria-selected") == "true")
        except Exception as e:
            printf(f"Error verifying program tab inactive: {e}")
            return False

    def verify_add_new_program_button_visible(self):
        """Verify Add New Program button is visible in Program tab."""
        return self.is_element_visible(ProgramTypePageLocators.ADD_NEW_PROGRAM_BUTTON)

    def verify_add_new_patient_program_status_button_visible(self):
        """Verify Add New Patient Program Status button is visible in Status tab."""
        return self.is_element_visible(ProgramTypePageLocators.ADD_NEW_PATIENT_PROGRAM_STATUS_BUTTON)

    def get_program_table_headers(self):
        """Get program table headers."""
        try:
            headers = self.find_elements(ProgramTypePageLocators.PROGRAM_TABLE_HEADERS)
            return [header.text.strip() for header in headers]
        except Exception as e:
            printf(f"Error getting program table headers: {e}")
            return []

    def get_patient_program_status_table_headers(self):
        """Get patient program status table headers."""
        try:
            headers = self.find_elements(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_TABLE_HEADERS)
            return [header.text.strip() for header in headers]
        except Exception as e:
            printf(f"Error getting status table headers: {e}")
            return []

    def get_program_table_data(self):
        """Get all program table data."""
        try:
            rows = self.find_elements(ProgramTypePageLocators.PROGRAM_TABLE_ROWS)
            table_data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text.strip() for cell in cells]
                table_data.append(row_data)
            return table_data
        except Exception as e:
            printf(f"Error getting program table data: {e}")
            return []

    def get_patient_program_status_table_data(self):
        """Get all patient program status table data."""
        try:
            rows = self.find_elements(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_TABLE_ROWS)
            table_data = []
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                row_data = [cell.text.strip() for cell in cells]
                table_data.append(row_data)
            return table_data
        except Exception as e:
            printf(f"Error getting status table data: {e}")
            return []

    def search_programs(self, search_term):
        """Search programs by name."""
        try:
            self.clear_field(ProgramTypePageLocators.PROGRAM_SEARCH_INPUT)
            self.send_keys(ProgramTypePageLocators.PROGRAM_SEARCH_INPUT, search_term)
            self.click(ProgramTypePageLocators.PROGRAM_SEARCH_BUTTON)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Error searching programs: {e}")
            return False

    def search_patient_program_statuses(self, search_term):
        """Search patient program statuses by name."""
        try:
            self.clear_field(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_SEARCH_INPUT)
            self.send_keys(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_SEARCH_INPUT, search_term)
            # Search is automatic for status tab
            sleep(1)  # Allow time for search to apply
            return True
        except Exception as e:
            printf(f"Error searching statuses: {e}")
            return False

    def clear_program_search(self):
        """Clear program search."""
        try:
            self.click(ProgramTypePageLocators.PROGRAM_CLEAR_SEARCH_BUTTON)
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Error clearing program search: {e}")
            return False

    def select_programs_per_page(self, count):
        """Select number of programs per page."""
        try:
            self.select_by_visible_text(ProgramTypePageLocators.PROGRAM_ENTRIES_DROPDOWN, str(count))
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Error selecting programs per page: {e}")
            return False

    def select_statuses_per_page(self, count):
        """Select number of statuses per page."""
        try:
            self.select_by_visible_text(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_ENTRIES_DROPDOWN, str(count))
            self.wait_for_loader()
            return True
        except Exception as e:
            printf(f"Error selecting statuses per page: {e}")
            return False

    def verify_program_pagination_info(self, expected_count):
        """Verify programs pagination shows correct count."""
        try:
            pagination_text = self.get_text(ProgramTypePageLocators.PROGRAM_PAGINATION_INFO)
            return str(expected_count) in pagination_text
        except Exception as e:
            printf(f"Error verifying program pagination: {e}")
            return False

    def verify_status_pagination_info(self, expected_count):
        """Verify statuses pagination shows correct count."""
        try:
            pagination_text = self.get_text(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_PAGINATION_INFO)
            return str(expected_count) in pagination_text
        except Exception as e:
            printf(f"Error verifying status pagination: {e}")
            return False

    def click_program_action_button(self, program_name, action):
        """Click action button for specific program."""
        try:
            # Find the row containing the program name
            program_row = self.find_element(ProgramTypePageLocators.PROGRAM_ROW(program_name))

            if action.lower() == "edit":
                self.click(ProgramTypePageLocators.PROGRAM_EDIT_BUTTON)
            elif action.lower() == "view":
                self.click(ProgramTypePageLocators.PROGRAM_VIEW_BUTTON)
            elif action.lower() == "delete":
                self.click(ProgramTypePageLocators.PROGRAM_DELETE_BUTTON)
            else:
                printf(f"Unknown action: {action}")
                return False

            return True
        except Exception as e:
            printf(f"Error clicking program {action} button: {e}")
            return False

    def click_status_action_button(self, status_name, action):
        """Click action button for specific status."""
        try:
            # Find the row containing the status name
            status_row = self.find_element(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_ROW(status_name))

            if action.lower() == "edit":
                self.click(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_EDIT_BUTTON)
            elif action.lower() == "view":
                self.click(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_VIEW_BUTTON)
            elif action.lower() == "delete":
                self.click(ProgramTypePageLocators.PATIENT_PROGRAM_STATUS_DELETE_BUTTON)
            else:
                printf(f"Unknown action: {action}")
                return False

            return True
        except Exception as e:
            printf(f"Error clicking status {action} button: {e}")
            return False

    def verify_program_exists(self, program_name):
        """Verify if a program exists in the table."""
        try:
            program_rows = self.get_program_table_data()
            for row in program_rows:
                if program_name in row[0]:  # First column is program name
                    return True
            return False
        except Exception as e:
            printf(f"Error verifying program exists: {e}")
            return False

    def verify_patient_program_status_exists(self, status_name):
        """Verify if a patient program status exists in the table."""
        try:
            status_rows = self.get_patient_program_status_table_data()
            for row in status_rows:
                if status_name in row[0]:  # First column is status name
                    return True
            return False
        except Exception as e:
            printf(f"Error verifying status exists: {e}")
            return False
