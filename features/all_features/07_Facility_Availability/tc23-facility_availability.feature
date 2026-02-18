@login_enroller_admin
Feature: tc23 - Facility Availability management and operations
  As an Enroller Admin
  I want to manage and operate Facility Availability
  So that I can ensure proper facility availability administration

  Scenario Outline: Facility Availability search functionality
    Given I am on the Facility Availability page
    When I fetch the first row data from the facility availability table
    And I select <field> option and enter the fetched data in facility availability search box
    Then the facility availability search results should match in facility availability table

    Examples:
      | field         |
      | Clinic Name   |
      | Facility Name |

  Scenario Outline: Facility Availability Action Buttons in Table
    Given I am on the Facility Availability page
    When I click on "<button>" button in facility availability table first row
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                                        |
      | View History | Facility Availability Operation History dialog opens    |
      | Edit         | Edit facility availability page loads                   |
      | Delete       | Facility availability delete confirmation dialog appears |

  Scenario Outline: Facility Availability Table Pagination - <records> Records per View
    Given I am on the Facility Availability page
    When I select <records> records per page for facility availability table
    Then the facility availability table should display exactly <records> records per page

    Examples:
      | records |
      | 20      |
      | 50      |