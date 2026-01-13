from features.commons.locators import DashboardPageLocators
from features.pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page object for the dashboard page."""

    def __init__(self, driver):
        super().__init__(driver)

    def is_logged_in(self):
        """Check if the user is logged in by verifying the presence of the welcome message."""
        try:
            return self.is_element_visible(DashboardPageLocators.HEADER_USER_MENU, timeout=10)
        except Exception as e:
            print(f"Error checking login status: {e}")
            return False

    def navigate_to_dashboard(self, page_name="dashboard"):
        """Navigate to the main dashboard page."""
        self.click_dynamic_hamburger_menu_option(page_name)

    def click_dynamic_hamburger_menu_option(self, option_name):
        """Click on a dynamic option in the hamburger menu."""
        try:
            dynamic_locator = DashboardPageLocators.HAMBURGER_MENU_OPTION(option_text=option_name)
            self.is_element_visible(dynamic_locator, timeout=2)
            return self.click(dynamic_locator)
        except Exception as e:
            print(f"Error clicking dynamic menu option '{option_name}': {e}")
            return False

    def verify_dashboard_header(self):
        """Verify the presence of the dashboard header."""
        return self.is_element_visible(DashboardPageLocators.HEADER_LOGO, timeout=10)

    def verify_hamburger_menu(self):
        """Verify the presence of the hamburger menu."""
        return self.is_element_visible(DashboardPageLocators.HAMBURGER_MENU, timeout=10)

    def verify_user_profile_section(self):
        """Verify the presence of the user profile section."""
        return self.is_element_visible(DashboardPageLocators.HEADER_USER_MENU, timeout=10)