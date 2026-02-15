@login_enroller_admin
Feature: tc18 - Workflow Status management and operations
  As an Enroller Admin
  I want to manage and operate workflow statuses
  So that I can ensure proper workflow status administration

  Scenario Outline: Workflow Status tab search functionality
    Given I am on the Workflow page
    And I am on the Workflow Status tab from workflow tasks
    When I fetch the first row data from the workflow status table
    And I enter the "<field>" value in workflow status search box
    Then the workflow status search results should match in workflow status table

    Examples:
      | field                |
      | Workflow Status Name |

  Scenario Outline: Workflow Status Action Buttons in Table
    Given I am on the Workflow page
    And I am on the Workflow Status tab from workflow tasks
    When I click on "<button>" button in workflow status table first row
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                                      |
      | View History | Workflow Status Operation History dialog opens       |
      | Edit         | Edit workflow status page loads                      |
      | Delete       | Workflow status delete confirmation dialog appears   |

  Scenario Outline: Workflow Status Table Pagination - <records> Records per View
    Given I am on the Workflow page
    And I am on the Workflow Status tab from workflow tasks
    When I select <records> records per page for workflow status table
    Then the workflow status table should display exactly <records> records per page for workflow status tab

    Examples:
      | records |
      | 20      |
      | 50      |
