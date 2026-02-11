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


class ProgramPageLocators:
    """Locators for the Program Type & Patient Program Status page elements."""

    # Tab navigation
    PROGRAM_TAB = (By.XPATH, "//button[@id='program_type_tab_program']")
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[@id='program_type_clear_btn']")

    # Add buttons
    ADD_NEW_PROGRAM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Add New Program']")

    # Program tab elements - based on actual page structure
    PROGRAM_TABLE = (By.XPATH, "//table[@id='table-admin-program-types']")
    PROGRAM_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-program-types']/tbody/tr")
    PROGRAM_SEARCH_DROPDOWN = (By.XPATH, "//button[@id='program_type_filter_select']")
    DROPDOWN_OPTION = lambda option_text: (By.XPATH, f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    PROGRAM_SEARCH_DATE_PICKER_INPUT = (By.XPATH, "//button[@role='combobox']/following-sibling::button[1]")
    PROGRAM_SEARCH_INPUT = (By.XPATH, "//input[@id='program_type_search_input']")
    PROGRAM_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space(text())='Search']")
    PROGRAM_HISTORY_BUTTON = (By.XPATH, "//table[@id='table-admin-program-types']/tbody/tr/td[last()]//button[contains(@id,'history')][1]")
    PROGRAM_EDIT_BUTTON = (By.XPATH, "//table[@id='table-admin-program-types']/tbody/tr/td[last()]//button[contains(@id,'edit')][1]")
    PROGRAM_DELETE_BUTTON = (By.XPATH, "//table[@id='table-admin-program-types']/tbody/tr/td[last()]//button[contains(@id,'delete')][1]")
    PROGRAM_OPERATION_HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    PROGRAM_OPERATION_HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    PROGRAM_DELETE_CONFIRMATION_DIALOG = (By.XPATH, "//h2[text()='Are you sure?']/following-sibling::p")
    PROGRAM_DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    PROGRAM_PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")

    # Program create/edit form locators
    PROGRAM_NAME_INPUT = (By.XPATH, "//input[@id='program_type_form_name_input']")
    PROGRAM_STATUS_SELECT_DROPDOWN = (By.XPATH, "//button[@id='program_type_form_status_select_btn']")
    PROGRAM_STATUS_OPTIONS = (By.XPATH, "//div[@role='listbox']//div[@role='option']")
    PROGRAM_SAVE_BUTTON = (By.XPATH, "//button[@id='program_type_form_submit_btn']")
    PROGRAM_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    PROGRAM_DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")

    # Notification locators
    PROGRAM_CREATED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Program type created successfully')]")
    PROGRAM_UPDATED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Program type updated successfully.']")
    PROGRAM_DELETED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Program type deleted successfully')]")

