@login_enroller_admin
Feature: tc05 - Enroller Admin Manage Users

  @regression @smoke @allure.label.severity:critical
  Scenario: Master User CRUD Operations
    Given I am on the Users page
    When I click "Add New User" button
    And I fill the create user form with valid data
    And I click "Save" button on the modal
    Then notification "User Created" appears

    When I find the created user in the list
    And I click edit for the created user
    And I update the user last name to "Edited"
    And I click "Save" button on the modal
    Then notification "User Updated" appears

    When I find the edited user in the list
    And I click delete for the edited user
    And I confirm the user delete in the dialog
    Then notification "User Deleted" appears

  @regression @allure.label.severity:critical
  Scenario: Validation - missing required fields
    Given I am on the Users page
    When I click "Add New User" button
    And I click "Save" button without filling user required fields
    Then validation error messages appear for required fields

  @regression @allure.label.severity:critical
  Scenario: Cancel create operation
    Given I am on the Users page
    When I click "Add New User" button
    And I fill the create user form with valid data
    And I click "Cancel" button on the modal
    Then modal closes without creating user

  @regression @allure.label.severity:critical
  Scenario: Master Cleanup - Delete all remaining test data
    Given I am on the Users page
    When I delete all users containing "Automation" in their email
    Then all test automation users should be deleted