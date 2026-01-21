@login_enroller_admin
Feature: tc07- Program Type Management CRUD Operations
  As an enroller admin
  I want to manage program types
  So that I can create, read, update, delete program types and search/paginate

  Scenario Outline: Program tab search Functionality
    Given I am on the "Program Type" page
    And I am on the Program tab from Program Type
    When I fetch the first row data from the program table
    And I enter that value in the "<field>" search field and search on program tab in in Program Type page
    Then the program table should show filtered results in Program Type page

    Examples:
      | field               |
      | Program Name        |
      | Created Date        |
      | Applicable Statuses |

  Scenario Outline: Program Action Buttons in Table
    Given I am on the "Program Type" page
    And I am on the Program tab from Program Type
    When I click on "<button>" button for a program in the program table
    Then "<expected_result>" should happen in Program Type page

    Examples:
      | button       | expected_result                     |
      | Edit         | Edit Program page loads             |
      | View History | Program History dialog opens        |
      | Delete       | Delete Program confirmation appears |

  Scenario Outline: Program Table Pagination - <records> Records per View
    Given I am on the "Program Type" page
    And I am on the Program tab from Program Type
    When I select <records> records per page from pagination dropdown
    Then the program table should display exactly <records> records per page

    Examples:
      | records |
      | 20      |
      | 50      |
