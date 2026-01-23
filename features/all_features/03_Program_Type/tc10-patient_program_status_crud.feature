@login_enroller_admin
Feature: tc10 - Patient Program Status CRUD operations
  As an Enroller Admin
  I want to manage patient program statuses
  So that I can ensure proper patient program status administration

  @regression @smoke @allure.label.severity:critical
  Scenario: Master Patient Program Status CRUD Operations
    Given I am on the Program Type page
    And I am on the Patient Program Status tab from program type
    When I click "Add New Patient Program Status" button
    And I fill the create patient program status form with valid data
    And I click "Save Status" button on the patient program status form
    Then notification "Program status created successfully" appears

    When I find the created patient program status in the list and click edit
    And I update the patient program status name to "Edited"
    And I click "Update Status" button on the patient program status form
    Then notification "Program status updated successfully" appears

    When I find the edited patient program status in the list and click delete
    And I confirm the patient program status delete in the dialog
    Then notification "Program status deleted successfully" appears

  @regression @allure.label.severity:critical
  Scenario: Cancel create operation
    Given I am on the Program Type page
    And I am on the Patient Program Status tab from program type
    When I click "Add New Patient Program Status" button
    And I fill the create patient program status form with valid data
    And I click "Cancel" button on the patient program status form
    Then modal closes without creating patient program status

  @regression @allure.label.severity:critical @only
  Scenario: Master Cleanup - Delete all remaining test data
    Given I am on the Program Type page
    And I am on the Patient Program Status tab from program type
    When I delete all patient program statuses containing "Automation" in their name
    Then all test automation patient program statuses should be deleted