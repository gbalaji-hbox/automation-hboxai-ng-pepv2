 @login_enroller_admin
Feature: tc22 - Tasks CRUD operations
  As an Enroller Admin
  I want to manage tasks
  So that I can ensure tasks administration

  @regression @smoke @allure.label.severity:critical
  Scenario: Master Tasks CRUD Operations
    Given I am on the Workflow & Tasks page
    And I am on the Tasks tab from workflow tasks
    When I click "Add New Task" button
    And I fill the create task form with valid data
    And I click "Save" button on the task form
    Then notification "Task created successfully" appears

    When I find the created task in the list and click edit
    And I update the task name to "Edited"
    And I click "Update" button on the task form
    Then notification "Task updated successfully" appears

    When I find the edited task in the list and click delete
    And I confirm the task delete in the dialog
    Then notification "Task deleted successfully" appears

  @regression @allure.label.severity:critical
  Scenario: Cancel task create operation
    Given I am on the Workflow & Tasks page
    And I am on the Tasks tab from workflow tasks
    When I click "Add New Task" button
    And I fill the create task form with valid data
    And I click "Cancel" button on the task form
    Then task form closes without creating record

  @regression @allure.label.severity:critical
  Scenario: Master Cleanup - Delete all remaining tasks test data
    Given I am on the Workflow & Tasks page
    And I am on the Tasks tab from workflow tasks
    When I delete all tasks containing "Automation" in their name
    Then all test automation tasks should be deleted