# Enroller Admin Dashboard Test Case

## Objective
Validate the core UI elements, navigation, and functional flows of the Enroller Admin Dashboard for the user `enroller.admin@hbox.ai` on https://ngpepv2-sandbox.hbox.ai.

## Preconditions
- User is logged in as Enroller Admin (`enroller.admin@hbox.ai`, password from config).
- Browser: Chrome (per config).

## Test Steps
1. **Login**
    - Navigate to the login page.
    - Enter valid credentials.
    - Verify successful login and redirection to `/admin/dashboard`.
2. **Dashboard UI Verification**
    - Verify presence of HBox logo and banner.
    - Verify user role indicator: `EA Enroller Admin ED`.
    - Verify sidebar navigation contains:
        - Dashboard
        - Users
        - Program Type
        - Patient Groups
        - Workflow
        - Activities
        - Facility Availability
        - Scheduled Appointments
        - SMS
        - Call History
        - Patients
    - Verify Logout button is present.
3. **Navigation Checks**
    - Click each sidebar link and verify correct page loads (URL and page title).
    - Return to Dashboard and verify main content loads.
4. **Functional Checks**
    - Click 'Page Refresh' and verify dashboard reloads.
    - Validate notifications region is visible.
5. **Edge Cases**
    - Attempt to access dashboard after logout (should redirect to login).
    - Attempt to access dashboard with invalid session (should redirect to login).

## Validation Points
- All sidebar links are functional and visible.
- User role and banner are correct.
- Main dashboard content loads without errors.
- Logout and session handling work as expected.

## Data Dependencies
- Valid enroller admin credentials from `configuration/config.ini`.

## Automation Coverage Notes
- All locators for automation must use XPath only.
- Page Object Model to be followed for step definitions and page actions.
- Retry logic for flaky elements (e.g., notifications region).

## References
- [docs/enroller_admin_dashboard_snapshot.md](docs/enroller_admin_dashboard_snapshot.md)
