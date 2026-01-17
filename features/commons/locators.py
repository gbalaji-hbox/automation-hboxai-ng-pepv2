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
    USER_TAB = (By.XPATH, "//button[@id='users_page_tab_user']")
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

class UserGroupPageLocators:
    """Locators for the user groups page elements."""
    USER_GROUP_TAB = (By.XPATH, "//button[@id='users_page_tab_user_group']")
    SEARCH_TYPE_DROPDOWN = (By.XPATH, "(//button[@role='combobox'])[1]")
    SEARCH_TYPE_OPTION = lambda option_text: (By.XPATH, f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    SEARCH_INPUT = (By.XPATH, "//button[@role='combobox']/following-sibling::input[1]")
    SEARCH_DATEPICKER_INPUT = (By.XPATH, "//button[@role='combobox']/following-sibling::button[1]")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    USER_GROUPS_TABLE = (By.XPATH, "//table[@id='table-admin-user-groups']")
    USER_GROUPS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-user-groups']/tbody/tr")
    HISTORY_BUTTON = (By.XPATH, "//table[@id='table-admin-user-groups']/tbody/tr/td[5]//button[contains(@id,'history')][1]")
    EDIT_BUTTON = (By.XPATH, "//table[@id='table-admin-user-groups']/tbody/tr/td[5]//button[contains(@id,'edit')][1]")
    DELETE_BUTTON = (By.XPATH, "//table[@id='table-admin-user-groups']/tbody/tr/td[5]//button[contains(@id,'delete')][1]")
    HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_DIALOG = (By.XPATH, "//h2[normalize-space(text())='Delete User Group']")
    DELETE_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")
    NEXT_PAGE_BUTTON = (By.XPATH, "//a[@aria-label='Go to next page']")
    PREVIOUS_PAGE_BUTTON = (By.XPATH, "//a[@aria-label='Go to next page']")
    SECOND_PAGE_BUTTON = (By.XPATH, "//a[text()='2']")


class ProgramTypePageLocators:
    """Locators for the Program Type & Patient Program Status page elements."""
    PAGE_TITLE = (By.XPATH, "//h1[normalize-space(text())='Program Type & Patient Program Status']")

    # Tab navigation
    PROGRAM_TAB = (By.XPATH, "//button[normalize-space(text())='Program']")
    PATIENT_PROGRAM_STATUS_TAB = (By.XPATH, "//button[normalize-space(text())='Patient Program Status']")

    # Add buttons
    ADD_NEW_PROGRAM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Add New Program']")
    ADD_NEW_PATIENT_PROGRAM_STATUS_BUTTON = (By.XPATH, "//button[normalize-space(text())='Add New Patient Program Status']")

    # Program tab elements
    PROGRAM_TABLE_HEADERS = (By.XPATH, "//table[contains(@class, 'program-table')]//thead//th")
    PROGRAM_TABLE_ROWS = (By.XPATH, "//table[contains(@class, 'program-table')]//tbody//tr")
    PROGRAM_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Enter program name']")
    PROGRAM_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space(text())='Search']")
    PROGRAM_CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space(text())='Clear']")
    PROGRAM_ENTRIES_DROPDOWN = (By.XPATH, "//select[contains(@class, 'entries-dropdown')]")
    PROGRAM_PAGINATION_INFO = (By.XPATH, "//div[contains(text(), 'Showing')]")

    # Program action buttons (relative to row)
    PROGRAM_ROW = lambda program_name: (By.XPATH, f"//table[contains(@class, 'program-table')]//tbody//tr[td[1][normalize-space(text())='{program_name}']]")
    PROGRAM_EDIT_BUTTON = (By.XPATH, ".//button[contains(@id,'edit')]")
    PROGRAM_VIEW_BUTTON = (By.XPATH, ".//button[contains(@id,'view')]")
    PROGRAM_DELETE_BUTTON = (By.XPATH, ".//button[contains(@id,'delete')]")

    # Patient Program Status tab elements
    PATIENT_PROGRAM_STATUS_TABLE_HEADERS = (By.XPATH, "//table[contains(@class, 'status-table')]//thead//th")
    PATIENT_PROGRAM_STATUS_TABLE_ROWS = (By.XPATH, "//table[contains(@class, 'status-table')]//tbody//tr")
    PATIENT_PROGRAM_STATUS_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search by Status Name']")
    PATIENT_PROGRAM_STATUS_ENTRIES_DROPDOWN = (By.XPATH, "//select[contains(@class, 'entries-dropdown')]")
    PATIENT_PROGRAM_STATUS_PAGINATION_INFO = (By.XPATH, "//div[contains(text(), 'Showing')]")

    # Status action buttons (relative to row)
    PATIENT_PROGRAM_STATUS_ROW = lambda status_name: (By.XPATH, f"//table[contains(@class, 'status-table')]//tbody//tr[td[1][normalize-space(text())='{status_name}']]")
    PATIENT_PROGRAM_STATUS_EDIT_BUTTON = (By.XPATH, ".//button[contains(@id,'edit')]")
    PATIENT_PROGRAM_STATUS_VIEW_BUTTON = (By.XPATH, ".//button[contains(@id,'view')]")
    PATIENT_PROGRAM_STATUS_DELETE_BUTTON = (By.XPATH, ".//button[contains(@id,'delete')]")
