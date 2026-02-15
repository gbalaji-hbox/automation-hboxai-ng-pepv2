@login_enroller_admin
Feature: tc20 - Workflow CRUD operations
  As an Enroller Admin
  I want to manage workflows
  So that I can ensure workflow administration

  @regression @smoke @allure.label.severity:critical
  Scenario: Master Workflow CRUD Operations
    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I click "Create New Workflow" button
    And I fill the create workflow form with valid data
    And I click "Create Workflow" button on the workflow form
    Then notification "Workflow created successfully" appears

    When I find the created workflow in the list and click edit
    And I update the workflow name to "Edited"
    And I remove a trigger row from the workflow
    And I click "Update Workflow" button on the workflow form
    Then notification "Workflow updated successfully" appears

    When I find the edited workflow in the list and click delete
    And I confirm the workflow delete in the dialog
    Then notification "Workflow deleted successfully" appears

  @regression @allure.label.severity:critical
  Scenario: Cancel create operation
    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I click "Create New Workflow" button
    And I fill the create workflow form with valid data
    And I click "Cancel" button on the workflow form
    Then modal closes without creating workflow

  @regression @allure.label.severity:critical
  Scenario: Master Cleanup - Delete all remaining test data
    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I delete all workflows containing "Automation" in their name
    Then all test automation workflows should be deleted