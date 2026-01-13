@login_enroller_admin
Feature: tc01 - Main Dashboard
    As a valid user
    I want to access the main dashboard
    So that I can view key information and navigate to other sections of the application

  Scenario: Verify main dashboard elements
    Given I am logged in as a valid user
    When I navigate to the Dashboard page
    Then I should see the dashboard header
    And I should see the main navigation menu
    And I should see the user profile section