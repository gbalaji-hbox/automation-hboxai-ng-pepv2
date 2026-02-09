@login_enroller_admin
Feature: tc11 - Patient Groups management and operations
  As an Enroller Admin
  I want to manage and operate patient groups
  So that I can ensure proper patient group administration

  Scenario: Patient Groups search functionality
    Given I am on the Patient Groups page
    When I fetch the first row data from the patient groups table
    And I enter that value in the group search field and search
    Then the Patient Groups table should show the results matching the search criteria

  Scenario Outline: Patient Groups Action Buttons in Table
    Given I am on the Patient Groups page
    When I click on "<button>" button for a Patient Group in the table
    Then "<expected_result>" should happen

    Examples:
      | button       | expected_result                                   |
      | View History | Patient Group Operation History dialog opens      |
      | Edit         | Edit Patient Group page loads                     |
      | Delete       | delete Patient Group confirmation dialog appears  |
      | Archive      | archive Patient Group confirmation dialog appears |
      | Duplicate    | Duplicate Patient Group details page loads        |


  Scenario Outline: Patient Groups Table Pagination - <records> Records per View
    Given I am on the Patient Groups page
    When I select <records> records per page from dropdown for patient groups table
    Then the patient groups table should display exactly <records> records per page

    Examples:
      | records |
      | 25      |
      | 50      |

  Scenario Outline: Create New Group menu navigation
    Given I am on the Patient Groups page
    When I click on "Create New Group" button
    And I select "<option>" from the create menu
    Then I should be navigated to the "<page>" page

    Examples:
      | option                      | page                    |
      | Create New Group By EMRs    | Create Group By EMRs    |
      | Create New Group By Filters | Create Group By Filters |
      | Create New Group By Excel   | Create Group By Excel   |