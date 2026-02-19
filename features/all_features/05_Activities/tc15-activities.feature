@login_enroller_admin
Feature: tc15 - Activities management and operations
  As an Enroller Admin
  I want to manage and operate Activities
  So that I can ensure proper activity administration

  Scenario Outline: Activities search functionality
    Given I am on the Activities page
    When I fetch the first row data from the activities table
    And I enter the "<field>" value in activities search box
    Then the activities search results should match in activities table

    Examples:
      | field         |
      | Activity Name |

  Scenario Outline: Activities Action Buttons in Table
    Given I am on the Activities page
    When I click on "<button>" button in activities table first row
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                                   |
      | View History | Activity Operation History dialog opens           |
      | Duplicate    | Activity creation page loads with pre-filled data |
      | Edit         | Edit activity page loads                          |
      | Delete       | Activity delete confirmation dialog appears       |

  Scenario Outline: Activities Table Pagination - <records> Records per View
    Given I am on the Activities page
    When I select <records> records per page for activities table
    Then the activities table should display exactly <records> records per page

    Examples:
      | records |
      | 20      |
      | 50      |