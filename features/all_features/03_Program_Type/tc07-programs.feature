@login_enroller_admin
Feature: tc07 - Programs management and operations
  As an Enroller Admin
  I want to manage and operate programs
  So that I can ensure proper program administration

  @only
  Scenario Outline: Program tab search functionality
    Given I am on the Program Type page
    And I am on the Program tab from program type
    When I fetch the first row data from the programs table
    And I select <field> option and enter the fetched data in the search box
    Then the Program table should show matching results

    Examples:
      | field             |
      | Program Name      |
      | Created Date      |
      | Applicable Status |