@login_enroller_admin
Feature: tc19 - Tasks management and operations
  As an Enroller Admin
  I want to manage and operate tasks
  So that I can ensure proper tasks administration

  Scenario Outline: Tasks tab search functionality
    Given I am on the Workflow page
    And I am on the Tasks tab from workflow tasks
    When I fetch the first row data from the tasks table
    And I enter the "<field>" value in tasks search box
    Then the tasks search results should match in tasks table

    Examples:
      | field     |
      | Task Name |

  Scenario Outline: Tasks Action Buttons in Table
    Given I am on the Workflow page
    And I am on the Tasks tab from workflow tasks
    When I click on "<button>" button in tasks table first row
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                              |
      | View History | Task Operation History dialog opens          |
      | Edit         | Edit task page loads                         |
      | Delete       | Task delete confirmation dialog appears      |

  Scenario Outline: Tasks Table Pagination - <records> Records per View
    Given I am on the Workflow page
    And I am on the Tasks tab from workflow tasks
    When I select <records> records per page for tasks table
    Then the tasks table should display exactly <records> records per page for tasks tab

    Examples:
      | records |
      | 20      |
      | 50      |
