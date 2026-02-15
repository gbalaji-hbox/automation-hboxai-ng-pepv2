@login_enroller_admin
Feature: tc17 - Workflow management and operations
  As an Enroller Admin
  I want to manage and operate workflows
  So that I can ensure proper workflow administration

  @only
  Scenario Outline: Workflow tab search functionality
    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I fetch the first row data from the workflow table
    And I select <field> option and enter the fetched data in workflow search box
    Then the workflow search results should match in workflow table

    Examples:
      | field               |
      | Workflow Name       |
      | Applicable Programs |
      | Assigned User Group |

  Scenario Outline: Workflow Action Buttons in Table
    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I click on "<button>" button in workflow table first row
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                             |
      | View History | Workflow Operation History dialog opens     |
      | Edit         | Edit workflow page loads                    |
      | Delete       | Workflow delete confirmation dialog appears |

  Scenario Outline: Workflow Table Pagination - <records> Records per View
    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I select <records> records per page for workflow table
    Then the workflow table should display exactly <records> records per page for workflow tab

    Examples:
      | records |
      | 20      |
      | 50      |
