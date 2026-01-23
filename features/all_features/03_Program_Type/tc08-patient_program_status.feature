@login_enroller_admin
Feature: tc08 - Patient Program Status management and operations
  As an Enroller Admin
  I want to manage and operate patient program statuses
  So that I can ensure proper patient program status administration

  Scenario Outline: Patient Program Status tab search functionality
    Given I am on the Program Type page
    And I am on the Patient Program Status tab from program type
    When I fetch the first row data from the patient programs status table
    And I enter the "<field>" value in the patient program status search box
    Then the Patient Program Status table should show matching results

    Examples:
      | field       |
      | Status Name |


  Scenario Outline: Patient Program Status Action Buttons in Table
    Given I am on the Program Type page
    And I am on the Patient Program Status tab from program type
    When I click on "<button>" button in patient program status table first row
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                                           |
      | View History | Patient Program Status Operation History dialog opens     |
      | Edit         | Edit patient program status page loads                    |
      | Delete       | Patient program status delete confirmation dialog appears |

  Scenario Outline: Patient Program Status Table Pagination - <records> Records per View
    Given I am on the Program Type page
    And I am on the Patient Program Status tab from program type
    When I select <records> records per page for patient program status table
    Then the Patient Program Status table should display exactly <records> records per page

    Examples:
      | records |
      | 20      |
      | 50      |