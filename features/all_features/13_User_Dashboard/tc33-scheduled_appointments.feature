@login_vpe_internal
Feature: tc27 - Scheduled Appointments management and operations
  As an Enroller Admin
  I want to view and manage Scheduled Appointments
  So that I can track patient appointments across virtual and in-person channels

  @regression @smoke
  Scenario: Virtual tab is active by default on Scheduled Appointments page
    Given I am on the Scheduled Appointments page
    Then the "Virtual" tab should be active
    And the scheduled appointments table should display records

  @regression
  Scenario Outline: Virtual tab - Search functionality by field
    Given I am on the Scheduled Appointments page
    And I am on the "Virtual" tab
    When I fetch the first row data from the scheduled appointments table
    And I search by "<field>" with the fetched value in scheduled appointments
    Then the scheduled appointments search results should match in the table

    Examples:
      | field            |
      | Patient Name     |
      | Appointment Date |
      | Clinic Name      |
      | User Name        |

  @regression
  Scenario Outline: Virtual tab - Table Pagination
    Given I am on the Scheduled Appointments page
    And I am on the "Virtual" tab
    When I select <records> records per page for scheduled appointments table
    Then the scheduled appointments table should display exactly <records> records per page

    Examples:
      | records |
      | 25      |
      | 50      |

  @regression @smoke
  Scenario: Navigate to patient details from Virtual tab
    Given I am on the Scheduled Appointments page
    And I am on the "Virtual" tab
    When I click on the patient name button in the first row
    Then I should be navigated to the patient details page
