import time
import traceback
from datetime import datetime
from time import sleep
from urllib.parse import urlparse

from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchWindowException,
    StaleElementReferenceException,
    NoSuchElementException,
)
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from utils.logger import printf
from utils.utils import slugify


def find_element_in(parent: WebElement, locator: tuple):
    """Find an element inside a given parent element."""
    return parent.find_element(*locator)


# Map common human-friendly key names to selenium Keys
_KEY_NAME_MAP = {
    "NULL": Keys.NULL,
    "CANCEL": Keys.CANCEL,
    "HELP": Keys.HELP,
    "BACKSPACE": Keys.BACKSPACE,
    "TAB": Keys.TAB,
    "CLEAR": Keys.CLEAR,
    "RETURN": Keys.RETURN,
    "ENTER": Keys.ENTER,
    "SHIFT": Keys.SHIFT,
    "CONTROL": Keys.CONTROL,
    "CTRL": Keys.CONTROL,
    "ALT": Keys.ALT,
    "PAUSE": Keys.PAUSE,
    "ESCAPE": Keys.ESCAPE,
    "ESC": Keys.ESCAPE,
    "SPACE": Keys.SPACE,
    "PAGE_UP": Keys.PAGE_UP,
    "PAGE_DOWN": Keys.PAGE_DOWN,
    "END": Keys.END,
    "HOME": Keys.HOME,
    "ARROW_LEFT": Keys.ARROW_LEFT,
    "ARROW_UP": Keys.ARROW_UP,
    "ARROW_RIGHT": Keys.ARROW_RIGHT,
    "ARROW_DOWN": Keys.ARROW_DOWN,
    "LEFT": Keys.LEFT,
    "UP": Keys.UP,
    "RIGHT": Keys.RIGHT,
    "DOWN": Keys.DOWN,
    "INSERT": Keys.INSERT,
    "DELETE": Keys.DELETE,
    "SEMICOLON": Keys.SEMICOLON,
    "EQUALS": Keys.EQUALS,
    "NUMPAD0": Keys.NUMPAD0,
    "NUMPAD1": Keys.NUMPAD1,
    "NUMPAD2": Keys.NUMPAD2,
    "NUMPAD3": Keys.NUMPAD3,
    "NUMPAD4": Keys.NUMPAD4,
    "NUMPAD5": Keys.NUMPAD5,
    "NUMPAD6": Keys.NUMPAD6,
    "NUMPAD7": Keys.NUMPAD7,
    "NUMPAD8": Keys.NUMPAD8,
    "NUMPAD9": Keys.NUMPAD9,
    "MULTIPLY": Keys.MULTIPLY,
    "ADD": Keys.ADD,
    "SEPARATOR": Keys.SEPARATOR,
    "SUBTRACT": Keys.SUBTRACT,
    "DECIMAL": Keys.DECIMAL,
    "DIVIDE": Keys.DIVIDE,
    "F1": Keys.F1,
    "F2": Keys.F2,
    "F3": Keys.F3,
    "F4": Keys.F4,
    "F5": Keys.F5,
    "F6": Keys.F6,
    "F7": Keys.F7,
    "F8": Keys.F8,
    "F9": Keys.F9,
    "F10": Keys.F10,
    "F11": Keys.F11,
    "F12": Keys.F12,
    "META": Keys.META,
    "COMMAND": Keys.META,
}


