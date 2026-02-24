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
    NOTIFICATION_POPUP = (By.XPATH, "//div[@id='appointment-reminder-popup']")
    NOTIFICATION_CLOSE_BUTTON = (By.XPATH, "//button[@id='appointment-reminder-close-btn']")


class UsersPageLocators:
    """Locators for the users page elements."""
    MAIN_DIV = (By.XPATH, "//h3[normalize-space()='Add New User']/ancestor::div[2]")
    USER_TAB = (By.XPATH, "//button[@id='users_page_tab_user']")
    SEARCH_TYPE_DROPDOWN = (By.XPATH, "(//button[@role='combobox'])[1]")
    SEARCH_TYPE_OPTION = lambda option_text: (By.XPATH,
                                              f"//div[@role='option']//span[normalize-space(text())='{option_text}']")
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
    DELETE_DIALOG = (By.XPATH,
                     "//p[normalize-space(text())='This action cannot be undone. This will permanently delete the user.']")
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
    USER_TYPE_COMBOBOX = (By.XPATH,
                          "(//label[normalize-space(text())='User Type *']/following::button[@role='combobox'])[1]")
    FROM_DATE_BUTTON = (By.XPATH, "//label[text()='From Date *']/following-sibling::button[1]")
    END_DATE_BUTTON = (By.XPATH, "//label[text()='End Date *']/following-sibling::button[1]")
    SCHEDULE_DAY_CHECKBOX = (By.XPATH,
                             "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]")
    START_TIME_HOUR_SELECT = (By.XPATH,
                              "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[1]")
    START_TIME_MINUTE_SELECT = (By.XPATH,
                                "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[2]")
    START_TIME_AM_PM_SELECT = (By.XPATH,
                               "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[3]")
    END_TIME_HOUR_SELECT = (By.XPATH,
                            "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[4]")
    END_TIME_MINUTE_SELECT = (By.XPATH,
                              "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[5]")
    END_TIME_AM_PM_SELECT = (By.XPATH,
                             "//label[normalize-space(text())='User Schedule']/following::button[@role='checkbox'][1]/following::select[6]")
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
    SEARCH_TYPE_OPTION = lambda option_text: (By.XPATH,
                                              f"//div[@role='option']//span[normalize-space(text())='{option_text}']")
    SEARCH_INPUT = (By.XPATH, "//button[@role='combobox']/following-sibling::input[1]")
    SEARCH_DATEPICKER_INPUT = (By.XPATH, "//button[@role='combobox']/following-sibling::button[1]")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    USER_GROUPS_TABLE = (By.XPATH, "//table[@id='table-admin-user-groups']")
    USER_GROUPS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-user-groups']/tbody/tr")
    HISTORY_BUTTON = (By.XPATH,
                      "//table[@id='table-admin-user-groups']/tbody/tr/td[5]//button[contains(@id,'history')][1]")
    EDIT_BUTTON = (By.XPATH, "//table[@id='table-admin-user-groups']/tbody/tr/td[5]//button[contains(@id,'edit')][1]")
    DELETE_BUTTON = (By.XPATH,
                     "//table[@id='table-admin-user-groups']/tbody/tr/td[5]//button[contains(@id,'delete')][1]")
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
    ADD_USER_FILTER_OPTION = lambda option_text: (By.XPATH,
                                                  f"//div[@role='option']//span[normalize-space(text())='{option_text}']")
    ADD_USER_SELECTION_CHECKBOX = (By.XPATH, "(//h4/following::input[@type='checkbox'])[1]")
    ADD_USERS_ADD_BUTTON = (By.XPATH, "//button[@id='user_group_modal_add_btn']")
    ADD_USERS_CANCEL_BUTTON = (By.XPATH, "//button[@id='user_group_modal_cancel_btn']")
    ADD_USERS_CLOSE_BUTTON = (By.XPATH, "//div[@id='user_group_add_users_dialog']/button[contains(.,'Close')]")
    USER_CHECKBOX = lambda user_name: (By.XPATH,
                                       f"//span[contains(text(),'{user_name}')]/preceding::input[@type='checkbox'][1]")

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
    DROPDOWN_OPTION = lambda option_text: (By.XPATH,
                                           f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    PROGRAM_SEARCH_DATE_PICKER_INPUT = (By.XPATH, "//button[@role='combobox']/following-sibling::button[1]")
    PROGRAM_SEARCH_INPUT = (By.XPATH, "//input[@id='program_type_search_input']")
    PROGRAM_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space(text())='Search']")
    PROGRAM_HISTORY_BUTTON = (By.XPATH,
                              "//table[@id='table-admin-program-types']/tbody/tr/td[last()]//button[contains(@id,'history')][1]")
    PROGRAM_EDIT_BUTTON = (By.XPATH,
                           "//table[@id='table-admin-program-types']/tbody/tr/td[last()]//button[contains(@id,'edit')][1]")
    PROGRAM_DELETE_BUTTON = (By.XPATH,
                             "//table[@id='table-admin-program-types']/tbody/tr/td[last()]//button[contains(@id,'delete')][1]")
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
    ADD_NEW_PATIENT_PROGRAM_STATUS_BUTTON = (By.XPATH,
                                             "//button[normalize-space(text())='Add New Patient Program Status']")

    # Patient Program Status tab elements
    PATIENT_PROGRAM_STATUS_TABLE = (By.XPATH, "//table[@id='table-admin-program-status']")
    PATIENT_PROGRAM_STATUS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-program-status']/tbody/tr")
    DROPDOWN_OPTION = lambda option_text: (By.XPATH,
                                           f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    PATIENT_PROGRAM_STATUS_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search by Status Name']")
    PATIENT_PROGRAM_STATUS_HISTORY_BUTTON = (By.XPATH,
                                             "//table[@id='table-admin-program-status']/tbody/tr/td[last()]//button[contains(@id,'history')][1]")
    PATIENT_PROGRAM_STATUS_EDIT_BUTTON = (By.XPATH,
                                          "//table[@id='table-admin-program-status']/tbody/tr/td[last()]//button[contains(@id,'edit')][1]")
    PATIENT_PROGRAM_STATUS_DELETE_BUTTON = (By.XPATH,
                                            "//table[@id='table-admin-program-status']/tbody/tr/td[last()]//button[contains(@id,'delete')][1]")
    PATIENT_PROGRAM_STATUS_OPERATION_HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    PATIENT_PROGRAM_STATUS_OPERATION_HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    PATIENT_PROGRAM_STATUS_DELETE_CONFIRMATION_DIALOG = (By.XPATH, "//h2[text()='Are you sure?']/following-sibling::p")
    PATIENT_PROGRAM_STATUS_DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON = (By.XPATH,
                                                                       "//button[normalize-space(text())='Cancel']")
    PATIENT_PROGRAM_STATUS_PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")

    # Patient Program Status create/edit form locators
    PATIENT_PROGRAM_STATUS_NAME_INPUT = (By.XPATH, "//label[text()='Status Name *']/following-sibling::input")
    PATIENT_PROGRAM_STATUS_SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save Status']")
    PATIENT_PROGRAM_STATUS_UPDATE_BUTTON = (By.XPATH, "//button[normalize-space()='Update Status']")
    PATIENT_PROGRAM_STATUS_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    PATIENT_PROGRAM_STATUS_DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")

    # Patient Program Status notification locators
    PATIENT_PROGRAM_STATUS_CREATED_NOTIFICATION = (By.XPATH,
                                                   "//div[contains(text(),'Program status created successfully')]")
    PATIENT_PROGRAM_STATUS_UPDATED_NOTIFICATION = (By.XPATH,
                                                   "//div[contains(text(),'Program status updated successfully')]")
    PATIENT_PROGRAM_STATUS_DELETED_NOTIFICATION = (By.XPATH,
                                                   "//div[contains(text(),'Program status deleted successfully')]")


class PatientGroupsPageLocators:
    """Locators for the patient groups page elements."""
    SEARCH_TYPE_DROPDOWN = (By.XPATH, "(//button[@role='combobox'])[1]")
    SEARCH_TYPE_OPTION = lambda option_text: (By.XPATH,
                                              f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Enter search value...']")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    CLEAR_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    PATIENT_GROUPS_TABLE = (By.XPATH, "//table[@id='table-admin-patient-groups']")
    PATIENT_GROUPS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-patient-groups']/tbody/tr")
    HISTORY_BUTTON = (By.XPATH,
                      "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'history')][1]")
    EDIT_BUTTON = (By.XPATH,
                   "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'edit')][1]")
    DELETE_BUTTON = (By.XPATH,
                     "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'delete')][1]")
    ARCHIVE_BUTTON = (By.XPATH,
                      "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'archive')][1]")
    DUPLICATE_BUTTON = (By.XPATH,
                        "//table[@id='table-admin-patient-groups']/tbody/tr/td[last()]//button[contains(@id,'duplicate')][1]")
    HISTORY_DIALOG = (By.XPATH, "//div[@role='dialog']//h2[@id='operations_history_title']")
    HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_DIALOG = (By.XPATH, "//h2[normalize-space(text())='Are you sure?']")
    DELETE_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    DELETE_DIALOG_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='Delete']")
    ARCHIVE_DIALOG = (By.XPATH, "//div[@role='alertdialog']//h2[contains(text(), 'Archive')]")
    ARCHIVE_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    ARCHIVE_DIALOG_ARCHIVE_BUTTON = (By.XPATH, "//button[normalize-space(text())='Archive']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")

    # Status locators
    ACTIVE_STATUS = (By.XPATH, "//td[normalize-space(text())='Active']")
    ARCHIVED_STATUS = (By.XPATH, "//td[normalize-space(text())='Archived']")
    CREATE_NEW_GROUP_BUTTON = (By.XPATH, "//button[normalize-space()='Create New Group']")
    ARCHIVED_GROUPS_BUTTON = (By.XPATH, "//button[normalize-space()='Archived Groups']")
    CREATE_BY_EMRS_OPTION = (By.XPATH, "//div[@role='menuitem'][normalize-space(text())='Create New Group By EMRs']")
    CREATE_BY_FILTERS_OPTION = (By.XPATH,
                                "//div[@role='menuitem'][normalize-space(text())='Create New Group By Filters']")
    CREATE_BY_EXCEL_OPTION = (By.XPATH, "//div[@role='menuitem'][normalize-space(text())='Create New Group By Excel']")
    BREADCRUMBS_BACK_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Patient Group')]")
    EDIT_BACK_BUTTON = (By.XPATH, "//h1/preceding-sibling::button")

    # Create By Filters locators
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter']")
    FILTER_DIALOG = (By.XPATH, "//div[@role='dialog']//h2[normalize-space(text())='Select Clinics and Providers']")
    FILTER_DIALOG_CLOSE_BUTTON = (By.XPATH, "//span[normalize-space(text())='Close']")
    FILTER_DROPDOWN_SEARCH_INPUT = (By.XPATH, "//input[@role='combobox']")
    FILTERS_CLINIC_DROPDOWN = (By.XPATH,
                               "//h2[normalize-space(text())='Select Clinics and Providers']/following::button[@role='combobox'][1]")
    FILTER_DROPDOWN_SEARCH_OPTION = lambda clinic: (By.XPATH,
                                                    f"//div[@role='option' and normalize-space(text())='{clinic}']")

    FILTERED_COUNT = (By.XPATH, "//div[contains(normalize-space(),'Filtered count')]")
    SELECT_PATIENTS_INPUT = (By.XPATH, "//input[@placeholder='Enter number']")
    PATIENTS_TABLE = (By.XPATH, "//table[@id='table-admin-patient-list']")
    PATIENTS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-patient-list']/tbody/tr")
    PATIENT_TABLE_ROW_CHECKBOX = lambda row_index: (By.XPATH,
                                                    f"//table[@id='table-admin-patient-list']/tbody/tr[{row_index}]/td[1]/button[@role='checkbox']")
    PATIENT_TABLE_ROW_EMR = lambda row_index: (By.XPATH,
                                               f"//table[@id='table-admin-patient-list']/tbody[1]/tr[{row_index}]/td[2]//span[contains(text(),'EMR')]/span")
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
    GROUP_NAME_EDIT_BUTTON = (By.XPATH,
                              "//span[normalize-space()='Group Name']/following::h2/following-sibling::button")
    GROUP_NAME_EDIT_SAVE_BUTTON = (By.XPATH, "//input[@placeholder='Enter group name']/following-sibling::button[1]")
    GROUP_ADD_PATIENTS_BUTTON = (By.XPATH, "//button[normalize-space()='Add Patients']")
    GROUP_REMOVE_PATIENTS_BUTTON = (By.XPATH, "//button[normalize-space()='Remove Patients']")
    GROUP_ADD_SELECTED_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Add Selected')]")
    GROUP_REMOVE_SELECTED_BUTTON = (By.XPATH, "//button[contains(normalize-space(),'Remove Selected')]")
    # Create By EMRs locators
    CREATE_BY_EMRS_CLINIC_DROPDOWN = (By.XPATH, "//label[text()='Select Clinic*']/following-sibling::button")
    CREATE_BY_EMR_CINIC_DROPDOWN_SEARCH_INPUT = (By.XPATH, "//input[@role='combobox']")
    CREATE_BY_EMRS_CLINIC_OPTION = lambda clinic: (By.XPATH,
                                                   f"//div[@role='option' and normalize-space(text())='{clinic}']")
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
    GROUP_DUPLICATED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Success')]")
    GROUP_ARCHIVED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Patient Group Archived')]")
    GROUP_UNARCHIVED_NOTIFICATION = (By.XPATH, "//div[contains(text(),'Success')]")

    # Archive Dialog locators
    ARCHIVE_DIALOG_TITLE = (By.XPATH, "//h2[normalize-space(text())='Archive Patient Group']")
    ARCHIVE_DIALOG_MESSAGE = (By.XPATH, "//p[contains(text(),'archive this patient group')]")

    # Unarchive Dialog locators
    UNARCHIVE_DIALOG_TITLE = (By.XPATH, "//h2[normalize-space(text())='Are you sure?']")
    UNARCHIVE_DIALOG_CANCEL_BUTTON = (By.XPATH,
                                      "//h2[normalize-space(text())='Are you sure?']/following::button[normalize-space(text())='Cancel']")
    UNARCHIVE_DIALOG_UNARCHIVE_BUTTON = (By.XPATH,
                                         "//h2[normalize-space(text())='Are you sure?']/following::button[normalize-space(text())='Unarchive']")

    # Archived Groups Page locators
    ARCHIVED_GROUPS_PAGE_HEADING = (By.XPATH, "//h1[normalize-space(text())='Archived Patient Groups']")
    BACK_TO_PATIENT_GROUPS_BUTTON = (By.XPATH, "//button[normalize-space(text())='Back to Patient Groups']")
    UNARCHIVE_BUTTON = (By.XPATH, "//button[normalize-space(text())='Unarchive']")
    ARCHIVED_GROUP_TABLE = (By.XPATH, "//table[@id='table-admin-archived-patient-groups']")
    ARCHIVED_GROUP_ROWS = (By.XPATH, "//table[@id='table-admin-archived-patient-groups']/tbody/tr")
    ARCHIVED_GROUP_ID = (By.XPATH, ".//td[1]")
    ARCHIVED_GROUP_NAME = (By.XPATH, ".//td[2]")
    ARCHIVED_GROUP_PATIENT_COUNT = (By.XPATH, ".//td[3]")
    ARCHIVED_GROUP_STATUS = (By.XPATH, ".//td[4]")
    ARCHIVED_GROUP_ACTIONS = (By.XPATH, ".//td[5]//button")

    # Duplicate Page locators
    DUPLICATE_PAGE_HEADING = (By.XPATH, "//h1[normalize-space(text())='Duplicate Patient Group']")
    DUPLICATE_FROM_LABEL = (By.XPATH, "//p[contains(text(),'Duplicating from:')]")
    DUPLICATE_NEW_GROUP_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter new group name']")
    DUPLICATE_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")


class WorkflowPageLocators:
    """Locators for Workflow tab under Workflow & Tasks page."""
    WORKFLOW_TAB = (By.XPATH, "//button[@role='tab' and normalize-space()='Workflow']")
    CREATE_NEW_WORKFLOW_BUTTON = (By.XPATH, "//button[normalize-space()='Create New Workflow']")
    WORKFLOW_TABLE = (By.XPATH, "//table[@id='table-admin-workflows']")
    WORKFLOW_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-workflows']/tbody/tr")
    WORKFLOW_SEARCH_DROPDOWN = (By.XPATH,
                                "//button[@role='combobox'][.//span[normalize-space()='Workflow Name'] or normalize-space()='Workflow Name']")
    DROPDOWN_OPTION = lambda option_text: (By.XPATH,
                                           f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    APPLICABLE_PROGRAM_OPTION = lambda program_name: (By.XPATH,
                                                      f"//div[@role='option' and normalize-space(text())='{program_name}']")
    WORKFLOW_SEARCH_INPUT = (By.XPATH, "//button[normalize-space()='Search']/preceding-sibling::input")
    WORKFLOW_ASSIGNED_GROUP_DROPDOWN = (By.XPATH, "//button[normalize-space()='Select user groups...']")
    WORKFLOW_ASSIGNED_GROUP_SEARCH_INPUT = (By.XPATH,
                                            "//button[normalize-space()='Select user groups...']/following::input[@placeholder='Search user groups...']")
    WORKFLOW_ASSIGNED_GROUP_OPTION = lambda group_name: (By.XPATH,
                                                         f"//div[@role='option']/following::span[normalize-space(text())='{group_name}']")
    WORKFLOW_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    WORKFLOW_HISTORY_BUTTON = (By.XPATH,
                               "//table[@id='table-admin-workflows']/tbody/tr[1]/td[last()]//button[contains(@id,'history')][1]")
    WORKFLOW_EDIT_BUTTON = (By.XPATH,
                            "//table[@id='table-admin-workflows']/tbody/tr[1]/td[last()]//button[contains(@id,'edit')][1]")
    WORKFLOW_DELETE_BUTTON = (By.XPATH,
                              "//table[@id='table-admin-workflows']/tbody/tr[1]/td[last()]//button[contains(@id,'delete')][1]")
    OPERATION_HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    OPERATION_HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_CONFIRMATION_DIALOG = (By.XPATH, "//h2[normalize-space(text())='Are you sure?']/following-sibling::p")
    DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")

    WORKFLOW_NAME_INPUT = (By.XPATH,
                           "//label[normalize-space()='Workflow Name']/following::input[@name='workflowName']")
    APPLICABLE_PROGRAMS_DROPDOWN = (By.XPATH,
                                    "//label[normalize-space()='Applicable Programs']/following::button[@role='combobox'][1]")
    DROPDOWN_FIRST_OPTION = (By.XPATH, "//div[@role='listbox']//div[@role='option'][1]")

    TRIGGER_WORKFLOW_DROPDOWN = (By.XPATH,
                                 "//table[.//th[normalize-space()='Workflow']]//tbody/tr[1]/td[1]//button[@role='combobox'][1]")
    TRIGGER_STATUS_DROPDOWN = (By.XPATH,
                               "//table[.//th[normalize-space()='Workflow']]//tbody/tr[1]/td[2]//button[@role='combobox'][1]")
    TRIGGER_ROW_DELETE_BUTTON = (By.XPATH,
                                 "//table[.//th[normalize-space()='Workflow']]//tbody/tr[1]/td[last()]//button")
    ADD_TRIGGER_BUTTON = (By.XPATH, "//button[normalize-space()='Add Trigger']")
    SECOND_TRIGGER_ROW_DELETE_BUTTON = (By.XPATH,
                                        "//table[.//th[normalize-space()='Workflow']]//tbody/tr[2]/td[last()]//button")

    ATTEMPT_TASK_DROPDOWN = (By.XPATH,
                             "//table[.//th[normalize-space()='Attempt No.']]//tbody/tr[1]/td[2]//button[@role='combobox'][1]")
    ATTEMPT_TASK_OPTION = lambda option_text: (By.XPATH,
                                               f"//div[@role='option' and normalize-space(text())='{option_text}']")
    ATTEMPT_WAITING_PERIOD_INPUT = (By.XPATH,
                                    "//table[.//th[normalize-space()='Attempt No.']]//tbody/tr[1]//input[@type='number' or @role='spinbutton']")
    ADD_ATTEMPT_BUTTON = (By.XPATH, "//button[normalize-space()='Add Attempt']")
    SECOND_ATTEMPT_DELETE_BUTTON = (By.XPATH,
                                    "//table[.//th[normalize-space()='Attempt No.']]//tbody/tr[2]/td[last()]//button")

    USER_GROUP_DROPDOWN = (By.XPATH, "//label[contains(.,'User Group *')]/following::button[@role='combobox']")
    USER_GROUP_OPTION_SEARCH_INPUT = (By.XPATH,
                                      "//label[contains(.,'User Group *')]/following::button[@role='combobox']/following::input[@placeholder='Search user groups...']")

    CREATE_WORKFLOW_BUTTON = (By.XPATH, "//button[normalize-space()='Create Workflow']")
    UPDATE_WORKFLOW_BUTTON = (By.XPATH, "//button[normalize-space()='Update Workflow']")
    WORKFLOW_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")

    WORKFLOW_CREATED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Workflow Created']")
    WORKFLOW_UPDATED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Workflow Updated']")
    WORKFLOW_DELETED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Success']")


class ActivitiesPageLocators:
    """Locators for the Activities page elements."""
    ACTIVITIES_TABLE = (By.XPATH, "//table[@id='table-admin-activities']")
    ACTIVITIES_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-activities']/tbody/tr")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search by Activity Name']")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    CLEAR_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")
    DROPDOWN_OPTION = lambda option_text: (
        By.XPATH,
        f"//div[@role='option']/span[normalize-space(text())='{option_text}']",
    )
    ADD_NEW_ACTIVITY_BUTTON = (By.XPATH, "//button[normalize-space()='Add New Activity']")

    HISTORY_BUTTON = (By.XPATH,
                      "//table[@id='table-admin-activities']/tbody/tr[1]/td[last()]//button[contains(@id,'history')][1]")
    DUPLICATE_BUTTON = (By.XPATH,
                        "//table[@id='table-admin-activities']/tbody/tr[1]/td[last()]//button[contains(@id,'duplicate')][1]")
    EDIT_BUTTON = (By.XPATH,
                   "//table[@id='table-admin-activities']/tbody/tr[1]/td[last()]//button[contains(@id,'edit')][1]")
    DELETE_BUTTON = (By.XPATH,
                     "//table[@id='table-admin-activities']/tbody/tr[1]/td[last()]//button[contains(@id,'delete')][1]")

    OPERATION_HISTORY_DIALOG = (By.XPATH, "//div[@role='dialog']//h2[normalize-space()='Activity Operation History']")
    OPERATION_HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_CONFIRMATION_DIALOG = (By.XPATH, "//div[@role='alertdialog']//h2[normalize-space()='Are you sure?']")
    DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")

    ACTIVITY_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter activity name']")
    PATIENT_GROUP_DROPDOWN = (By.XPATH,
                              "//label[normalize-space(text())='Patient Group *']/following-sibling::button")
    PATIENT_GROUP_SEARCH_INPUT = (By.XPATH,
                                  "//label[normalize-space(text())='Patient Group *']/following-sibling::button/following::input[@placeholder='Search patient groups...']")
    PATIENT_GROUP_OPTION = lambda option_text: (
        By.XPATH,
        f"//div[@role='option']//span[normalize-space(text())='{option_text}']",
    )
    PATIENT_GROUP_FIRST_OPTION = (By.XPATH, "//div[@role='option'][1]")
    WORKFLOW_DROPDOWN = (By.XPATH, "//label[normalize-space(text())='Workflow *']/following-sibling::button")
    WORKFLOW_SEARCH_INPUT = (By.XPATH,
                             "//label[normalize-space(text())='Workflow *']/following-sibling::button/following::input[@placeholder='Search workflows...']")
    WORKFLOW_OPTION = lambda option_text: (
        By.XPATH,
        f"//div[@role='option']//span[normalize-space(text())='{option_text}']",
    )
    WORKFLOW_FIRST_OPTION = (By.XPATH, "//div[@role='option'][1]")

    FROM_DATE_BUTTON = (By.XPATH, "//label[normalize-space(text())='From Date *']/following-sibling::button")
    END_DATE_BUTTON = (By.XPATH, "//label[normalize-space(text())='End Date *']/following-sibling::button")
    TIMEZONE_DROPDOWN = (By.XPATH, "//label[normalize-space(text())='Timezone']/following-sibling::button")
    ACTIVITY_SCHEDULE_CHECKBOX = (By.XPATH, "(//label[normalize-space(text())='Timezone']/following::input)[1]")
    FROM_HH_INPUT = (By.XPATH, "//label[normalize-space(text())='From Time *']/following::select[1]")
    FROM_MM_INPUT = (By.XPATH, "//label[normalize-space(text())='From Time *']/following::select[2]")
    FROM_AMPM_INPUT = (By.XPATH, "//label[normalize-space(text())='From Time *']/following::select[3]")
    END_HH_INPUT = (By.XPATH, "//label[normalize-space(text())='To Time *']/following::select[1]")
    END_MM_INPUT = (By.XPATH, "//label[normalize-space(text())='To Time *']/following::select[2]")
    END_AMPM_INPUT = (By.XPATH, "//label[normalize-space(text())='To Time *']/following::select[3]")
    COPY_TO_ALL_BUTTON = (By.XPATH, "//button[contains(.,'Copy to All Days')]")

    ACTIVE_DAY_CHECKBOX = lambda day: (
        By.XPATH,
        f"//label[normalize-space(text())='{day}']/preceding-sibling::button[@role='checkbox']",
    )
    ADD_ANOTHER_SLOT_BUTTON = (By.XPATH, "//button[normalize-space()='Add Another Slot']")

    SAVE_ACTIVITY_BUTTON = (By.XPATH, "//button[normalize-space()='Save Activity']")
    CANCEL_ACTIVITY_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CREATE_DUPLICATE_BUTTON = (By.XPATH, "//button[normalize-space()='Create Duplicate']")
    UPDATE_ACTIVITY_BUTTON = (By.XPATH, "//button[normalize-space()='Update Activity']")

    ACTIVITY_CREATED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Activity created successfully']")


