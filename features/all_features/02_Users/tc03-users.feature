@login_enroller_admin
Feature: tc03- Users Management CRUD Operations
  As an enroller admin
  I want to manage users
  So that I can create, read, update, delete users and search/paginate

  Scenario Outline: User tab search Functionality
    Given I am on the Users page
    And I am on the Users tab
    When I fetch the first row data from the users table
    And I enter that value in the "<field>" search field and search
    Then the users table should filter results to show matching users

    Examples:
      | field        |
      | Email        |
      | User Name    |
      | User Type    |
      | Update Date |
      | Last Active  |

  Scenario Outline: Users Action Buttons in Table
    Given I am on the Users page
    And I am on the user tab
    When I click on "<button>" button for a user in the users table
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                     |
      | View History | User Operation History dialog opens |
      | Edit         | Edit User page loads                |
      | Delete       | confirmation dialog appears         |


  Scenario Outline: User Table Pagination - <records> Records per View
    Given I am on the Users page
    And I am on the user tab
    When I select <records> records per page from pagination dropdown
    Then the table should display exactly <records> records per page

    Examples:
      | records |
      | 20      |
      | 50      |