class BasePage:
    # Loader locators
    LOADER_XPATH = (By.XPATH, "//div[@data-component-file='LoaderComponent.tsx' and @data-component-line='27']")
    VPE_LOADER_XPATH = (By.XPATH, "//p[contains(normalize-space(.), 'Loading patient')]")
    SPINNER_LOADER_XPATH = (By.XPATH, "//div[contains(@class, 'animate-spin')]")
    LUCID_LOADER_XPATH = (By.XPATH, "//svg[contains(@class,'lucide-loader-circle') and contains(@class,'animate-spin')]")
    
    # All loader locators
    ALL_LOADER_LOCATORS = [LOADER_XPATH, VPE_LOADER_XPATH, SPINNER_LOADER_XPATH]

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # -------------------- Core Retry Mechanism --------------------

    def wait_for_dom_stability(self, timeout=1):
        try:
            # prefer waiting for readyState = complete briefly
            WebDriverWait(self.driver, min(timeout, 3)).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except Exception as e:
            printf(f"[WARN] DOM did not stabilize in time: {e}")
        time.sleep(timeout)

    def _handle_stale_exception(self, attempt, max_attempts, locator, js_fallback):
        printf(f"StaleElementReferenceException on attempt {attempt + 1} for {locator}, retrying...")
        if attempt < max_attempts - 1:
            self.wait_for_dom_stability(timeout=2)
            return True
        if js_fallback and locator is not None:
            printf(f"Final attempt: using JS fallback for {locator}")
            return self.js_click(locator)
        return None

    def _handle_click_intercepted_exception(self, attempt, max_attempts, locator, js_fallback):
        printf(f"ElementClickInterceptedException on attempt {attempt + 1} for {locator}")
        if js_fallback and locator is not None:
            printf(f"Using JavaScript click as fallback for {locator}")
            return self.js_click(locator)
        if attempt < max_attempts - 1:
            self.wait_for_dom_stability(timeout=1)
            return True
        return None

    def _handle_timeout_exception(self, attempt, locator, te, suppress_timeout):
        msg = f"TimeoutException waiting for {locator} on attempt {attempt + 1}: {te}"
        printf(msg)
        if suppress_timeout:
            return False
        return None

    def _handle_generic_exception(self, attempt, max_attempts, locator, e):
        printf(f"Exception on attempt {attempt + 1} for {locator}: {e}")
        traceback.print_exc()
        if attempt < max_attempts - 1:
            self.wait_for_dom_stability(timeout=1)
            return True
        return None

    def _handle_exception(self, e, attempt, max_attempts, locator, js_fallback, suppress_timeout):
        if isinstance(e, StaleElementReferenceException):
            ret = self._handle_stale_exception(attempt, max_attempts, locator, js_fallback)
        elif isinstance(e, ElementClickInterceptedException):
            ret = self._handle_click_intercepted_exception(attempt, max_attempts, locator, js_fallback)
        elif isinstance(e, TimeoutException):
            ret = self._handle_timeout_exception(attempt, locator, e, suppress_timeout)
            return 'return', ret
        else:
            ret = self._handle_generic_exception(attempt, max_attempts, locator, e)
        if ret:
            return 'continue', None
        else:
            return 'return', ret

    def _retry_action(self, action, locator=None, js_fallback=False, max_attempts=3, wait_condition=None,
                      suppress_timeout=False):
        for attempt in range(max_attempts):
            try:
                if wait_condition and locator:
                    # wait_condition is an expected_condition factory (like ec.element_to_be_clickable)
                    self.wait.until(wait_condition(locator))
                # call action. If action expects locator, pass it; else call with no args.
                result = action(locator) if locator is not None else action()
                return result
            except Exception as e:
                action_type, value = self._handle_exception(e, attempt, max_attempts, locator, js_fallback,
                                                            suppress_timeout)
                if action_type == 'continue':
                    continue
                elif action_type == 'return':
                    return value
        # if loop completes, return False for suppressed flows
        return False

    # -------------------- Basic Find/Click/Type with Retry --------------------

    def find_element(self, locator, retry=False):
        """Return WebElement or raise TimeoutException if not found (same as original)."""
        if retry:
            return self._retry_action(
                action=lambda loc: self.wait.until(ec.presence_of_element_located(loc)),
                locator=locator,
                wait_condition=ec.presence_of_element_located,
                suppress_timeout=False,
            )
        else:
            return self.wait.until(ec.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Return list of WebElements or raise TimeoutException if not found."""
        return self._retry_action(
            action=lambda loc: self.wait.until(ec.presence_of_all_elements_located(loc)),
            locator=locator,
            wait_condition=ec.presence_of_all_elements_located,
            suppress_timeout=False,
        )

    def click(self, locator):
        """Click an element with stale element handling and JS fallback if needed."""
        return self._retry_action(
            action=lambda loc: self.find_element(loc).click(),
            locator=locator,
            js_fallback=True,
            wait_condition=ec.element_to_be_clickable,
            suppress_timeout=True
        )

    def js_click(self, locator, timeout=10):
        """
        Click an element using JavaScript. Useful when regular click is intercepted or fails.
        Keeps original behaviour: returns False on timeout, raises other exceptions.
        """
        printf(f"Attempting JavaScript click on: {locator}")
        try:
            element = self.find_element(locator)  # will raise TimeoutException if not found
            self.driver.execute_script("arguments[0].click();", element)
            printf(f"Successfully clicked element via JS: {locator}")
            return True
        except TimeoutException:
            printf(f"Timeout: Element not found for JS click within {timeout} seconds: {locator}")
            return False
        except Exception as e:
            printf(f"Error with JS click on element {locator}: {e}")
            raise

    def send_keys(self, locator, text, use_js=False):
        """Send keys to an input; uses retry mechanism and preserves optional JS approach."""
        return self._retry_action(
            action=lambda loc: self._send_keys_internal(loc, text, use_js),
            locator=locator,
            wait_condition=ec.element_to_be_clickable,
            suppress_timeout=False,
        )

    def _send_keys_internal(self, locator, text, use_js):
        ele = self.find_element(locator)
        if use_js:
            # Use JavaScript to set value and dispatch input event
            self.driver.execute_script(
                "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                ele,
                text,
            )
        else:
            ele.clear()
            ele.send_keys(text)
        return True

    def clear_field(self, locator):
        """Clear the text content of an input field"""
        return self._retry_action(
            action=lambda loc: self.find_element(loc).clear(),
            locator=locator,
            wait_condition=ec.presence_of_element_located,
            suppress_timeout=False,
        )

    def file_upload_input(self, locator, file_path):
        """Upload a file by sending the file path to an <input type='file'> element."""
        return self._retry_action(
            action=lambda loc: self.find_element(loc).send_keys(file_path),
            locator=locator,
            wait_condition=ec.presence_of_element_located,
            suppress_timeout=False,
        )

    def _flatten_keys(self, keys):
        if len(keys) == 1 and isinstance(keys[0], (list, tuple)):
            return tuple(keys[0])
        return keys

    def _resolve_element(self, loc):
        if isinstance(loc, tuple):
            return self.find_element(loc)
        elif isinstance(loc, WebElement):
            return loc
        elif loc is None:
            return self.driver.switch_to.active_element
        else:
            raise TypeError("locator must be a locator tuple, WebElement, or None")

    def _convert_keys(self, keys):
        converted = []
        for k in keys:
            if isinstance(k, str):
                if len(k) == 1:
                    converted.append(k)
                else:
                    mapped = _KEY_NAME_MAP.get(k.upper())
                    if mapped:
                        converted.append(mapped)
                    else:
                        converted.append(k)
            else:
                converted.append(k)
        return converted

    def send_key_down(self, locator=None, *keys):
        """
        Send keyboard keys to an element or active element.

        Args:
            locator: locator tuple (By, value), WebElement, or None (sends to active element)
            *keys: one or more keys/strings. Acceptable forms:
                   - selenium Keys constants (use page.Keys.ENTER to avoid importing Keys elsewhere)
                   - single-character strings ('a', '1', etc.)
                   - named strings 'ENTER', 'CTRL', 'ESC' (mapped automatically)
                   - lists/tuples of the above (you can pass a single list)
        Examples:
            page.send_key_down(locator, page.Keys.ENTER)
            page.send_key_down(locator, 'a')
            page.send_key_down(locator, page.Keys.CONTROL, 'a')
            page.send_key_down(None, 'ESCAPE')  # sends to active element
        """
        keys = self._flatten_keys(keys)

        def _action(loc):
            element = self._resolve_element(loc)
            converted = self._convert_keys(keys)
            try:
                element.send_keys(*converted)
                return True
            except Exception as e:
                printf(f"Error sending keys {keys} to {locator}: {e}")
                raise

        # only wait for presence if locator is a locator tuple
        wait_cond = ec.presence_of_element_located if isinstance(locator, tuple) else None

        return self._retry_action(action=_action, locator=locator, wait_condition=wait_cond, suppress_timeout=False)

    def get_text(self, locator):
        """Get text from element with retry."""
        return self._retry_action(
            action=lambda loc: self.find_element(loc).text,
            locator=locator,
            wait_condition=ec.presence_of_element_located,
            suppress_timeout=False,
        )

    def get_attribute(self, locator_or_element, attribute_name):
        """Get attribute from either a locator tuple or a WebElement."""
        if isinstance(locator_or_element, tuple):
            # will raise TimeoutException if not found
            element = self.find_element(locator_or_element)
        elif isinstance(locator_or_element, WebElement):
            element = locator_or_element
        else:
            raise TypeError("Expected a locator tuple or WebElement")
        return element.get_attribute(attribute_name)

    # -------------------- URL / Title Checks --------------------

    def check_url_contains(self, text, partial=True):
        """Check whether URL contains a slugified last segment or full match."""
        printf(f"Checking if URL contains '{text}' (partial={partial})")
        sleep(1)
        if partial:
            slug_text = slugify(text)

            def last_segment_matches(driver):
                try:
                    current_url = driver.current_url
                    path = urlparse(current_url).path.rstrip("/")
                    last_segment = path.split("/")[-1]
                    return last_segment == slug_text
                except Exception as e:
                    printf(f"Error checking URL segment match: {e}")
                    return False

            return self.wait.until(last_segment_matches)
        else:
            return self.wait.until(ec.url_contains(text.lower()))

    def check_url_match(self, text):
        current_url = self.driver.current_url
        if text != current_url:
            f"Expected URL '{text}', but got '{current_url}'"
        return text == current_url

    def check_title_contains(self, text):
        self.wait.until(ec.title_contains(text))
        current_title = self.driver.title
        return text in current_title, f"Expected URL '{text}', but got '{current_title}'"

    # -------------------- Hover / Iframe / Scrolling --------------------

    def hover_over_element(self, element_or_locator):
        """Hover over an element or WebElement; works with either input type."""

        def _action(loc):
            if isinstance(loc, tuple):
                ele = self.find_element(loc)
            elif isinstance(loc, WebElement):
                ele = loc
            else:
                raise TypeError("Expected a locator tuple or WebElement")
            self.wait.until(ec.visibility_of(ele))
            ActionChains(self.driver).move_to_element(ele).perform()
            return True

        # if the input is a WebElement, pass it directly as locator param
        if isinstance(element_or_locator, WebElement):
            return self._retry_action(action=lambda _: _action(element_or_locator), locator=None, wait_condition=None)
        else:
            return self._retry_action(action=_action, locator=element_or_locator,
                                      wait_condition=ec.visibility_of_element_located)

    def switch_to_iframe(self, locator):
        """Switch to iframe by locator (waits for frame availability)."""
        # Use ec.frame_to_be_available_and_switch_to_it if desired; but keep original style
        return self._retry_action(
            action=lambda loc: self.driver.switch_to.frame(self.find_element(loc)),
            locator=locator,
            wait_condition=ec.frame_to_be_available_and_switch_to_it,
            suppress_timeout=False,
        )

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def scroll_to_visible_element(self, locator):
        """Scroll element into view (returns True on success)."""
        return self._retry_action(
            action=lambda loc: self.driver.execute_script("arguments[0].scrollIntoView(true);", self.find_element(loc)),
            locator=locator,
            wait_condition=ec.presence_of_element_located,
            suppress_timeout=False,
        )

    # -------------------- Date / Alert / Element Checks --------------------

    def select_date(self, locator, date_str):
        # e.g., date_str = "2025-04-06" or "06/04/2025" depending on format
        date_input = self.find_element(locator)
        date_input.clear()
        date_input.send_keys(date_str)
        return True

    def accept_alert(self):
        self.wait.until(ec.alert_is_present())
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        self.wait.until(ec.alert_is_present())
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        self.wait.until(ec.alert_is_present())
        return self.driver.switch_to.alert.text

    def is_element_visible(self, locator, timeout=15):
        original_wait = self.driver.timeouts.implicit_wait
        try:
            self.driver.implicitly_wait(0)
            WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
            return False
        finally:
            self.driver.implicitly_wait(original_wait)

    def is_element_present(self, locator):
        """Returns True if element exists and is displayed, else False."""
        try:
            ele: WebElement = self.find_element(locator)
            return ele.is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def is_clickable(self, locator, timeout=15):
        original_wait = self.driver.timeouts.implicit_wait
        try:
            self.driver.implicitly_wait(0)
            WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False
        finally:
            self.driver.implicitly_wait(original_wait)

    # -------------------- Tab / Window Handling --------------------

    def check_url_changes(self, old_url, timeout=15):
        WebDriverWait(self.driver, timeout).until(ec.url_changes(old_url))

    def _resolve_tab_index(self, tab_index, num_tabs):
        if isinstance(tab_index, int):
            if 0 <= tab_index < num_tabs:
                return tab_index
            elif tab_index == -1:
                return num_tabs - 1
            else:
                raise IndexError(
                    f"Invalid tab index '{tab_index}'. "
                    f"Index must be 0-{num_tabs - 1} or -1. Currently {num_tabs} tab(s) open."
                )
        elif isinstance(tab_index, str):
            if tab_index == "-1":
                return num_tabs - 1
            else:
                try:
                    index_val = int(tab_index)
                    if 0 <= index_val < num_tabs:
                        return index_val
                    else:
                        raise IndexError(
                            f"Tab index '{tab_index}' out of bounds. "
                            f"Index must be 0-{num_tabs - 1} or -1. Currently {num_tabs} tab(s) open."
                        )
                except ValueError:
                    raise ValueError(
                        f"Invalid tab identifier '{tab_index}'. "
                        "Must be an integer, '-1', or a string representation."
                    )
        else:
            raise TypeError(
                f"Invalid tab_index type: {type(tab_index).__name__}. Expected int or str."
            )

    def switch_to_tab(self, tab_index):
        """Switches WebDriver focus to a tab by index or identifier."""
        handles = self.driver.window_handles
        num_tabs = len(handles)

        if num_tabs == 0:
            raise RuntimeError("Cannot switch tabs: No browser tabs are currently open.")

        resolved_target_index = self._resolve_tab_index(tab_index, num_tabs)

        # resolved_target_index is guaranteed to be valid at this point.
        try:
            self.driver.switch_to.window(handles[resolved_target_index])
            printf(f"Successfully switched to tab at index {resolved_target_index}.")
        except NoSuchWindowException as e:
            # Catch if tab becomes unavailable during switch.
            raise NoSuchWindowException(
                f"Failed to switch to tab {resolved_target_index}. Window handle missing: {e}"
            )

    def wait_for_any_element_visible(self, locators, timeout=10):
        """
        Waits for any of the elements specified by the locators to be visible.

        Args:
            locators (list): A list of locator tuples (By.ID, "locator_value").
            timeout (int): The maximum time to wait in seconds.
        """
        for locator in locators:
            try:
                WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))
                return True
            except TimeoutException:
                continue
        raise TimeoutException(
            f"Timed out after {timeout} seconds waiting for any of the elements {locators} to be visible."
        )

    def wait_for_new_tab(self, expected_tab_count: int):
        try:
            self.wait.until(ec.number_of_windows_to_be(expected_tab_count))
        except Exception as e:
            raise TimeoutError(f"Timeout waiting for {expected_tab_count} tabs to open. Error: {e}")

    # -------------------- Select Helpers --------------------

    def select_by_visible_text(self, locator, text):
        """Standard <select> dropdown."""

        def action(loc):
            ele = WebDriverWait(self.driver, 10).until(ec.element_to_be_clickable(loc))
            select = Select(ele)
            current = select.first_selected_option.text.strip()
            if current != text:
                select.select_by_visible_text(text)
                printf(f"✅ Selected '{text}' in dropdown.")
            else:
                printf(f"ℹ️ Dropdown already has '{text}' selected. Skipping.")
            return True

        return self._retry_action(
            action=action,
            locator=locator,
            wait_condition=ec.element_to_be_clickable,
            suppress_timeout=False,
        )

    def select_by_value(self, locator, value):
        """Select by value for standard select elements."""
        return self._retry_action(
            action=lambda loc: Select(self.find_element(loc)).select_by_value(value),
            locator=locator,
            wait_condition=ec.presence_of_element_located,
            suppress_timeout=False,
        )

    def select_by_value_and_update_ui(self, locator, value):
        select_elem = self.find_element(locator)
        Select(select_elem).select_by_value(value)

        # Trigger the change event so React/Redux updates the UI
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", select_elem)

    def select_by_index(self, locator, index):
        """Select by index for standard select elements."""
        return self._retry_action(
            action=lambda loc: Select(self.find_element(loc)).select_by_index(index),
            locator=locator,
            wait_condition=ec.presence_of_element_located,
            suppress_timeout=False,
        )

    # -------------------- Navigation Helpers --------------------

    def refresh_page(self):
        self.driver.refresh()
        sleep(1)  # Small delay to ensure page is fully refreshed

    def navigate_to(self, url):
        """
        Navigate to a specific URL.
        """
        self.driver.get(url)
        self.wait_for_dom_stability()

    def navigate_back(self):
        self.driver.back()
        sleep(1)  # Small delay to ensure navigation completes

    def navigate_forward(self):
        self.driver.forward()
        sleep(1)  # Small delay to ensure navigation completes

    def hard_refresh_with_cache_clear(self):
        # Execute JavaScript to clear cache and perform a hard refresh
        try:
            self.driver.execute_script("location.reload(true);")
        except Exception as e:
            printf(f"Error performing hard refresh via JS: {e}")
            # fallback refresh
            self.driver.refresh()
        sleep(2)  # Longer delay to ensure cache is cleared and page is fully reloaded

    def clear_browser_cache(self):
        # Execute JavaScript to clear localStorage and sessionStorage
        try:
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")
        except Exception as e:
            printf(f"Error clearing storage: {e}")
        # Clear cookies
        try:
            self.driver.delete_all_cookies()
        except Exception as e:
            printf(f"Error deleting cookies: {e}")
        sleep(1)

    # -------------------- Table / Spinner / Wait Helpers --------------------

    def get_number_of_table_rows(self, data_locator):
        """Get number of valid table rows, filtering out headers and invalid rows"""
        try:
            all_rows = self.find_elements(data_locator)
            return len(all_rows)
        except Exception as e:
            printf(f"Error filtering table rows: {e}, returning raw count")
            try:
                return len(self.find_elements(data_locator))
            except Exception as e:
                printf(f"Error getting table rows: {e}")
                return 0

    def extract_table_data(self, table_locator: tuple, first_row_only: bool = False):
        """
        Extract data from an HTML table as a list of dictionaries (header -> cell value).

        Args:
            table_locator (tuple): Locator for the <table> element (By, "value")
            first_row_only (bool): If True, return only the first row as a dict

        Returns:
            list[dict] or dict: List of rows as dicts, or single dict if first_row_only=True
        """

        # Get table element
        table: WebElement = self.find_element(table_locator)

        # Extract headers dynamically
        header_row: WebElement = table.find_element(By.XPATH, ".//thead/tr")
        headers = [th.text.strip() for th in header_row.find_elements(By.TAG_NAME, "th") if th.text.strip()]

        # Extract all body rows
        body_rows = table.find_elements(By.XPATH, ".//tbody/tr")
        all_data = []

        for row in body_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            cell_texts = [c.text.strip() for c in cells]
            row_dict = dict(zip(headers, cell_texts))
            all_data.append(row_dict)

            if first_row_only:
                return row_dict  # Return immediately for first row

        return all_data

    def wait_for_loader(self, timeout=15, strict=True, loader_locators=None):
        if loader_locators is None:
            loader_locators = self.ALL_LOADER_LOCATORS
        elif not isinstance(loader_locators, list):
            loader_locators = [loader_locators]
        
        original_wait = self.driver.timeouts.implicit_wait
        self.driver.implicitly_wait(0)
        printf(f"⏳ Waiting for loaders to disappear (timeout={timeout}, strict={strict})...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            any_loader_visible = False
            for locator in loader_locators:
                try:
                    loader: WebElement = self.driver.find_element(*locator)
                    if loader.is_displayed():
                        any_loader_visible = True
                        break
                except (NoSuchElementException, StaleElementReferenceException):
                    continue
            
            if not any_loader_visible:
                # All loaders gone or not visible
                self.driver.implicitly_wait(original_wait)
                elapsed = time.time() - start_time
                printf(f"✅ All loaders disappeared after {elapsed:.2f}s")
                return True
            
            time.sleep(0.2)

        # Timeout
        elapsed = time.time() - start_time
        msg = f"❌ Some loaders still visible after {elapsed:.2f}s"
        if strict:
            raise TimeoutException(msg)
        else:
            self.driver.implicitly_wait(original_wait)
            printf(msg)
            return False

    def select_calender_date(self, date_str: str):
        """
        Select a date in the calendar popup.
        Assumes the calendar is already open.
        date_str format: dd/mm/yyyy or dd-mm-yyyy
        """
        # Try multiple date formats dynamically
        date_formats = [
        "%m-%d-%y",  # 03-04-54
        "%m-%d-%Y",  # 03-04-1954
        "%d-%m-%Y",  # 04-03-1954
        "%Y-%m-%d",  # 1954-03-04
        "%d/%m/%Y",  # 04/03/1954
        "%Y/%m/%d",  # 1954/03/04
        "%m/%d/%Y",  # 03/04/1954 (US style)
        ]
        date = None
        for fmt in date_formats:
            try:
                date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        if date is None:
            raise ValueError(f"time data '{date_str}' does not match any expected format {date_formats}")
        day = date.day
        month = date.month
        year = date.year

        # Get current displayed month
        month_text_locator = (By.XPATH, "//div[@aria-live='polite' and @role='presentation']")
        current_month_element = self.driver.find_element(*month_text_locator)
        current_month_text = current_month_element.text  # e.g. "January 2026"
        current_date = datetime.strptime(current_month_text, "%B %Y")
        current_month = current_date.month
        current_year = current_date.year

        # Calculate months to navigate
        months_diff = (year - current_year) * 12 + (month - current_month)

        if months_diff > 0:
            for _ in range(months_diff):
                next_button = self.driver.find_element(By.XPATH, "//button[@name='next-month']")
                next_button.click()
                time.sleep(0.2)  # Wait for calendar update
        elif months_diff < 0:
            for _ in range(-months_diff):
                prev_button = self.driver.find_element(By.XPATH, "//button[@name='previous-month']")
                prev_button.click()
                time.sleep(0.2)

        # Click the day button (ensure it's not a day from previous/next month)
        day_button = self.driver.find_element(By.XPATH, f"//button[@name='day' and not(contains(@class, 'day-outside')) and text()='{day}']")
        day_button.click()

    # -------------------- Misc / State Checks --------------------

    def wait_for_dom_stability_full(self, timeout=10):
        """
        Wait until document.readyState is complete and no DOM mutation is ongoing.
        For React apps, this typically waits until all rendering is done.
        Kept old name (wait_for_dom_stability) exists below for backward compatibility.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Optional: ensure React rendering has flushed
            time.sleep(0.3)  # brief pause after readyState
            return True
        except Exception as e:
            printf(f"[WARN] DOM did not stabilize in time: {e}")
            return False

    def is_element_enabled(self, locator):
        try:
            element: WebElement = self.find_element(locator, retry=True)
            class_attr = element.get_attribute("class") or ""
            return "disabled" not in class_attr.lower()
        except Exception as e:
            printf(f"Error checking element state: {e}")
            return False

    def react_clear(self, locator):
        """Clears a React-controlled input reliably."""
        element = self._resolve_element(locator)
        self.driver.execute_script("""
            arguments[0].value = '';
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, element)
        return element

    def custom_select_by_locator(self, base_locator, option_locator):
        """Custom dropdown selection for non-standard select elements."""
        dropdown = self.find_element(base_locator)
        dropdown.click()
        time.sleep(0.5)  # wait for options to render
        option = self.find_element(option_locator)
        option.click()
        return True