class PatientProgramStatusPageLocators:
    """Locators for the Patient Program Status page elements."""

    # Tab navigation
    PATIENT_PROGRAM_STATUS_TAB = (By.XPATH, "//button[@id='program_type_tab_patient_program_status']")

    # Add buttons
    ADD_NEW_PATIENT_PROGRAM_STATUS_BUTTON = (By.XPATH, "//button[normalize-space(text())='Add New Patient Program Status']")

    # Patient Program Status tab elements
    PATIENT_PROGRAM_STATUS_TABLE = (By.XPATH, "//table[@id='table-admin-program-status']")
    PATIENT_PROGRAM_STATUS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-program-status']/tbody/tr")
    DROPDOWN_OPTION = lambda option_text: (By.XPATH, f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    PATIENT_PROGRAM_STATUS_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search by Status Name']")
    PATIENT_PROGRAM_STATUS_HISTORY_BUTTON = (By.XPATH, "//table[@id='table-admin-program-status']/tbody/tr/td[last()]//button[contains(@id,'history')][1]")
    PATIENT_PROGRAM_STATUS_EDIT_BUTTON = (By.XPATH, "//table[@id='table-admin-program-status']/tbody/tr/td[last()]//button[contains(@id,'edit')][1]")
    PATIENT_PROGRAM_STATUS_DELETE_BUTTON = (By.XPATH, "//table[@id='table-admin-program-status']/tbody/tr/td[last()]//button[contains(@id,'delete')][1]")
    PATIENT_PROGRAM_STATUS_OPERATION_HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    PATIENT_PROGRAM_STATUS_OPERATION_HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    PATIENT_PROGRAM_STATUS_DELETE_CONFIRMATION_DIALOG = (By.XPATH, "//h2[text()='Are you sure?']/following-sibling::p")
    PATIENT_PROGRAM_STATUS_DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    PATIENT_PROGRAM_STATUS_PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")

    # Patient Program Status create/edit form locators
    PATIENT_PROGRAM_STATUS_NAME_INPUT = (By.XPATH, "//label[text()='Status Name *']/following-sibling::input")
    PATIENT_PROGRAM_STATUS_SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save Status']")
    PATIENT_PROGRAM_STATUS_UPDATE_BUTTON = (By.XPATH, "//button[normalize-space()='Update Status']")
    PATIENT_PROGRAM_STATUS_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    PATIENT_PROGRAM_STATUS_DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")

    # Patient Program Status notification locators
    PATIENT_PROGRAM_STATUS_CREATED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Program status created successfully')]")
    PATIENT_PROGRAM_STATUS_UPDATED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Program status updated successfully')]")
    PATIENT_PROGRAM_STATUS_DELETED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Program status deleted successfully')]")


class PatientGroupsPageLocators:
    """Locators for the patient groups page elements."""
    SEARCH_TYPE_DROPDOWN = (By.XPATH, "(//button[@role='combobox'])[1]")
    SEARCH_TYPE_OPTION = lambda option_text: (By.XPATH, f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Enter search value...']")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    PATIENT_GROUPS_TABLE = (By.XPATH, "//table[@id='table-admin-patient-groups']")
    PATIENT_GROUPS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-patient-groups']/tbody/tr")
    HISTORY_BUTTON = (By.XPATH, "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'history')][1]")
    EDIT_BUTTON = (By.XPATH, "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'edit')][1]")
    DELETE_BUTTON = (By.XPATH, "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'delete')][1]")
    ARCHIVE_BUTTON = (By.XPATH, "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'archive')][1]")
    DUPLICATE_BUTTON = (By.XPATH, "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'duplicate')][1]")
    HISTORY_DIALOG = (By.XPATH, "//div[@role='dialog']//h2[@id='operations_history_title']")
    HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_DIALOG = (By.XPATH, "//h2[normalize-space(text())='Are you sure?']")
    DELETE_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    DELETE_DIALOG_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Delete']")
    ARCHIVE_DIALOG = (By.XPATH, "//div[@role='alertdialog']//h2[contains(text(), 'Archive')]")
    ARCHIVE_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")
    CREATE_NEW_GROUP_BUTTON = (By.XPATH, "//button[normalize-space()='Create New Group']")
    ARCHIVED_GROUPS_BUTTON = (By.XPATH, "//button[normalize-space()='Archived Groups']")
    CREATE_BY_EMRS_OPTION = (By.XPATH, "//div[@role='menuitem'][normalize-space(text())='Create New Group By EMRs']")
    CREATE_BY_FILTERS_OPTION = (By.XPATH, "//div[@role='menuitem'][normalize-space(text())='Create New Group By Filters']")
    CREATE_BY_EXCEL_OPTION = (By.XPATH, "//div[@role='menuitem'][normalize-space(text())='Create New Group By Excel']")
    BREADCRUMBS_BACK_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Patient Group')]")
    EDIT_BACK_BUTTON = (By.XPATH, "//h1/preceding-sibling::button")

    # Create By Filters locators
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter']")
    FILTER_DIALOG = (By.XPATH, "//div[@role='dialog']//h2[normalize-space(text())='Select Clinics and Providers']")
    FILTER_DIALOG_CLOSE_BUTTON = (By.XPATH, "//span[normalize-space(text())='Close']")
    FILTER_DROPDOWN_SEARCH_INPUT = (By.XPATH, "//input[@role='combobox']")
    FILTERS_CLINIC_DROPDOWN = (By.XPATH, "//h2[normalize-space(text())='Select Clinics and Providers']/following::button[@role='combobox'][1]")
    FILTER_DROPDOWN_SEARCH_OPTION = lambda clinic: (By.XPATH, f"//div[@role='option' and normalize-space(text())='{clinic}']")

    FILTERED_COUNT = (By.XPATH, "//div[contains(normalize-space(),'Filtered count')]")
    SELECT_PATIENTS_INPUT = (By.XPATH, "//input[@placeholder='Enter number']")
    PATIENTS_TABLE = (By.XPATH, "//table[@id='table-admin-patient-list']")
    PATIENTS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-patient-list']/tbody/tr")
    PATIENT_TABLE_ROW_CHECKBOX = lambda row_index: (By.XPATH, f"//table[@id='table-admin-patient-list']/tbody/tr[{row_index}]/td[1]/button[@role='checkbox']")
    PATIENT_TABLE_ROW_EMR = lambda row_index: (By.XPATH, f"//table[@id='table-admin-patient-list']/tbody[1]/tr[{row_index}]/td[2]//span[contains(text(),'EMR')]/span")
    CREATE_BY_FILTERS_APPLY_BUTTON = (By.XPATH, "//button[normalize-space(text())='Apply']")

    # Create Group button
    CREATE_GROUP_BUTTON = (By.XPATH, "//button[normalize-space(text())='Create Group']")
    GROUP_NAME = (By.XPATH, "//h1")

    # Name Patient Group dialog
    GROUP_NAME_DIALOG = (By.XPATH, "//div[@role='dialog']//h2[normalize-space(text())='Name Patient Group']")
    GROUP_NAME_DIALOG_CLOSE_BUTTON = (By.XPATH, "//div[@role='dialog']//button[contains(.,'Close')]")
    GROUP_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter Group Name']")
    GROUP_NAME_INPUT_EXCEL = (By.XPATH, "(//label[contains(.,'Group Name *')]/following::input)[1]")
    GROUP_NOTE_TEXTAREA = (By.XPATH, "//label[normalize-space(text())='Note']/following::textarea")
    GROUP_NAME_SAVE_BUTTON = (By.XPATH, "//button[normalize-space(text())='Save']")
    GROUP_NAME_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    GROUP_NAME_EDIT_FIELD = (By.XPATH, "//input[@placeholder='Enter group name']")
    GROUP_NAME_EDIT_BUTTON = (By.XPATH, "//span[normalize-space()='Group Name']/following::h2/following-sibling::button")
    GROUP_NAME_EDIT_SAVE_BUTTON = (By.XPATH, "//input[@placeholder='Enter group name']/following-sibling::button[1]")
    GROUP_ADD_PATIENTS_BUTTON = (By.XPATH, "//button[normalize-space()='Add Patients']")
    GROUP_REMOVE_PATIENTS_BUTTON = (By.XPATH, "//button[normalize-space()='Remove Patients']")
    GROUP_ADD_SELECTED_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Add Selected')]")
    GROUP_REMOVE_SELECTED_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Remove Selected')]")
    # Create By EMRs locators
    CREATE_BY_EMRS_CLINIC_DROPDOWN = (By.XPATH, "//label[text()='Select Clinic*']/following-sibling::button")
    CREATE_BY_EMR_CINIC_DROPDOWN_SEARCH_INPUT = (By.XPATH, "//input[@role='combobox']")
    CREATE_BY_EMRS_CLINIC_OPTION = lambda clinic: (By.XPATH, f"//div[@role='option' and normalize-space(text())='{clinic}']")
    CREATE_BY_EMRS_TEXTBOX = (By.XPATH, "//textarea[@id='emrs']")
    CREATE_BY_EMRS_PASTE_BUTTON = (By.XPATH, "//button[normalize-space(text())='Paste EMRs']")
    CREATE_BY_EMRS_APPLY_BUTTON = (By.XPATH, "//button[normalize-space(text())='Apply']")
    CREATE_BY_EMRS_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")

    GROUP_EXCEL_UPLOAD_INPUT = (By.XPATH, "//input[@type='file']")

    # Success notification
    FILTER_APPLIED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Filters Applied')]")
    EMR_SEARCH_COMPLETED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Search Complete')]")
    GROUP_CREATED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Group Created Successfully')]")
    EXCEL_GROUP_CREATED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Patient Group Created')]")
    GROUP_NAME_UPDATED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Group name updated successfully.')]")
    GROUP_PATIENT_REMOVED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Patients removed')]")
    GROUP_PATIENT_ADDED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Patients added')]")
    GROUP_DELETED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Patient Group Deleted')]")
    PATIENTS_SELECTED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Patients Selected')]")