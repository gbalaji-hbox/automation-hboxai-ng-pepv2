# --- File: features/commons/locators.py ---

from selenium.webdriver.common.by import By

"""
Central repository for all page object locators.
Locators are grouped by page or component using classes.
Access locators directly using ClassName.LOCATOR_NAME.
"""


class LoginPageLocators:
    """Locators for the login_page page elements."""
    EMAIL_INPUT = (By.XPATH, "//input[@id='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")
    # Avoid using class in XPath as it can be unstable
    ERROR_MESSAGE = (By.XPATH, "//div[normalize-space(text())='Email or password is incorrect']")
    PASSWORD_ERROR_MESSAGE = (By.XPATH, "//div[normalize-space(text())='Invalid password']")
    # More reliable locator without using class attribute
    HEADER_LOGO = (By.XPATH, "//img[@id='admin_header_logo']")
    SIGN_OUT_BUTTON = (By.XPATH, "//button[@id='sidebar_logout_btn']")
    LOG_OUT_CONFIRM_BUTTON = (By.XPATH, "//button[@id='logout_dialog_confirm_btn']")

class DashboardPageLocators:
    """Locators for the dashboard page elements."""
    HEADER_USER_MENU = (By.XPATH, "//button[@id='admin_header_user_menu_btn']")
    HAMBURGER_MENU = (By.XPATH, "//button[@id='admin_header_toggle_sidebar_btn']")
    HAMBURGER_MENU_ITEMS = (By.XPATH, "//nav[@id='admin_sidebar_nav']//a")
    HAMBURGER_MENU_OPTION = lambda option_text: (By.XPATH, f"//a/span[normalize-space(text())='{option_text}']")
    HEADER_LOGO = (By.XPATH, "//img[@id='admin_header_logo']")
    LOGOUT_BUTTON = (By.XPATH, "//button[@id='sidebar_logout_btn']")
    LOGOUT_DIALOG_CONFIRM_BUTTON = (By.XPATH, "//button[@id='logout_dialog_confirm_btn']")

class UsersPageLocators:
    """Locators for the users page elements."""
    USER_TABS = lambda tab_name: (By.XPATH, f"//button[@id='users_page_tab_{tab_name}']")
    SEARCH_TYPE_DROPDOWN = (By.XPATH, "(//button[@role='combobox'])[1]")
    SEARCH_TYPE_OPTION = lambda option_text: (By.XPATH, f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    SEARCH_INPUT = (By.XPATH, "//button[@role='combobox']/following-sibling::input[1]")
    SEARCH_DATEPICKER_INPUT = (By.XPATH, "//button[@role='combobox']/following-sibling::button[1]")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    USERS_TABLE = (By.XPATH, "//table[@id='table-admin-users']")
    USERS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-users']/tbody/tr")
    HISTORY_BUTTON = (By.XPATH, "//table[@id='table-admin-users']/tbody/tr/td[6]//button[contains(@id,'history')][1]")
    EDIT_BUTTON = (By.XPATH, "//table[@id='table-admin-users']/tbody/tr/td[6]//button[contains(@id,'edit')][1]")
    DELETE_BUTTON = (By.XPATH, "//table[@id='table-admin-users']/tbody/tr/td[6]//button[contains(@id,'delete')][1]")
    HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_DIALOG = (By.XPATH, "//p[normalize-space(text())='This action cannot be undone. This will permanently delete the user.']")
    DELETE_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")
    NEXT_PAGE_BUTTON = (By.XPATH, "//a[@aria-label='Go to next page']")
    PREVIOUS_PAGE_BUTTON = (By.XPATH, "//a[@aria-label='Go to next page']")
    SECOND_PAGE_BUTTON = (By.XPATH, "//a[text()='2']")