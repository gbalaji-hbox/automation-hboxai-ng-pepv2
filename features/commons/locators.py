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
    # Add New User form locators
    ADD_NEW_USER_BUTTON = (By.XPATH, "//button[@id='users_page_add_btn']")
    FIRST_NAME_INPUT = (By.XPATH, "(//label[normalize-space(text())='First Name *']/following::input)[1]")
    LAST_NAME_INPUT = (By.XPATH, "(//label[normalize-space(text())='Last Name *']/following::input)[1]")
    EMAIL_INPUT = (By.XPATH, "(//label[normalize-space(text())='Email Address *']/following::input)[1]")
    PHONE_INPUT = (By.XPATH, "(//label[normalize-space(text())='Phone Number *']/following::input)[1]")
    PASSWORD_INPUT = (By.XPATH, "(//label[normalize-space()='Password *']/following::input)[1]")
    USER_TYPE_COMBOBOX = (By.XPATH, "(//label[normalize-space(text())='User Type *']/following::button[@role='combobox'])[1]")
    FROM_DATE_BUTTON = (By.XPATH, "//label[text()='From Date *']/following-sibling::button[1]")
    END_DATE_BUTTON = (By.XPATH, "//label[text()='End Date *']/following-sibling::button[1]")
    SCHEDULE_DAY_CHECKBOX = (By.XPATH, "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]")
    START_TIME_HOUR_SELECT = (By.XPATH, "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[1]")
    START_TIME_MINUTE_SELECT = (By.XPATH, "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[2]")
    START_TIME_AM_PM_SELECT = (By.XPATH, "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[3]")
    END_TIME_HOUR_SELECT = (By.XPATH, "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[4]")
    END_TIME_MINUTE_SELECT = (By.XPATH, "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[5]")
    END_TIME_AM_PM_SELECT = (By.XPATH, "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[6]")
    COPY_TO_ALL_DAYS_BUTTON = (By.XPATH, "//span[normalize-space()='Copy to All Days']")
    SAVE_BUTTON = (By.XPATH, "//button[normalize-space(text())='Save']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    USER_CREATE_SUCCESS = (By.XPATH, "//div[normalize-space(text())='User Created']")
    ERROR_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Error']")
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")
    VALIDATION_ERROR = lambda error: (By.XPATH, f"//p[normalize-space(text())='{error}']")

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

    # Add New User Group locators
    ADD_NEW_USER_GROUP_BUTTON = (By.XPATH, "//button[@id='users_page_add_btn']")
    GROUP_NAME_INPUT = (By.XPATH, "//input[@id='user_group_form_name_input']")
    ADD_USERS_BUTTON = (By.XPATH, "//button[@id='user_group_form_add_users_btn']")

    # Add Users Dialog locators
    ADD_USERS_DIALOG = (By.XPATH, "//div[@id='user_group_add_users_dialog']")
    ADD_USERS_SEARCH_INPUT = (By.XPATH, "//input[@id='user_group_modal_search_input']")
    ADD_USERS_FILTER_DROPDOWN = (By.XPATH, "//button[@id='user_group_modal_filter_select']")
    ADD_USER_FILTER_OPTION = lambda option_text: (By.XPATH, f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    ADD_USER_SELECTION_CHECKBOX = (By.XPATH, "//h4/following::div//input[@data-lov-name='input']")
    ADD_USERS_ADD_BUTTON = (By.XPATH, "//button[@id='user_group_modal_add_btn']")
    ADD_USERS_CANCEL_BUTTON = (By.XPATH, "//button[@id='user_group_modal_cancel_btn']")
    ADD_USERS_CLOSE_BUTTON = (By.XPATH, "//div[@id='user_group_add_users_dialog']/button[contains(.,'Close')]")
    USER_CHECKBOX = lambda user_name: (By.XPATH, f"//span[contains(text(),'{user_name}')]/preceding::input[@type='checkbox'][1]")

    # Form buttons
    SAVE_BUTTON = (By.XPATH, "//button[@id='user_group_form_submit_btn']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")

    # Notifications
    USER_GROUP_CREATED_SUCCESS = (By.XPATH, "//div[normalize-space(text())='User Group Created']")
    USER_GROUP_UPDATED_SUCCESS = (By.XPATH, "//div[normalize-space(text())='User group updated successfully']")
    USER_GROUP_DELETED_SUCCESS = (By.XPATH, "//div[normalize-space(text())='User group deleted successfully']")

    # Delete confirm
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")


class ProgramTypePageLocators:
    """Locators for the Program Type & Patient Program Status page elements."""
    PAGE_TITLE = (By.XPATH, "//h1[normalize-space(text())='Program Type & Patient Program Status']")

    # Tab navigation
    PROGRAM_TAB = (By.XPATH, "//button[normalize-space(text())='Program']")
    PATIENT_PROGRAM_STATUS_TAB = (By.XPATH, "//button[normalize-space(text())='Patient Program Status']")

    # Add buttons
    ADD_NEW_PROGRAM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Add New Program']")
    ADD_NEW_PATIENT_PROGRAM_STATUS_BUTTON = (By.XPATH, "//button[normalize-space(text())='Add New Patient Program Status']")

    # Program tab elements - based on actual page structure
    PROGRAM_TABLE_HEADERS = (By.XPATH, "//table//thead//th")
    PROGRAM_TABLE_ROWS = (By.XPATH, "//table//tbody//tr")
    PROGRAM_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Enter program name']")
    PROGRAM_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space(text())='Search']")
    PROGRAM_CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space(text())='Clear']")
    PROGRAM_ENTRIES_DROPDOWN = (By.XPATH, "//button[contains(@role, 'combobox')]//following::button[contains(@aria-label, 'rows per page')]")
    PROGRAM_PAGINATION_INFO = (By.XPATH, "//p[contains(text(), 'Showing')]")

    # Program action buttons (absolute paths for first row)
    PROGRAM_EDIT_BUTTON = (By.XPATH, "//table//tbody//tr[1]//button[contains(@aria-label, 'Edit') or contains(text(), 'Edit')]")
    PROGRAM_VIEW_BUTTON = (By.XPATH, "//table//tbody//tr[1]//button[contains(@aria-label, 'View') or contains(text(), 'View')]")
    PROGRAM_DELETE_BUTTON = (By.XPATH, "//table//tbody//tr[1]//button[contains(@aria-label, 'Delete') or contains(text(), 'Delete')]")

    # Patient Program Status tab elements
    PATIENT_PROGRAM_STATUS_TABLE_HEADERS = (By.XPATH, "//table//thead//th")
    PATIENT_PROGRAM_STATUS_TABLE_ROWS = (By.XPATH, "//table//tbody//tr")
    PATIENT_PROGRAM_STATUS_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search by Status Name']")
    PATIENT_PROGRAM_STATUS_ENTRIES_DROPDOWN = (By.XPATH, "//button[contains(@role, 'combobox')]//following::button[contains(@aria-label, 'rows per page')]")
    PATIENT_PROGRAM_STATUS_PAGINATION_INFO = (By.XPATH, "//p[contains(text(), 'Showing')]")

    # Status action buttons (absolute paths for first row)
    PATIENT_PROGRAM_STATUS_EDIT_BUTTON = (By.XPATH, "//table//tbody//tr[1]//button[contains(@aria-label, 'Edit') or contains(text(), 'Edit')]")
    PATIENT_PROGRAM_STATUS_VIEW_BUTTON = (By.XPATH, "//table//tbody//tr[1]//button[contains(@aria-label, 'View') or contains(text(), 'View')]")
    PATIENT_PROGRAM_STATUS_DELETE_BUTTON = (By.XPATH, "//table//tbody//tr[1]//button[contains(@aria-label, 'Delete') or contains(text(), 'Delete')]")
