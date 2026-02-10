@login_enroller_admin
Feature: tc09 - Program Types CRUD operations
  As an Enroller Admin
  I want to manage program types
  So that I can ensure proper program type administration

  @regression @smoke @allure.label.severity:critical
  Scenario: Master Program Type CRUD Operations
    Given I am on the Program Type page
    And I am on the Program tab from program type
    When I click "Add New Program" button
    And I fill the create program form with valid data
    And I click "Save" button on the program form
    Then notification "Program type created successfully" appears

    When I find the created program in the list and click edit
    And I update the program name to "Edited"
    And I click "Save" button on the program form
    Then notification "Program type updated successfully" appears

    When I find the edited program in the list and click delete
    And I confirm the program delete in the dialog
    Then notification "Program type deleted successfully" appears

  @regression @allure.label.severity:critical
  Scenario: Cancel create operation
    Given I am on the Program Type page
    And I am on the Program tab from program type
    When I click "Add New Program" button
    And I fill the create program form with valid data
    And I click "Cancel" button on the program form
    Then modal closes without creating program

  @regression @allure.label.severity:critical
  Scenario: Master Cleanup - Delete all remaining test data
    Given I am on the Program Type page
    And I am on the Program tab from program type
    When I delete all programs containing "Automation" in their name
    Then all test automation programs should be deleted