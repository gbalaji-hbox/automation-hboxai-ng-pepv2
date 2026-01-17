@login_enroller_admin
Feature: tc04- User Group Management CRUD Operations
  As an enroller admin
  I want to manage user groups
  So that I can create, read, update, delete user groups and search/paginate

  Scenario Outline: User tab search Functionality
    Given I am on the Users page
    And I am on the User Group tab
    When I fetch the first row data from the user groups table
    And I enter that value in the "<field>" search field and search
    Then the user groups table should filter results to show matching groups

    Examples:
      | field        |
      | Group Name   |
      | Total Users  |
      | Created Date |
      | Updated Date |

  Scenario Outline: Users Action Buttons in Table
    Given I am on the Users page
    And I am on the User Group tab
    When I click on "<button>" button for a user group in the user groups table
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                               |
      | View History | User group Operation History dialog opens     |
      | Edit         | Edit User Group page loads                    |
      | Delete       | delete User Group confirmation dialog appears |


  Scenario Outline: User Table Pagination - <records> Records per View
    Given I am on the Users page
    And I am on the User Group tab
    When I select <records> records per page from pagination dropdown
    Then the user group table should display exactly <records> records per page

    Examples:
      | records |
      | 20      |
      | 50      |