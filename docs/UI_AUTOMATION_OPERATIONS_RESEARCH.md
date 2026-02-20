# UI Automation Framework Operations Research

## Research Completed: February 18, 2026

---

## 1. USER CREATION WITH SPECIFIC ROLE & CREDENTIALS

### EXISTING METHOD: `fill_create_user_form()`

**Location:** [features/pages/users_page/users_page.py](features/pages/users_page/users_page.py#L167-L195)

**Method Signature:**
```python
def fill_create_user_form(self):
    """Fill the create user form with valid generated data."""
```

**Current Behavior:**
- Generates **random** credentials using Faker library
- **Fixed user type: "ES"** (Enrollment Specialist)
- **Fixed password: "Password123"**
- Email format: `{first_name}.{last_name}@hbox.ai` (auto-generated)
- Phone: 10 random digits

**Returns:**
```python
{
    "first_name": str,
    "last_name": str,
    "email": str,
    "phone": str,
    "password": str,
    "user_type": str  # Always "ES"
}
```

### LOCATORS AVAILABLE:
- `USER_TYPE_COMBOBOX` - [locators.py](features/commons/locators.py#L68-L69)
- `FIRST_NAME_INPUT` - [locators.py](features/commons/locators.py#L63)
- `LAST_NAME_INPUT` - [locators.py](features/commons/locators.py#L64)
- `EMAIL_INPUT` - [locators.py](features/commons/locators.py#L65)
- `PASSWORD_INPUT` - [locators.py](features/commons/locators.py#L67)
- `PHONE_INPUT` - [locators.py](features/commons/locators.py#L66)

### HELPER METHOD: `select_user_type()`

**Location:** [features/pages/users_page/users_page.py](features/pages/users_page/users_page.py#L197-L203)

```python
def select_user_type(self, user_type):
    """Select user type from combobox."""
    # Uses custom_select_by_locator to select ES, CS, or PE
```

### ⚠️ MISSING FUNCTIONALITY:

**Need to create NEW method:** `fill_create_user_form_with_specific_data()`

```python
def fill_create_user_form_with_specific_data(self, first_name, last_name, email, password, user_type, phone=None):
    """
    Fill the create user form with specific credentials.
    
    Args:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): Exact email address to use
        password (str): Exact password to use
        user_type (str): "ES", "CS", or "PE"
        phone (str, optional): Phone number (generates random if not provided)
    
    Returns:
        dict: User credentials used for creation
    """
```

**Implementation Strategy:**
1. Copy logic from `fill_create_user_form()` lines 167-195
2. Replace Faker-generated values with parameter values
3. Keep date/time selection logic identical
4. Call existing `select_user_type(user_type)` method
5. Return dict with provided credentials

---

## 2. ASSIGNING USERS TO GROUPS

### EXISTING METHOD: `add_users_by_type()`

**Location:** [features/pages/users_page/user_group_page.py](features/pages/users_page/user_group_page.py#L86-L107)

**Method Signature:**
```python
def add_users_by_type(self, count=1, user_type="ES"):
    """Add users to the group by type."""
```

**Current Behavior:**
- Filters users by **type only** (ES, CS, PE)
- Selects **first N users** matching the type
- Cannot target specific users by email/name

**How it works:**
1. Opens user selection dropdown
2. Filters by "User Type" field
3. Enters user_type in search (e.g., "ES")
4. Clicks first `count` checkboxes that appear
5. Clicks "Add" button

### LOCATORS AVAILABLE:
- `ADD_USERS_BUTTON` - Opens user selection modal
- `ADD_USERS_FILTER_DROPDOWN` - Filter type selector
- `ADD_USERS_SEARCH_INPUT` - Search/filter input
- `ADD_USER_SELECTION_CHECKBOX` - User checkboxes
- `ADD_USERS_ADD_BUTTON` - Confirm selection

### ⚠️ MISSING FUNCTIONALITY:

**Need to create NEW method:** `add_specific_users_by_email()`

```python
def add_specific_users_by_email(self, email_list):
    """
    Add specific users to the group by their email addresses.
    
    Args:
        email_list (list): List of email addresses to add
        
    Returns:
        int: Number of users successfully added
        
    Example:
        add_specific_users_by_email([
            "john.doe@hbox.ai",
            "jane.smith@hbox.ai"
        ])
    """
```

**Implementation Strategy:**
1. Click `ADD_USERS_BUTTON`
2. For each email in email_list:
   - Select filter type "Email" from `ADD_USERS_FILTER_DROPDOWN`
   - Enter email in `ADD_USERS_SEARCH_INPUT`
   - Find and click checkbox for matching user
3. Click `ADD_USERS_ADD_BUTTON` at the end

**Alternative Method:** `add_users_by_name()`
```python
def add_users_by_name(self, name_list):
    """Add users by their full names or partial names."""
```

---

## 3. WORKFLOW CREATION WITH TRIGGERS

### EXISTING METHOD: `fill_create_workflow_form()`

**Location:** [features/pages/workflow_tasks_page/workflow_page.py](features/pages/workflow_tasks_page/workflow_page.py#L137-L161)

**Method Signature:**
```python
def fill_create_workflow_form(self):
    """Fill workflow form with default selections."""
```

**Current Behavior:**
- Selects **FIRST option** from all dropdowns
- Always creates workflows **WITH triggers**
- Cannot specify "no trigger" scenario
- Cannot select specific program (like "CCM")

**Uses Helper Method:** `_select_first_dropdown_option()`

**Location:** [workflow_page.py](features/pages/workflow_tasks_page/workflow_page.py#L125-L138)

```python
def _select_first_dropdown_option(self, dropdown_locator):
    """Clicks dropdown, selects first option, returns option text."""
```

### WORKFLOW LOCATORS:

**Location:** [features/commons/locators.py](features/commons/locators.py#L412-L418)

```python
APPLICABLE_PROGRAMS_DROPDOWN = (By.XPATH, "...")  # Line 412
TRIGGER_WORKFLOW_DROPDOWN = (By.XPATH, "...")     # Line 416
TRIGGER_STATUS_DROPDOWN = (By.XPATH, "...")       # Line 418
TRIGGER_ROW_DELETE_BUTTON = (By.XPATH, "...")     # Delete trigger row
```

### EXISTING METHOD: `remove_trigger_row()`

**Location:** [workflow_page.py](features/pages/workflow_tasks_page/workflow_page.py#L219-L228)

```python
def remove_trigger_row(self):
    """Delete trigger row to create workflow without trigger."""
```

### ⚠️ MISSING FUNCTIONALITY:

**Need to create NEW method:** `fill_create_workflow_form_with_options()`

```python
def fill_create_workflow_form_with_options(
    self,
    workflow_name=None,
    program_name=None,
    trigger_workflow=None,
    trigger_status=None,
    task_name="Call",
    waiting_period=1,
    user_group=None,
    no_trigger=False
):
    """
    Fill workflow creation form with specific options.
    
    Args:
        workflow_name (str, optional): Specific workflow name, generates if None
        program_name (str, optional): Program to select (e.g., "CCM"), first if None
        trigger_workflow (str, optional): Trigger workflow name, first if None
        trigger_status (str, optional): Trigger status name, first if None
        task_name (str): Task type (default "Call")
        waiting_period (int): Days to wait between attempts
        user_group (str, optional): User group name, first if None
        no_trigger (bool): If True, removes trigger row
        
    Returns:
        dict: Workflow configuration details
    """
```

**Implementation Strategy:**
1. Generate or use provided `workflow_name`
2. **Select specific program:**
   ```python
   if program_name:
       self.custom_select_by_locator(
           WorkflowPageLocators.APPLICABLE_PROGRAMS_DROPDOWN,
           WorkflowPageLocators.DROPDOWN_OPTION(program_name)
       )
   else:
       self._select_first_dropdown_option(APPLICABLE_PROGRAMS_DROPDOWN)
   ```
3. **Handle no_trigger scenario:**
   ```python
   if no_trigger:
       self.remove_trigger_row()
   else:
       # Select trigger workflow and status
   ```
4. Continue with task/attempt/user group selection
5. Return full configuration dict

**Helper Method Needed:** `select_dropdown_by_text()`

```python
def select_dropdown_by_text(self, dropdown_locator, option_text):
    """Select dropdown option by exact text match."""
    self.click(dropdown_locator)
    option = self.find_element((By.XPATH, 
        f"//div[@role='option']//span[normalize-space()='{option_text}']"))
    option.click()
    return option_text
```

---

## 4. ACTIVITY CREATION

### ⚠️ CRITICAL FINDING: NO ACTIVITY CREATION METHODS EXIST

**Activities Page Location:** [features/pages/activities_page/activities_page.py](features/pages/activities_page/activities_page.py)

**Current Implementation:**
- Only has listing/search/navigation methods
- **No form-filling methods**
- **No create activity logic**

**Available Methods:**
- ✅ `navigate_to_listing()` - Navigate to activities list
- ✅ `get_activities_first_row_data()` - Extract row data
- ✅ `perform_activities_search_by_field()` - Search activities
- ✅ `click_on_activities_action_button()` - Click edit/delete/duplicate
- ✅ `is_navigated_to_activity_edit_page()` - Verify navigation
- ❌ **No create/fill methods**

### ACTIVITY LOCATORS AVAILABLE:

**Location:** [features/commons/locators.py](features/commons/locators.py#L450-L500)

```python
# Activity form fields
ACTIVITY_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter activity name']")
PATIENT_GROUP_DROPDOWN = (By.XPATH, "...")
PATIENT_GROUP_OPTION = lambda text: (By.XPATH, "...")
WORKFLOW_DROPDOWN = (By.XPATH, "...")
WORKFLOW_OPTION = lambda text: (By.XPATH, "...")
FROM_DATE_BUTTON = (By.XPATH, "...")
END_DATE_BUTTON = (By.XPATH, "...")
TIMEZONE_DROPDOWN = (By.XPATH, "...")
ACTIVE_DAY_CHECKBOX = lambda day: (By.XPATH, "...")
ADD_ANOTHER_SLOT_BUTTON = (By.XPATH, "...")
SAVE_ACTIVITY_BUTTON = (By.XPATH, "//button[normalize-space()='Save Activity']")
CANCEL_ACTIVITY_BUTTON = (By.XPATH, "...")
```

### 🔧 NEED TO CREATE: Complete Activity Creation Methods

**Method 1:** `click_add_new_activity()`

```python
def click_add_new_activity(self):
    """Click Add New Activity button and wait for form to load."""
    self.click(ActivitiesPageLocators.ADD_NEW_ACTIVITY_BUTTON)
    self.wait_for_dom_stability()
    return True
```

**Method 2:** `fill_create_activity_form()`

```python
def fill_create_activity_form(
    self,
    activity_name=None,
    patient_group_name=None,
    workflow_name=None,
    from_date=None,
    end_date=None,
    active_days=None,
    timezone=None
):
    """
    Fill the create activity form.
    
    Args:
        activity_name (str, optional): Activity name, generates if None
        patient_group_name (str): Required - Patient group to assign
        workflow_name (str): Required - Workflow to associate
        from_date (str, optional): Start date (DD-MM-YYYY), defaults to today
        end_date (str, optional): End date (DD-MM-YYYY), defaults to +30 days
        active_days (list, optional): Days to activate (e.g., ["Monday", "Tuesday"])
        timezone (str, optional): Timezone, uses first if None
        
    Returns:
        dict: Activity configuration
        
    Example:
        fill_create_activity_form(
            activity_name="CCM Outreach Q1",
            patient_group_name="CCM Patients - 50",
            workflow_name="CCM Call Workflow",
            active_days=["Monday", "Wednesday", "Friday"]
        )
    """
```

**Implementation Steps:**
1. Generate or use provided activity name
2. Enter in `ACTIVITY_NAME_INPUT`
3. Select patient group from dropdown
4. Select workflow from dropdown
5. Select dates using date picker logic (similar to user creation)
6. Check active day checkboxes
7. Select timezone if provided
8. Return configuration dict

**Method 3:** `submit_create_activity()`

```python
def submit_create_activity(self):
    """Click Save Activity button."""
    self.click(ActivitiesPageLocators.SAVE_ACTIVITY_BUTTON)
    return True
```

**Method 4:** `check_activity_notification()`

```python
def check_activity_notification(self, expected_message):
    """Verify activity creation/update/delete notification."""
    # Need to add notification locators to ActivitiesPageLocators
```

---

## 5. PATIENT GROUP CREATION

### EXISTING METHODS: Multiple Creation Paths

#### Method A: Create by EMRs

**Location:** [features/pages/patient_groups_page/patient_groups_page.py](features/pages/patient_groups_page/patient_groups_page.py#L291-L322)

**Method Signature:**
```python
def create_patient_group_by_emrs(self, clinic, emr_ids):
    """
    Create patient group by EMR IDs.
    
    Args:
        clinic (str): Clinic name to select
        emr_ids (list): List of EMR ID strings
        
    Example:
        create_patient_group_by_emrs(
            clinic="Main Clinic",
            emr_ids=["12345", "67890", "11223"]
        )
    """
```

**How it works:**
1. Select clinic from dropdown
2. Enter comma-separated EMR IDs in textbox
3. Click "Apply" button
4. Wait for search completion notification

#### Method B: Create by Filters

**Location:** [patient_groups_page.py](features/pages/patient_groups_page/patient_groups_page.py#L233-L268)

**Available Helper Methods:**
- ✅ `extract_filtered_count()` - Get count of filtered patients
- ✅ `extract_filtered_emr_ids()` - Get list of EMR IDs from results

**Workflow:**
1. Navigate to "Create New Group By Filters"
2. Apply clinic/provider filters
3. See filtered patient count
4. Create group naming it

#### Method C: Create by Excel Upload

**Location:** [patient_groups_page.py](features/pages/patient_groups_page/patient_groups_page.py#L528-L543)

```python
def create_patient_group_by_excel_upload(self):
    """Create patient group by uploading Excel file with patient IDs."""
```

### ✅ ANSWER: To Create Group with 50 Patients

**Use Method A (By EMRs) or Method B (By Filters)**

**Strategy 1: Using EMR IDs (Most Direct)**

```python
# Step 1: Search and collect 50 patient EMR IDs
search_page = SearchPatientsPage(driver)
search_page.navigate_to_search_patients()  # Shows all patients

# Step 2: Extract EMR IDs from search results
# Need to create helper method to get N patient IDs

# Step 3: Create group with those EMR IDs
patient_groups = PatientGroupsPage(driver)
patient_groups.click_create_new_group()
patient_groups.select_create_option("create new group by emrs")
patient_groups.create_patient_group_by_emrs(
    clinic="Main Clinic",
    emr_ids=fifty_patient_ids
)
patient_groups.enter_group_name_and_note()
```

**Strategy 2: Using Filters**

```python
# Apply filters to get exactly 50 patients
# Then create group from filtered results
patient_groups.select_create_option("create new group by filters")
# Apply clinic/provider filters until filtered_count == 50
patient_groups.enter_group_name_and_note()
```

### 🔧 HELPER METHOD NEEDED:

```python
def collect_patient_emr_ids(self, count=50):
    """
    Collect EMR IDs from search results.
    
    Args:
        count (int): Number of EMR IDs to collect
        
    Returns:
        list: List of EMR ID strings
    """
    # Navigate through pagination if needed
    # Extract EMR IDs from table rows
    # Return list of count EMR IDs
```

---

## 6. DASHBOARD & PATIENT DETAILS

### EXISTING METHODS: Dashboard Navigation

**Location:** [features/pages/dashboard_page/dashboard_page.py](features/pages/dashboard_page/dashboard_page.py)

#### Open Patient Details Page

**Method:** `click_dynamic_hamburger_menu_option()`

**Location:** [dashboard_page.py](features/pages/dashboard_page/dashboard_page.py#L28-L37)

```python
def click_dynamic_hamburger_menu_option(self, option_name):
    """
    Click on a dynamic option in the hamburger menu.
    
    Args:
        option_name (str): Menu option text (e.g., "Search Patients")
    """
```

**Usage to navigate to patient search:**
```python
dashboard = DashboardPage(driver)
dashboard.click_dynamic_hamburger_menu_option("Search Patients")
```

### SEARCH PATIENTS PAGE: View Details

**Location:** [features/pages/search_patients_page/search_patients_page.py](features/pages/search_patients_page/search_patients_page.py#L155-L162)

```python
def click_view_details_for_first_patient(self):
    """Click View Details button on first patient row."""
    self.is_element_visible(SearchPatientsPageLocators.VIEW_DETAILS_BUTTON, timeout=15)
    self.click(SearchPatientsPageLocators.VIEW_DETAILS_BUTTON)

def is_patient_details_page_loaded(self) -> bool:
    """Verify patient details page is loaded."""
    return self.check_url_contains(Routes.PATIENT_DETAILS, partial=False)
```

### ⚠️ MISSING: Patient Details Page Object

**No page object exists for Patient Details page**

**Need to create:** `features/pages/patient_details_page/patient_details_page.py`

```python
class PatientDetailsPage(BasePage):
    """Page object for Patient Details page."""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def get_patient_program_status(self):
        """Get current program status displayed."""
        
    def change_program_status(self, new_status):
        """
        Change patient's program status.
        
        Args:
            new_status (str): New status name to select
        """
        # Need to identify locators for:
        # - Program status dropdown
        # - Status options
        # - Save/Update button
        
    def is_navigated_to_patient_details(self):
        """Verify on patient details page."""
        return self.check_url_contains(Routes.PATIENT_DETAILS, partial=False)
    
    def get_patient_info(self):
        """Extract patient information from details page."""
        # First, last name, DOB, EMR ID, etc.
```

### 🔧 NEED TO CREATE: Patient Details Locators

**Add to:** `features/commons/locators.py`

```python
class PatientDetailsPageLocators:
    """Locators for Patient Details page."""
    
    # Patient info display
    PATIENT_NAME_HEADER = (By.XPATH, "...")
    PATIENT_EMR_ID = (By.XPATH, "...")
    PATIENT_DOB = (By.XPATH, "...")
    
    # Program status section
    PROGRAM_STATUS_DROPDOWN = (By.XPATH, "...")
    PROGRAM_STATUS_OPTION = lambda status: (By.XPATH, f"...")
    SAVE_STATUS_BUTTON = (By.XPATH, "...")
    
    # Navigation
    BACK_BUTTON = (By.XPATH, "...")
    
    # Notifications
    STATUS_UPDATED_SUCCESS = (By.XPATH, "...")
```

### Complete Flow Example:

```python
# Navigate from dashboard to patient details
dashboard = DashboardPage(driver)
dashboard.click_dynamic_hamburger_menu_option("Search Patients")

# Search for patient
search_page = SearchPatientsPage(driver)
search_page.perform_search_by_field("First Name", "John")
search_page.click_view_details_for_first_patient()

# Change program status (NEW functionality)
patient_details = PatientDetailsPage(driver)  # Need to create
patient_details.change_program_status("Active in Program")
```

---

## 7. SUMMARY OF REQUIRED NEW METHODS

### High Priority - Must Create:

#### UsersPage (`features/pages/users_page/users_page.py`)
1. ✅ **`fill_create_user_form_with_specific_data()`** - Create user with specific email/password/role

#### UserGroupPage (`features/pages/users_page/user_group_page.py`)
2. ✅ **`add_specific_users_by_email()`** - Assign specific users by email to group

#### WorkflowPage (`features/pages/workflow_tasks_page/workflow_page.py`)
3. ✅ **`fill_create_workflow_form_with_options()`** - Create workflow with specific options
4. ✅ **`select_dropdown_by_text()`** - Helper to select dropdown option by text

#### ActivitiesPage (`features/pages/activities_page/activities_page.py`)
5. ✅ **`click_add_new_activity()`** - Navigate to activity creation form
6. ✅ **`fill_create_activity_form()`** - Fill activity creation form
7. ✅ **`submit_create_activity()`** - Submit activity form
8. ✅ **`check_activity_notification()`** - Verify success notification

#### PatientGroupsPage (`features/pages/patient_groups_page/patient_groups_page.py`)
9. ✅ **`collect_patient_emr_ids()`** - Collect N patient EMR IDs from search

#### BRAND NEW: PatientDetailsPage
10. ✅ **Create entire page object** - `features/pages/patient_details_page/patient_details_page.py`
11. ✅ **Create locators** - Add `PatientDetailsPageLocators` to `locators.py`
12. ✅ **`change_program_status()`** - Change patient's program status
13. ✅ **`get_patient_info()`** - Extract patient details

---

## 8. KEY TECHNICAL NOTES

### Dropdown Selection Pattern

The framework uses **custom dropdowns** (not standard HTML `<select>`):

```python
# Standard pattern used throughout
self.custom_select_by_locator(
    base_dropdown_locator,
    option_locator
)

# Example: Select user type
self.custom_select_by_locator(
    UsersPageLocators.USER_TYPE_COMBOBOX,
    UsersPageLocators.SEARCH_TYPE_OPTION("ES")
)
```

**Helper in BasePage:** [base_page.py](features/pages/base_page.py#L861-L869)

```python
def custom_select_by_locator(self, base_locator, option_locator):
    """Custom dropdown selection for non-standard select elements."""
    dropdown = self.find_element(base_locator)
    dropdown.click()
    time.sleep(0.5)  # wait for options to render
    option = self.find_element(option_locator)
    option.click()
    return True
```

### XPath-Only Locator Strategy

All locators **MUST use XPath** (project constraint):

```python
# Correct
BUTTON = (By.XPATH, "//button[normalize-space()='Submit']")

# FORBIDDEN
BUTTON = (By.ID, "submit-btn")
BUTTON = (By.CSS_SELECTOR, ".submit-button")
```

### Page Object Model (POM) Compliance

- Step definitions should **ONLY call page object methods**
- No direct Selenium calls in step files
- All locators stored in `features/commons/locators.py`
- All page logic in `features/pages/*/`

---

## 9. RECOMMENDED IMPLEMENTATION ORDER

1. **User Creation with Specific Credentials** (Easiest - modify existing)
2. **Workflow with Specific Program/Triggers** (Medium - extend existing)
3. **Assign Specific Users to Groups** (Medium - new logic needed)
4. **Activity Creation** (Complex - build from scratch)
5. **Patient Details & Status Change** (Complex - new page object)

---

## 10. NEXT STEPS

### Immediate Actions:
1. Create missing methods in existing page objects
2. Build PatientDetailsPage page object from scratch
3. Add missing locators to locators.py
4. Write step definitions using new methods
5. Create Gherkin feature files for new scenarios

### Testing Requirements:
- Verify each new method independently
- Test error handling (user not found, etc.)
- Validate dropdown selections work correctly
- Confirm notifications appear after operations

---

**Research completed by:** GitHub Copilot  
**Framework Version:** automation-hbox-ng-pepv2  
**Documentation Date:** February 18, 2026
