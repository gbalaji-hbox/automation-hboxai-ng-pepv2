from selenium.common import NoSuchElementException

from features.commons.locators import ProgramPageLocators
from features.pages.base_page import BasePage
from utils.logger import printf


class ProgramPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_tab(self, tab_name):
        """Navigate to the specified tab in the Program Type page."""
        if tab_name == 'Program':
            locator = ProgramPageLocators.PROGRAM_TAB
        else:
            locator = ProgramPageLocators.PATIENT_PROGRAM_STATUS_TAB

        try:
            if self.is_element_visible(ProgramPageLocators.CLEAR_SEARCH_BUTTON, timeout=2):
                self.click(ProgramPageLocators.CLEAR_SEARCH_BUTTON)
                self.wait_for_dom_stability_full()

            tab_ele = self.find_element(locator)
            if self.get_attribute(tab_ele, "aria-selected") == "true":
                printf(f"Tab '{tab_name}' is already selected.")
                return
            tab_ele.click()
            self.wait_for_loader()
        except NoSuchElementException:
            printf(f"Tab with name '{tab_name}' not found on Users Page.")
            raise