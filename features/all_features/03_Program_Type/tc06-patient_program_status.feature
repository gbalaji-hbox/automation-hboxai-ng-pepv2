@login_enroller_admin
Feature: tc06 - Patient Program Status Management CRUD Operations
  As an enroller admin
  I want to manage patient program statuses
  So that I can create, read, update, delete patient program statuses and search/paginate

  Scenario Outline: Patient Program Status tab search Functionality
    Given I am on the "Program Type" page
    And I am on the Patient Program Status tab
    When I fetch the first row data from the patient program status table
    And I enter that value in the "<field>" search field and search
    Then the patient program status table should filter results to show matching statuses

    Examples:
      | field        |
      | Status Name  |
      | Created Date |

  Scenario Outline: Patient Program Status Action Buttons in Table
    Given I am on the "Program Type" page
    And I am on the Patient Program Status tab
    When I click on "<button>" button for a patient program status in the status table
    Then "<expected_result>" should happen

    Examples:
      | button | expected_result                      |
      | Edit   | Edit Patient Program Status page loads |
      | View   | Status details dialog opens         |
      | Delete | Delete confirmation appears         |

  Scenario Outline: Patient Program Status Table Pagination - <records> Records per View
    Given I am on the "Program Type" page
    And I am on the Patient Program Status tab
    When I select <records> records per page from pagination dropdown
    Then the patient program status table should display exactly <records> records per page

    Examples:
      | records |
      | 10      |
      | 25      |
