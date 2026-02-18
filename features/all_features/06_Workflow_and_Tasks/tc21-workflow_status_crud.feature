@login_enroller_admin
Feature: tc21 - Workflow Status CRUD operations
  As an Enroller Admin
  I want to manage workflow statuses
  So that I can ensure workflow status administration

  @regression @smoke @allure.label.severity:critical
  Scenario: Master Workflow Status CRUD Operations
    Given I am on the Workflow & Tasks page
    And I am on the Workflow Status tab from workflow tasks
    When I click "Add New Workflow Status" button
    And I fill the create workflow status form with valid data
    And I click "Save" button on the workflow status form
    Then notification "Workflow Status created successfully" appears

    When I find the created workflow status in the list and click edit
    And I update the workflow status name to "Edited"
    And I click "Update" button on the workflow status form
    Then notification "Workflow Status updated successfully" appears

    When I find the edited workflow status in the list and click delete
    And I confirm the workflow status delete in the dialog
    Then notification "Workflow Status deleted successfully" appears

  @regression @allure.label.severity:critical
  Scenario: Cancel workflow status create operation
    Given I am on the Workflow & Tasks page
    And I am on the Workflow Status tab from workflow tasks
    When I click "Add New Workflow Status" button
    And I fill the create workflow status form with valid data
    And I click "Cancel" button on the workflow status form
    Then workflow status form closes without creating record

  @regression @allure.label.severity:critical
  Scenario: Master Cleanup - Delete all remaining workflow status test data
    Given I am on the Workflow & Tasks page
    And I am on the Workflow Status tab from workflow tasks
    When I delete all workflow statuses containing "Automation" in their name
    Then all test automation workflow statuses should be deleted