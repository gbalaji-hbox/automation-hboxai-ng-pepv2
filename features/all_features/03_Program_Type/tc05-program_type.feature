@login_enroller_admin
Feature: tc05 - Program Type & Patient Program Status Management
  As an enroller admin
  I want to manage program types and patient program statuses
  So that I can configure and maintain program offerings and status tracking

  Scenario: Verify Program Type page navigation and default state
    Given I am logged in as a valid user
    When I navigate to the Program Type page
    Then I should see the Program Type page title
    And I should see the Program tab as active by default
    And I should see the Patient Program Status tab as inactive
    And I should see the Add New Program button
    And I should see the program table with correct headers

  Scenario: Switch between Program and Patient Program Status tabs
    Given I am on the "Program Type" page
    When I click on the Patient Program Status tab
    Then I should see the Patient Program Status tab as active
    And I should see the Program tab as inactive
    And I should see the Add New Patient Program Status button
    And I should see the status table with correct headers

  Scenario: Verify Program tab table structure and data
    Given I am on the "Program Type" page
    When I view the program table
    Then I should see programs listed in the table
    And I should see program names, created dates, applicable statuses, and actions columns
    And I should see action buttons for each program row

  Scenario: Verify Patient Program Status tab table structure and data
    Given I am on the "Program Type" page
    When I switch to the Patient Program Status tab
    Then I should see patient program statuses listed in the table
    And I should see status names, created dates, and actions columns
    And I should see action buttons for each status row

  Scenario Outline: Search programs by name
    Given I am on the "Program Type" page
    When I search for program "<search_term>"
    Then I should see the search results filtered correctly
    And I should be able to clear the search

    Examples:
      | search_term |
      | CCM         |
      | RPM         |
      | invalid     |

  Scenario Outline: Search patient program statuses by name
    Given I am on the "Program Type" page
    And I am on the Patient Program Status tab
    When I search for status "<search_term>"
    Then I should see the status search results filtered correctly

    Examples:
      | search_term |
      | Enrolled    |
      | Decline     |
      | Consent     |

  Scenario Outline: Change entries per page for programs
    Given I am on the "Program Type" page
    When I select <entries> entries per page for programs
    Then I should see pagination info showing <entries> entries

    Examples:
      | entries |
      | 20      |
      | 50      |

  Scenario Outline: Change entries per page for statuses
    Given I am on the "Program Type" page
    And I am on the Patient Program Status tab
    When I select <entries> entries per page for statuses
    Then I should see status pagination info showing <entries> entries

    Examples:
      | entries |
      | 10      |
      | 25      |

  Scenario: Verify program action buttons functionality
    Given I am on the "Program Type" page
    When I view the program table
    Then I should see Edit, View, and Delete buttons for each program
    And the buttons should be clickable

  Scenario: Verify patient program status action buttons functionality
    Given I am on the "Program Type" page
    And I am on the Patient Program Status tab
    When I view the status table
    Then I should see Edit, View, and Delete buttons for each status
    And the status buttons should be clickable

  Scenario: Verify existing programs are displayed
    Given I am on the "Program Type" page
    Then I should see "CCM" program in the table
    And I should see "RPM" program in the table

  Scenario: Verify existing patient program statuses are displayed
    Given I am on the "Program Type" page
    And I am on the Patient Program Status tab
    Then I should see "Enrolled (Virtual)" status in the table
    And I should see "Decline" status in the table
    And I should see "Consented (In-Person)" status in the table
