@login_vpe_internal
Feature: tc02 - Dynamic Hamburger Menu Navigation on NGPEP portal

  As a user
  I want to navigate to different sections of the application via the Hamburger Menu
  So that I can access various functionalities dynamically based on available options


  Scenario: Verify all available menu options are accessible and navigate correctly
    Given I am on the Dashboard page
    When I extract all available hamburger menu options
    Then I should verify each menu option navigates to the correct page
    And I should verify each menu option has the correct browser title
    And I should verify all menu option links are functional

  Scenario: Verify "Logout" functionality
    Given I am on the Dashboard page
    When I click on "Logout" in the Hamburger Menu
    Then I should be logged out and navigated to the Login page
