@login_enroller_admin
Feature: tc07 - Programs management and operations
  As an Enroller Admin
  I want to manage and operate programs
  So that I can ensure proper program administration

  Scenario Outline: Program tab search functionality
    Given I am on the Program Type page
    And I am on the Program tab from program type
    When I fetch the first row data from the programs table
    And I select <field> option and enter the fetched data in the search box
    Then the Program table should show matching results

    Examples:
      | field               |
      | Program Name        |
      | Created Date        |
      | Applicable Statuses |


  Scenario Outline: Program Action Buttons in Table
    Given I am on the Program Type page
    And I am on the Program tab from program type
    When I click on "<button>" button in programs table first row
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                            |
      | View History | Program Operation History dialog opens     |
      | Edit         | Edit program page loads                    |
      | Delete       | Program delete confirmation dialog appears |

  @only
  Scenario Outline: Programs Table Pagination - <records> Records per View
    Given I am on the Program Type page
    And I am on the Program tab from program type
    When I select <records> records per page for programs table
    Then the Programs table should display exactly <records> records per page

    Examples:
      | records |
      | 20      |
      | 50      |