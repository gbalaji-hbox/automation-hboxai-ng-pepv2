import traceback
from time import sleep
from urllib.parse import urlparse

from selenium.webdriver.common.by import By

from features.commons.locators import DashboardPageLocators
from features.pages.base_page import BasePage
from utils.logger import printf


class DashboardPage(BasePage):
    """Page object for the dashboard page."""

    def __init__(self, driver):
        super().__init__(driver)

    def is_logged_in(self):
        """Check if the user is logged in by verifying the presence of the welcome message."""
        try:
            return self.is_element_visible(DashboardPageLocators.HEADER_USER_MENU, timeout=10)
        except Exception as e:
            printf(f"Error checking login status: {e}")
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
            printf(f"Error clicking dynamic menu option '{option_name}': {e}")
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

    def get_all_available_menu_options(self):
        """
        Dynamically extract all menu options available in current session.
        Uses utility functions to get real-time menu structure.

        Returns:
            list: List of menu option details with 'text', 'url', 'is_action' keys
        """
        try:
            printf("Extracting all available hamburger menu options...")

            # Wait for DOM to settle first
            self.wait_for_dom_stability()

            # Check if menu items locator finds elements
            try:
                menu_elements = self.find_elements(DashboardPageLocators.HAMBURGER_MENU_ITEMS)
                printf(f"Found {len(menu_elements)} menu item elements")
                if len(menu_elements) == 0:
                    printf("No menu item elements found with locator:", DashboardPageLocators.HAMBURGER_MENU_ITEMS[1])
                    return []
            except Exception as elem_e:
                printf(f"Error finding menu elements: {elem_e}")
                return []

            menu_options = self.get_hamburger_menu_options(DashboardPageLocators.HAMBURGER_MENU_ITEMS)

            if menu_options:
                printf(f"Found {len(menu_options)} menu options")
                for option in menu_options:
                    action_type = "Action" if option.get('is_action') else "Navigation"
                    printf(f"  - {option['text']} ({action_type})")
                return menu_options
            else:
                printf("No menu options found")
                return []

        except Exception as e:
            printf(f"Error extracting menu options: {e}")

            traceback.print_exc()
            return []

    def get_hamburger_menu_options(self, menu_items_locator):
        """
        Extract all available menu options dynamically from hamburger menu for dynamic testing.

        Args:
            menu_items_locator: Locator for menu items (e.g., HAMBURGER_MENU_ITEMS)

        Returns:
            list: List of menu option details with keys 'text', 'url', 'is_action' or None if extraction fails
        """
        try:
            print(f"🔍 Searching for menu items with locator: {menu_items_locator[1]}")

            # Brief wait for menu items to be visible
            sleep(1)

            # Get all menu item elements
            menu_items = self.find_elements(menu_items_locator)
            printf(f"Found {len(menu_items)} raw menu item elements")

            if not menu_items:
                printf("❌ No menu items found in the hamburger menu")
                return None

            menu_options = []

            for i, item in enumerate(menu_items):
                try:
                    printf(f"Parsing menu item {i + 1}/{len(menu_items)}...")
                    # Parse each menu item to extract details
                    menu_data = self._parse_menu_item_data(item)
                    if menu_data:
                        menu_options.append(menu_data)
                        printf(f"  ✅ Parsed: {menu_data['text']}")
                    else:
                        printf(f"  ❌ Failed to parse menu item {i + 1}")
                except Exception as e:
                    printf(f"  ❌ Error parsing menu item {i + 1}: {e}")
                    continue

            if menu_options:
                printf(f"✅ Extracted {len(menu_options)} menu options: {[opt['text'] for opt in menu_options]}")
                return menu_options
            else:
                printf("❌ Could not parse any menu options")
                return None

        except Exception as e:
            printf(f"Error extracting hamburger menu options: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _parse_menu_item_data(self, menu_item):
        """Extract text and href metadata from a single hamburger menu item."""
        try:
            text_el = menu_item.find_element(By.XPATH, ".//span[normalize-space()]")
            text_value = text_el.text.strip()
        except Exception as e:
            printf(f"Error extracting text from menu item: {e}")
            text_value = (menu_item.text or "").strip()

        if not text_value:
            return None

        href_value = (menu_item.get_attribute("href") or "").strip()
        is_action = not href_value or href_value.lower().startswith("javascript:")

        return {
            "text": text_value,
            "url": href_value,
            "is_action": is_action,
        }

    # -------------------- Navigation helpers for menu verification --------------------

    def choose_return_option(self, menu_options):
        """Pick a sensible menu item to navigate back to after visiting others."""
        if not menu_options:
            return None
        texts = [opt.get("text", "") for opt in menu_options]
        return texts[0]

    def verify_all_menu_navigation_with_titles(self, menu_options, return_option=None):
        """Visit each menu option, record navigation success, and capture browser titles."""
        results = {}
        for opt in menu_options:
            text = opt.get("text")
            href = opt.get("url")
            if not text:
                continue

            # Skip non-navigational actions
            if opt.get("is_action"):
                results[text] = {"status": "skipped", "reason": "action"}
                continue

            try:
                # Click the menu item by text using existing dynamic locator
                self.click_dynamic_hamburger_menu_option(text)
                self.wait_for_dom_stability(timeout=2)

                # Basic URL check: last path segment matches slugified text or href path if provided
                current_url = self.driver.current_url
                if href:
                    expected_path = urlparse(href).path.rstrip("/")
                    current_path = urlparse(current_url).path.rstrip("/")
                    url_passed = current_path == expected_path or current_path.endswith(expected_path.split("/")[-1])
                else:
                    url_passed = text.lower() in current_url.lower()

                # Get expected title based on menu text
                expected_title = self._get_expected_title_for_menu_option(text)
                actual_title = self.driver.title

                title_passed = actual_title == expected_title

                results[text] = {
                    "status": "passed" if (url_passed and title_passed) else "failed",
                    "current_url": current_url,
                    "expected_url": href or text,
                    "actual_title": actual_title,
                    "expected_title": expected_title,
                    "url_passed": url_passed,
                    "title_passed": title_passed,
                }
            except Exception as e:
                results[text] = {"status": "failed", "error": str(e)}

            # Navigate back to a known page to keep state clean
            if return_option and return_option != text:
                try:
                    self.click_dynamic_hamburger_menu_option(return_option)
                    self.wait_for_dom_stability(timeout=1)
                except Exception as e:
                    printf(f"Error visiting menu options: {e}")
                    pass

        return results

    def assert_navigation_results(self, navigation_results):
        """Assert all non-skipped navigation attempts passed."""
        failed = [name for name, res in navigation_results.items() if res.get("status") == "failed"]
        if failed:
            printf("Navigation assertion failed. Detailed failure reasons:")
            for name in failed:
                res = navigation_results[name]
                printf(f"  - {name}:")
                if "error" in res:
                    printf(f"    Error: {res['error']}")
                if "current_url" in res and "expected_url" in res:
                    printf(f"    URL - Expected: {res['expected_url']}, Actual: {res['current_url']}")
                if "actual_title" in res and "expected_title" in res:
                    printf(f"    Title - Expected: '{res['expected_title']}', Actual: '{res['actual_title']}'")
                if "url_passed" in res and "title_passed" in res:
                    printf(f"    URL passed: {res['url_passed']}, Title passed: {res['title_passed']}")
            raise AssertionError(f"Navigation failed for menu options: {', '.join(failed)}")

    def assert_links_functional(self, navigation_results):
        """Validate that all navigable links responded with a passed status."""
        passed = [name for name, res in navigation_results.items() if res.get("status") == "passed"]
        testable = [name for name, res in navigation_results.items() if res.get("status") in ["passed", "failed"]]
        if len(passed) != len(testable):
            raise AssertionError("Some menu links are not functional")
        printf(f"All {len(passed)} menu option links are functional and accessible")

    def click_logout_option(self):
        """Click on the 'Logout' option in the hamburger menu."""
        try:
            self.click(DashboardPageLocators.LOGOUT_BUTTON)
            sleep(1)
            self.is_element_visible(DashboardPageLocators.LOGOUT_DIALOG_CONFIRM_BUTTON, timeout=5)
            self.click(DashboardPageLocators.LOGOUT_DIALOG_CONFIRM_BUTTON)
            return True
        except Exception as e:
            printf(f"Error clicking logout option: {e}")
            return False

    def _get_expected_title_for_menu_option(self, menu_text):
        """Get the expected browser title for a menu option."""
        title_map = {
            "Dashboard": "Dashboard | Admin",
            "Users": "Users & User Groups | Admin",
            "Program Type": "Program Type | Admin",
            "Patient Groups": "Patient Groups | Admin",
            "Workflow": "Workflow & Tasks | Admin",
            "Activities": "Activities | Admin",
            "Facility Availability": "Facility Availability | Admin",
            "Scheduled Appointments": "Scheduled Appointments | Admin",
            "SMS": "SMS | Admin",
            "Call History": "Call History | Admin",
            "Patients": "Patients | Admin",
            "Add Patient": "Add Patient | Admin",
        }
        return title_map.get(menu_text, f"{menu_text} | Admin")

    def assert_browser_titles_correct(self, navigation_results):
        """Assert that all menu options have correct browser titles."""
        title_failures = []
        for name, res in navigation_results.items():
            if res.get("status") == "skipped":
                continue
            if not res.get("title_passed", False):
                expected = res.get("expected_title", "Unknown")
                actual = res.get("actual_title", "Unknown")
                title_failures.append(f"{name} (expected: '{expected}', actual: '{actual}')")

        if title_failures:
            raise AssertionError(f"Browser title verification failed for: {', '.join(title_failures)}")

        printf(f"All {len([r for r in navigation_results.values() if r.get('status') != 'skipped'])} menu options have correct browser titles")

    def verify_browser_tab_contains(self, expected_text):
        """Verify that the browser tab title contains the expected text."""
        try:
            actual_title = self.driver.title
            printf(f"Browser tab title: '{actual_title}'")
            return expected_text in actual_title
        except Exception as e:
            printf(f"Error checking browser tab title: {e}")
            return False
