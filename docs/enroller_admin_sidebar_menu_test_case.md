# Enroller Admin Sidebar Menu Test Case

## Objective
Validate the visibility, navigation, and functional correctness of all sidebar menu options for Enroller Admin on https://ngpepv2-sandbox.hbox.ai.

## Preconditions
- User is logged in as Enroller Admin (`enroller.admin@hbox.ai`, password from config).
- Browser: Chrome (per config).

## Sidebar Menu Options
1. Dashboard
2. Users
3. Program Type
4. Patient Groups
5. Workflow
6. Activities
7. Facility Availability
8. Scheduled Appointments
9. SMS
10. Call History
11. Patients

## Test Steps
1. **Verify Sidebar Visibility**
    - Ensure sidebar is visible after login.
    - Confirm all menu options above are present and visible.
2. **Navigation and Page Load**
    - For each menu option:
        - Click the menu link.
        - Verify the URL matches expected route (e.g., `/admin/users` for Users).
        - Verify the page title and main content loads correctly.
        - Return to Dashboard after each check.
3. **Edge Cases**
    - Attempt to access each menu route directly via URL (should load if authorized).
    - Attempt to access menu routes after logout (should redirect to login).

## Validation Points
- All sidebar menu options are present and functional.
- Navigation to each route loads correct content and title.
- Unauthorized access is blocked after logout.

## Data Dependencies
- Valid enroller admin credentials from `configuration/config.ini`.

## Automation Coverage Notes
- All locators for automation must use XPath only.
- Page Object Model to be followed for step definitions and page actions.
- Retry logic for flaky elements (e.g., sidebar rendering).

## References
- [docs/enroller_admin_dashboard_snapshot.md](docs/enroller_admin_dashboard_snapshot.md)
