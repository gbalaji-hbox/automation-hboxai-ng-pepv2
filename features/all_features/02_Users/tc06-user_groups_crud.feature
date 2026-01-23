@login_enroller_admin
Feature: tc06 - Enroller Admin Manage User Groups

  @regression @smoke @allure.label.severity:critical
  Scenario: Master User Group CRUD Operations
    Given I am on the Users page
    And I am on the User Group tab from Users
    When I click "Add New User Group" button
    And I fill the create user group form with valid data
    And I click "Save" button on the modal
    Then notification "User Group Created" appears

    When I find the created user group in the list and click edit
    And I update the user group name to "Edited"
    And I click "Save" button on the modal
    Then notification "User group updated successfully" appears

    When I find the edited user group in the list and click delete
    And I confirm the user group delete in the dialog
    Then notification "User group deleted successfully" appears

  @regression @allure.label.severity:critical
  Scenario: Cancel create operation
    Given I am on the Users page
    And I am on the User Group tab from Users
    When I click "Add New User Group" button
    And I fill the create user group form with valid data
    And I click "Cancel" button on the modal
    Then modal closes without creating user group

  @regression @allure.label.severity:critical
  Scenario: Master Cleanup - Delete all remaining test data
    Given I am on the Users page
    And I am on the User Group tab from Users
    When I delete all user groups containing "automation" in their name
    Then all test automation user groups should be deleted