class WorkflowStatusPageLocators:
    """Locators for Workflow Status tab under Workflow & Tasks page."""
    WORKFLOW_STATUS_TAB = (By.XPATH, "//button[@role='tab' and normalize-space()='Workflow Status']")
    ADD_NEW_WORKFLOW_STATUS_BUTTON = (By.XPATH, "//button[normalize-space()='Add New Workflow Status']")
    WORKFLOW_STATUS_TABLE = (By.XPATH, "//table[@id='table-admin-workflow-statuses']")
    WORKFLOW_STATUS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-workflow-statuses']/tbody/tr")
    WORKFLOW_STATUS_SEARCH_INPUT = (By.XPATH, "//button[normalize-space()='Search']/preceding-sibling::input")
    WORKFLOW_STATUS_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    WORKFLOW_STATUS_CLEAR_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    WORKFLOW_STATUS_HISTORY_BUTTON = (By.XPATH,
                                      "//table[@id='table-admin-workflow-statuses']/tbody/tr[1]/td[last()]//button[contains(@id,'history')][1]")
    WORKFLOW_STATUS_EDIT_BUTTON = (By.XPATH,
                                   "//table[@id='table-admin-workflow-statuses']/tbody/tr[1]/td[last()]//button[contains(@id,'edit')][1]")
    WORKFLOW_STATUS_DELETE_BUTTON = (By.XPATH,
                                     "//table[@id='table-admin-workflow-statuses']/tbody/tr[1]/td[last()]//button[contains(@id,'delete')][1]")
    OPERATION_HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    OPERATION_HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_CONFIRMATION_DIALOG = (By.XPATH, "//h2[normalize-space(text())='Are you sure?']/following-sibling::p")
    DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")
    DROPDOWN_OPTION = lambda option_text: (By.XPATH,
                                           f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    WORKFLOW_STATUS_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter workflow status name']")
    WORKFLOW_STATUS_SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")
    WORKFLOW_STATUS_UPDATE_BUTTON = (By.XPATH, "//button[normalize-space()='Update']")
    WORKFLOW_STATUS_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    WORKFLOW_STATUS_EDIT_BUTTON_BY_NAME = lambda name: (
        By.XPATH,
        f"//table[.//th[normalize-space()='Workflow Status Name']]//tr[td[1][normalize-space()='{name}']]//button[contains(@id,'edit')][1]",
    )
    WORKFLOW_STATUS_DELETE_BUTTON_BY_NAME = lambda name: (
        By.XPATH,
        f"//table[.//th[normalize-space()='Workflow Status Name']]//tr[td[1][normalize-space()='{name}']]//button[contains(@id,'delete')][1]",
    )
    WORKFLOW_STATUS_CREATED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Workflow Status Added']")
    WORKFLOW_STATUS_UPDATED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Workflow Status Updated']")
    WORKFLOW_STATUS_DELETED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Workflow Status Deleted']")


class TasksPageLocators:
    """Locators for Tasks tab under Workflow & Tasks page."""
    TASKS_TAB = (By.XPATH, "//button[@role='tab' and normalize-space()='Tasks']")
    ADD_NEW_TASK_BUTTON = (By.XPATH, "//button[normalize-space()='Add New Task']")
    TASKS_TABLE = (By.XPATH, "//table[@id='table-admin-workflow-tasks']")
    TASKS_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-workflow-tasks']/tbody/tr")
    TASKS_SEARCH_INPUT = (By.XPATH, "//button[normalize-space()='Search']/preceding-sibling::input")
    TASKS_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    TASK_CLEAR_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    TASKS_HISTORY_BUTTON = (By.XPATH,
                            "//table[@id='table-admin-workflow-tasks']/tbody/tr[1]/td[last()]//button[contains(@id,'history')][1]")
    TASKS_EDIT_BUTTON = (By.XPATH,
                         "//table[@id='table-admin-workflow-tasks']/tbody/tr[1]/td[last()]//button[contains(@id,'edit')][1]")
    TASKS_DELETE_BUTTON = (By.XPATH,
                           "//table[@id='table-admin-workflow-tasks']/tbody/tr[1]/td[last()]//button[contains(@id,'delete')][1]")
    OPERATION_HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    OPERATION_HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_CONFIRMATION_DIALOG = (By.XPATH, "//h2[normalize-space(text())='Are you sure?']")
    DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")
    DROPDOWN_OPTION = lambda option_text: (By.XPATH,
                                           f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    TASK_NAME_INPUT = (By.XPATH, "//input[@id='task_form_name_input']")
    TASK_SAVE_BUTTON = (By.XPATH, "//button[normalize-space()='Save']")
    TASK_UPDATE_BUTTON = (By.XPATH, "//button[normalize-space()='Update']")
    TASK_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    TASK_EDIT_BUTTON_BY_NAME = lambda name: (
        By.XPATH,
        f"//table[.//th[normalize-space()='Task Name']]//tr[td[1][normalize-space()='{name}']]//button[contains(@id,'edit')][1]",
    )
    TASK_DELETE_BUTTON_BY_NAME = lambda name: (
        By.XPATH,
        f"//table[.//th[normalize-space()='Task Name']]//tr[td[1][normalize-space()='{name}']]//button[contains(@id,'delete')][1]",
    )
    TASK_CREATED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Task Added']")
    TASK_UPDATED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Task Updated']")
    TASK_DELETED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Task Deleted']")


class FacilityAvailabilityPageLocators:
    """Locators for Facility Availability page elements."""
    FACILITY_AVAILABILITY_TABLE = (By.XPATH, "//table[@id='table-admin-facility-availability']")
    FACILITY_AVAILABILITY_TABLE_ROWS = (By.XPATH, "//table[@id='table-admin-facility-availability']/tbody/tr")
    FACILITY_AVAILABILITY_PAGINATION = (By.XPATH, "//nav[@aria-label='pagination']")
    FACILITY_AVAILABILITY_SEARCH_DROPDOWN = (By.XPATH,
                                             "//button[normalize-space()='Search']/preceding::button[@role='combobox']")
    FACILITY_AVAILABILITY_SEARCH_INPUT = (By.XPATH, "//button[normalize-space()='Search']/preceding-sibling::input")
    FACILITY_AVAILABILITY_SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    FACILITY_AVAILABILITY_CLEAR_BUTTON = (By.XPATH, "//button[normalize-space()='Clear']")
    DROPDOWN_OPTION = lambda option_text: (By.XPATH,
                                           f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    FACILITY_AVAILABILITY_HISTORY_BUTTON = (By.XPATH,
                                            "//table[@id='table-admin-facility-availability']/tbody/tr[1]/td[last()]//button[contains(@id,'history')][1]")
    FACILITY_AVAILABILITY_EDIT_BUTTON = (By.XPATH,
                                         "//table[@id='table-admin-facility-availability']/tbody/tr[1]/td[last()]//button[contains(@id,'edit')][1]")
    FACILITY_AVAILABILITY_DELETE_BUTTON = (By.XPATH,
                                           "//table[@id='table-admin-facility-availability']/tbody/tr[1]/td[last()]//button[contains(@id,'delete')][1]")
    OPERATION_HISTORY_DIALOG = (By.XPATH, "//div[@id='operations_history_dialog']")
    OPERATION_HISTORY_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[contains(.,'Close')]")
    DELETE_CONFIRMATION_DIALOG = (By.XPATH, "//h2[normalize-space(text())='Delete Facility Availability']")
    DELETE_CONFIRMATION_DIALOG_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")
    DELETE_CONFIRMATION_DIALOG_CONFIRM_BUTTON = (By.XPATH, "//button[normalize-space(text())='Delete']")
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//span[text()='Show']/following-sibling::button")

    # Create/Edit form locators
    ADD_NEW_FACILITY_AVAILABILITY_BUTTON = (By.XPATH,
                                            "//button[normalize-space(text())='Add New Facility Availability']")
    SELECT_CLINIC_DROPDOWN = (By.XPATH, "//label[@for='clinic']/following-sibling::button")
    FACILITY_DROPDOWN_OPTION = lambda option: (By.XPATH,
                                               f"//div[@role='option' and normalize-space(text())='{option}']")
    SELECT_SEARCH_CLINIC_INPUT = (By.XPATH, "//label[@for='clinic']/following::input[@placeholder='Search clinic...']")
    SELECT_FACILITY_DROPDOWN = (By.XPATH, "//label[@for='facility']/following-sibling::button[1]")
    FROM_DATE_BUTTON = (By.XPATH, "//label[contains(.,'From Date *')]/following-sibling::button[1]")
    TO_DATE_BUTTON = (By.XPATH, "//label[contains(.,'To Date *')]/following-sibling::button")
    TIMEZONE_DROPDOWN = (By.XPATH, "//label[text()='Timezone']/following-sibling::button")

    SCHEDULE_DAY_CHECKBOX = (By.XPATH,
                             "//h3[normalize-space()='Facility Schedule']/following::input[@type='checkbox'][1]")
    START_TIME_HOUR_SELECT = (By.XPATH, "//button[contains(@id,'from-hour')]/following::select[1]")
    START_TIME_MINUTE_SELECT = (By.XPATH, "//button[contains(@id,'from-minute')]/following::select[1]")
    START_TIME_AM_PM_SELECT = (By.XPATH, "//button[contains(@id,'from-period')]/following::select[1]")
    END_TIME_HOUR_SELECT = (By.XPATH, "//button[contains(@id,'to-hour')]/following::select[1]")
    END_TIME_MINUTE_SELECT = (By.XPATH, "//button[contains(@id,'to-minute')]/following::select[1]")
    END_TIME_AM_PM_SELECT = (By.XPATH, "//button[contains(@id,'to-period')]/following::select[1]")

    COPY_TO_ALL_DAYS_BUTTON = (By.XPATH, "//span[normalize-space()='Copy to All Days']")

    CREATE_FACILITY_AVAILABILITY_BUTTON = (By.XPATH, "//button[normalize-space(text())='Create Facility Availability']")
    UPDATE_FACILITY_AVAILABILITY_BUTTON = (By.XPATH, "//button[normalize-space(text())='Update Facility Availability']")
    FACILITY_AVAILABILITY_FORM_CANCEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Cancel']")

    FACILITY_AVAILABILITY_CREATED_NOTIFICATION = (By.XPATH,
                                                  "//div[contains(normalize-space(text()),'Facility availability created successfully')]")
    FACILITY_AVAILABILITY_UPDATED_NOTIFICATION = (By.XPATH,
                                                  "//div[contains(normalize-space(text()),'Facility availability updated successfully')]")
    FACILITY_AVAILABILITY_DELETE_FAILED_NOTIFICATION = (By.XPATH,
                                                        "//div[contains(normalize-space(text()),'Failed to delete facility availability')]")
    FACILITY_AVAILABILITY_DELETE_NOTIFICATION = (By.XPATH,
                                                 "//div[contains(normalize-space(text()),'Facility availability deleted successfully')]")
    
class ScheduledAppointmentsPageLocators:
    """Locators for the Scheduled Appointments page elements."""
    # Tab navigation
    VIRTUAL_TAB = (By.XPATH, "//button[@id='scheduled_appointments_tab_virtual']")
    IN_PERSON_TAB = (By.XPATH, "//button[@id='scheduled_appointments_tab_in_person']")
    
    # Table locators
    SCHEDULED_APPOINTMENTS_TABLE = (By.XPATH, "//table[contains(@id,'table-scheduled-appointments')]")
    SCHEDULED_APPOINTMENTS_TABLE_ROWS = (By.XPATH, "//table[contains(@id,'table-scheduled-appointments')]/tbody/tr")

    PATIENT_NAME_SEARCH_INPUT = (By.XPATH, "//input[contains(@id,'patientName')]")
    APPOINTMENT_DATE_BUTTON = (By.XPATH, "//button[contains(@id,'appointment_date_picker')]")
    CLINIC_NAME_SEARCH_INPUT = (By.XPATH, "//input[contains(@id,'clinicName')]")
    USER_NAME_SEARCH_INPUT = (By.XPATH, "//input[contains(@id,'userName')]")
    FACILITY_NAME_SEARCH_INPUT = (By.XPATH, "//input[@id='userName_in-person']")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(@id,'scheduled_appointments_search')]")
    RESET_BUTTON = (By.XPATH, "//button[contains(@id,'scheduled_appointments_reset')]")

    REFRESH_BUTTON = (By.XPATH, "//button[@id='scheduled_appointments_refresh_btn']")

    
    # Patient name button (clickable to navigate to ES dashboard)
    PATIENT_NAME_BUTTON = (By.XPATH, "//table[contains(@id,'table-scheduled-appointments')]/tbody/tr[1]/td[1]//button")
    
    # Pagination
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//select[@id='pagination_records_per_page_select']")
    PAGE_INFO_TEXT = (By.XPATH, "//span[@id='pagination_page_info']")


class SearchPatientsPageLocators:
    """Locators for the Search Patients (Global Search) page elements."""

    # Search bar
    SEARCH_TYPE_DROPDOWN = (By.XPATH, "//button[@id='search_form_searchby_select']")
    SEARCH_TYPE_OPTION = lambda option_text: (By.XPATH,
                                              f"//div[@role='option']/span[normalize-space(text())='{option_text}']")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search']")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    RESET_BUTTON = (By.XPATH, "//button[@id='search_form_reload_btn']")
    MONTH_SELECT_DROPDOWN = (By.XPATH, "//button[contains(.,'Month')]/following-sibling::select[1]")
    DAY_SELECT_DROPDOWN = (By.XPATH, "//button[contains(.,'Day')]/following-sibling::select[1]")
    YEAR_SELECT_DROPDOWN = (By.XPATH, "//button[contains(.,'Year')]/following-sibling::select[1]")
    CLINIC_DROPDOWN = (By.XPATH, "//button[contains(.,'Select Clinic Name')]/following-sibling::select")

    # Results table
    PATIENTS_TABLE = (By.XPATH, "//table[@id='table-search-patients']")
    PATIENTS_TABLE_ROWS = (By.XPATH, "//table[@id='table-search-patients']/tbody/tr")

    # No results message
    NO_RESULTS_MESSAGE = (By.XPATH, "//h3[normalize-space()='No patients found']")

    # Row action button
    VIEW_DETAILS_BUTTON = (By.XPATH, "//table[@id='table-search-patients']/tbody/tr[1]//button[contains(@id, 'view')]")

    # Pagination
    PAGE_LIMIT_DROPDOWN = (By.XPATH, "//select[@id='pagination_records_per_page_select']")
    PAGINATION_NAV = (By.XPATH, "//nav[@aria-label='pagination']")

    # Patient details page - back navigation
    BACK_BUTTON = (By.XPATH, "(//button[contains(text(),'Back')])[1]")


class AddPatientPageLocators:
    """Locators for the Add Patient page elements."""

    # Step 1 - Patient Details - Clinic Selection
    SELECT_CLINIC_DROPDOWN = (By.XPATH, "//button[@id='add_patient_clinic']")
    SELECT_CLINIC_SEARCH_INPUT = (By.XPATH, "//button[@id='add_patient_clinic']/following::input[@role='combobox'][1]")
    SELECT_CLINIC_OPTION = lambda clinic_name: (By.XPATH,
                                                f"//div[@role='option' and normalize-space(text())='{clinic_name}']")
    SELECT_FACILITY_DROPDOWN = (By.XPATH, "//button[@id='add_patient_facility']")
    SELECT_FACILITY_OPTION = lambda facility_name: (By.XPATH,
                                                    f"//div[@role='option']//span[normalize-space(text())='{facility_name}']")
    SELECT_PROVIDER_DROPDOWN = (By.XPATH, "//button[@id='add_patient_provider']")
    SELECT_PROVIDER_OPTION = lambda provider_name: (By.XPATH, "//div[@role='option'][1]")

    # Step 1 - Patient Details - Personal Information
    FIRST_NAME_INPUT = (By.XPATH, "//input[@id='add_patient_first_name']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@id='add_patient_last_name']")
    ALIAS_NAME_INPUT = (By.XPATH, "//input[@id='add_patient_alias_name']")
    EMAIL_INPUT = (By.XPATH, "//input[@id='add_patient_email']")
    PHONE_NUMBER_INPUT = (By.XPATH, "//input[@id='add_patient_phone_number']")
    ALTERNATE_PHONE_INPUT = (By.XPATH, "//input[@id='add_patient_alternate_phone']")
    BIRTH_DATE_INPUT = (By.XPATH, "//input[@id='add_patient_birth_date']")
    GENDER_DROPDOWN = (By.XPATH, "//button[@id='add_patient_gender']")
    GENDER_OPTION = lambda gender: (By.XPATH, f"//div[@role='option']//span[normalize-space(text())='{gender}']")
    HEIGHT_FEET_DROPDOWN = (By.XPATH, "//button[@id='add_patient_height_feet']")
    HEIGHT_INCHES_DROPDOWN = (By.XPATH, "//button[@id='add_patient_height_inches']")
    HEIGHT_OPTION = lambda value: (By.XPATH, f"//div[@role='option']//span[normalize-space(text())='{value}']")

    # Step 1 - Patient Details - Medical Records
    EMR_ID_INPUT = (By.XPATH, "//input[@id='add_patient_emr_id']")
    PRIMARY_INSURANCE_ID_INPUT = (By.XPATH, "//input[@id='add_patient_primary_insurance_id']")
    PRIMARY_INSURANCE_PAYER_INPUT = (By.XPATH, "//input[@id='add_patient_primary_insurance_payer']")
    SECONDARY_INSURANCE_ID_INPUT = (By.XPATH, "//input[@id='add_patient_secondary_insurance_id']")
    SECONDARY_INSURANCE_PAYER_INPUT = (By.XPATH, "//input[@id='add_patient_secondary_insurance_payer']")
    INSURANCE_PLAN_INPUT = (By.XPATH, "//input[@id='add_patient_insurance_plan']")

    # Step 1 - Patient Details - Program Eligibility
    CCM_ELIGIBLE_CHECKBOX = (By.XPATH, "//button[@id='add_patient_ccm_eligible']")
    RPM_ELIGIBLE_CHECKBOX = (By.XPATH, "//button[@id='add_patient_rpm_eligible']")
    PCM_ELIGIBLE_CHECKBOX = (By.XPATH, "//button[@id='add_patient_pcm_eligible']")

    # Step 1 - Patient Details - Communication Preference
    LANGUAGE_PREFERENCE_DROPDOWN = (By.XPATH, "//button[@id='add_patient_language']")
    LANGUAGE_PREFERENCE_OPTION = lambda language: (By.XPATH,
                                                   f"//div[@role='option']//span[normalize-space(text())='{language}']")

    # Step 1 - Patient Details - Emergency Contact
    EMERGENCY_FIRST_NAME_INPUT = (By.XPATH, "//input[@id='add_patient_emergency_first_name']")
    EMERGENCY_LAST_NAME_INPUT = (By.XPATH, "//input[@id='add_patient_emergency_last_name']")
    EMERGENCY_PHONE_INPUT = (By.XPATH, "//input[@id='add_patient_emergency_phone']")

    # Step 1 - Navigation
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue']")

    # Step 2 - Address
    ADDRESS_LINE_1_INPUT = (By.XPATH, "//input[@id='add_patient_address_line1']")
    ADDRESS_LINE_2_INPUT = (By.XPATH, "//input[@id='add_patient_address_line2']")
    CITY_INPUT = (By.XPATH, "//input[@id='add_patient_city']")
    STATE_INPUT = (By.XPATH, "//input[@id='add_patient_state']")
    ZIP_CODE_INPUT = (By.XPATH, "//input[@id='add_patient_zip_code']")
    COUNTRY_DROPDOWN = (By.XPATH, "//button[@id='add_patient_country']")
    COUNTRY_DROPDOWN_OPTION = lambda country: (By.XPATH,
                                               f"//div[@role='option']//span[normalize-space(text())='{country}']")

    # Step 2 - Navigation
    PREVIOUS_BUTTON = (By.XPATH, "//button[normalize-space()='Previous']")

    # Step 3 - Summary
    SUMMARY_HEADING = (By.XPATH, "//h2[normalize-space()='Review Patient Information']")
    PERSONAL_INFO_SECTION = (By.XPATH, "//h3[contains(text(),'Personal Information')]")
    MEDICAL_RECORDS_SECTION = (By.XPATH, "//h3[contains(text(),'Medical Records')]")
    EMERGENCY_CONTACT_SECTION = (By.XPATH, "//h3[contains(text(),'Emergency Contact Information')]")
    ADDRESS_SECTION = (By.XPATH, "//h3[normalize-space()='Address']")

    # Step 3 - Navigation
    SUBMIT_BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")

    # Success notification
    PATIENT_ADDED_SUCCESS_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Patient added successfully!']")

    # Validation errors
    VALIDATION_ERROR = lambda field_name: (By.XPATH,
                                           f"//label[normalize-space()='{field_name}']/following::p[contains(@class, 'text-red-500')][1]")


class PatientDetailsPageLocators:
    """Locators for the Patient Details Page (ES Dashboard) elements."""

    # Patient information
    PATIENT_NAME_HEADING = (By.XPATH, "//h1[contains(@class, 'patient-name')]")
    PATIENT_EMR_ID = (By.XPATH, "//span[contains(text(),'EMR ID')]/following-sibling::span[1]")

    # Program status dropdown
    PROGRAM_STATUS_DROPDOWN = (By.XPATH,
                               "//label[normalize-space()='Program Status']/following-sibling::button[@role='combobox'][1]")
    PROGRAM_STATUS_OPTION = lambda status: (By.XPATH,
                                            f"//div[@role='option']//span[normalize-space(text())='{status}']")

    # Save button after changing status
    SAVE_CHANGES_BUTTON = (By.XPATH,
                           "//button[normalize-space()='Save Changes' or normalize-space()='Save' or normalize-space()='Update']")

    # Notifications
    STATUS_UPDATED_NOTIFICATION = (By.XPATH,
                                   "//div[contains(normalize-space(),'updated successfully') or contains(normalize-space(),'Status updated') or contains(normalize-space(),'Patient updated')]")

    # Navigation
    BACK_TO_DASHBOARD_BUTTON = (By.XPATH, "//button[normalize-space()='Back to Dashboard' or normalize-space()='Back']")

    #  Workflow tabs/sections
    WORKFLOW_TAB = lambda workflow_name: (By.XPATH,
                                          f"//button[@role='tab' and contains(normalize-space(), '{workflow_name}')]")
    ACTIVE_WORKFLOW_SECTION = (By.XPATH, "//div[contains(@class, 'workflow-section')]")




class UserDashboardPageLocators:
    """Locators for User Dashboard page elements."""

    HEADER_USER_MENU = (By.XPATH, "//button[@id='admin_header_user_menu_btn']")
    HAMBURGER_MENU = (By.XPATH, "//button[@id='admin_header_toggle_sidebar_btn']")
    HAMBURGER_MENU_ITEMS = (By.XPATH, "//nav[@id='admin_sidebar_nav']//a")
    HAMBURGER_MENU_OPTION = lambda option_text: (By.XPATH, f"//a/span[normalize-space(text())='{option_text}']")
    HEADER_LOGO = (By.XPATH, "//img[@id='admin_header_logo']")
    LOGOUT_BUTTON = (By.XPATH, "//button[@id='sidebar_logout_btn']")
    LOGOUT_DIALOG_CONFIRM_BUTTON = (By.XPATH, "//button[@id='logout_dialog_confirm_btn']")
    HEADER_REFRESH_BUTTON = (By.XPATH, "//button[@id='admin_header_refresh_btn']")
    OUTBOUND_CALL_BUTTON = (By.XPATH, "//button[@id='admin_header_outbound_call_btn']")

    GLOBAL_TIMER_TOGGLE_BUTTON = (By.XPATH, "//button[@id='global_timelog_toggle_btn']")
    PATIENT_TIMER_RUNNING_BUTTON = (By.XPATH, "//button[@title='Pause timer']")
    PATIENT_TIMER_PAUSED_BUTTON = (By.XPATH, "//button[@title='Resume timer']")

    PATIENT_INFORMATION_PANEL = (By.XPATH, "//span[normalize-space()='Patient Information']")
    DROP_DOWN_OPTION = lambda option_text: (By.XPATH, f"//div[@role='option']//span[normalize-space(text())='{option_text}']")
    DROP_DOWN_OPTION_SEARCH = (By.XPATH, "//input[@role='combobox'][1]")

    FIRST_NAME_INPUT = (By.XPATH, "(//label[normalize-space(text())='First Name']/following::input)[1]")
    LAST_NAME_INPUT = (By.XPATH, "(//label[normalize-space(text())='Last Name']/following::input)[1]")
    DATE_OF_BIRTH_INPUT = (By.XPATH, "//label[text()='Date of Birth']/following-sibling::button")
    GENDER_DROPDOWN = (By.XPATH, "//label[text()='Gender']/following-sibling::button")
    MOBILE_NUMBER_INPUT = (By.XPATH, "(//label[normalize-space(text())='Mobile Number']/following::input)[1]")
    CALL_BUTTON = (By.XPATH, "(//label[normalize-space(text())='Mobile Number']/following::input)[1]/following-sibling::button[1]")
    COPY_BUTTON = (By.XPATH, "(//label[normalize-space(text())='Mobile Number']/following::input)[1]/following-sibling::button[2]")
    MESSAGE_BUTTON = (By.XPATH, "(//label[normalize-space(text())='Mobile Number']/following::input)[1]/following-sibling::span[1]")
    HOME_PHONE_NUMBER_INPUT = (By.XPATH, "(//label[normalize-space(text())='Home Phone Number']/following::input)[1]")
    EMAIL_INPUT = (By.XPATH, "(//label[normalize-space(text())='Email Address']/following::input)[1]")
    ADDRESS_INPUT = (By.XPATH, "(//label[normalize-space(text())='Address']/following::input)[1]")
    CITY_INPUT = (By.XPATH, "(//label[normalize-space(text())='City']/following::input)[1]")
    STATE_INPUT = (By.XPATH, "(//label[normalize-space(text())='State']/following::input)[1]")
    ZIP_CODE_INPUT = (By.XPATH, "(//label[normalize-space(text())='Zip Code']/following::input)[1]")
    CLINIC_NAME_INPUT = (By.XPATH, "(//label[normalize-space(text())='Clinic Name']/following::input)[1]")
    PROVIDER_NAME_INPUT = (By.XPATH, "(//label[normalize-space(text())='Provider Name']/following::input)[1]")
    EMR_ID_INPUT = (By.XPATH, "(//label[normalize-space(text())='EMR ID']/following::input)[1]")
    PRIMARY_DX_BUTTON = (By.XPATH, "(//label[normalize-space(text())='Primary Dx']/following::button)[1]")
    SECONDARY_DX_BUTTON = (By.XPATH, "(//label[normalize-space(text())='Secondary Dx']/following::button)[1]")
    PRIMARY_INSURANCE_PROVIDER_BUTTON = (By.XPATH, "//label[text()='Primary Insurance Provider']/following-sibling::button")
    PRIMARY_INSURANCE_NO_INPUT = (By.XPATH, "//label[text()='Primary Insurance Number']/following-sibling::input")
    SECONDARY_INSURANCE_PROVIDER_BUTTON = (By.XPATH, "//label[text()='Secondary Insurance Provider']/following-sibling::button")
    SECONDARY_INSURANCE_NO_INPUT = (By.XPATH, "//label[text()='Secondary Insurance Number']/following-sibling::input")
    SAVE_DEMOGRAPHIC_BUTTON = (By.XPATH, "//button[normalize-space()='Save Demographic Changes']")
    ENROLLMENT_STATUS_DROPDOWN = (By.XPATH, "(//label[contains(.,'Select Enrollment Status *')]/following::button)[1]")
    ENROLLMENT_STATUS_SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search statuses...']")
    ENROLLMENT_STATUS_OPTION = lambda status: (By.XPATH,f"//span[normalize-space(text())='{status}']")
    WORKFLOW_STATUS_DROPDOWN = (By.XPATH, "(//label[contains(.,'Select Workflow Status *')]/following::button)[1]")
    APPOINTMENT_TYPE_DROPDOWN = (By.XPATH, "(//label[normalize-space(text())='Appointment Type']/following::button)[1]")
    APPOINTMENT_OPTION = lambda option: (By.XPATH, f"//span[normalize-space(text())='{option}']")
    SELECT_RESOURCE_DROPDOWN = (By.XPATH, "(//label[normalize-space(text())='Select Resource']/following::button)[1]")
    SELECT_FACILITY_DROPDOWN = (By.XPATH, "(//label[normalize-space(text())='Select Facility']/following::button)[1]")
    APPOINTMENT_DATE_BUTTON = (By.XPATH, "(//label[normalize-space(text())='Appointment Date']/following::button)[1]")
    APPOINTMENT_TIME_BUTTON = (By.XPATH, "(//label[normalize-space(text())='Appointment Time']/following::button)[1]")
    APPOINTMENT_NEXT_MONTH_BUTTON = (By.XPATH, "//button[.//*[contains(@class,'lucide-chevron-right')]]")
    AVAILABLE_SLOTS_TEXT = (By.XPATH, "//label[normalize-space(text())='Appointment Time']/following::ul/li")
    START_HH_INPUT = (By.XPATH, "(//label[normalize-space(text())='Start Time']/following::button)[1]")
    START_MM_INPUT = (By.XPATH, "(//label[normalize-space(text())='Start Time']/following::button)[2]")
    START_PERIOD_INPUT = (By.XPATH, "(//label[normalize-space(text())='Start Time']/following::button)[3]")
    END_HH_INPUT = (By.XPATH, "(//label[normalize-space(text())='End Time']/following::button)[1]")
    END_MM_INPUT = (By.XPATH, "(//label[normalize-space(text())='End Time']/following::button)[2]")
    END_PERIOD_INPUT = (By.XPATH, "(//label[normalize-space(text())='End Time']/following::button)[3]")
    APPLY_SLOT_BUTTON = (By.XPATH, "//button[text()='Reset']/following-sibling::button")
    COMMENT_TEXTAREA = (By.XPATH, "//textarea[@id='es-patient-comments']")
    SAVE_BUTTON = (By.XPATH, "//button[@id='es-save-patient']")
    NEXT_PATIENT_BUTTON = (By.XPATH, "//button[contains(@id,'es-next-patient')]")
    NEXT_PATIENT_BUTTON_DISABLED = (By.XPATH, "//button[@id='es-save-patient']")
    NEXT_AVAILABLE_DAY = lambda days_after: (By.XPATH, f"//button[@name='day' and not(@disabled)][{days_after}]")
    PATIENT_ENROLLMENT_SAVED_NOTIFICATION = (By.XPATH, "//div[normalize-space()='Patient enrollment saved successfully']")
    GROUP_COMPLETION_DIALOG = (By.XPATH, "//div[@id='group-completion-dialog']")
    GROUP_COMPLETION_DIALOG_CLOSE_BUTTON = (By.XPATH, "//button[text()='Ok']")
