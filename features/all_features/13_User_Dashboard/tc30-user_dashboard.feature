@login_vpe_internal
Feature: tc30 - User Dashboard appointment scheduling
  As a VPE internal user
  I want to schedule virtual and physical appointments from the dashboard
  So that patient enrollment updates are saved successfully

  @regression @smoke @allure.label.severity:critical
  Scenario: Schedule a virtual appointment from the dashboard
    Given I am on User Dashboard page
    When I wait for patient details to load in the dashboard
    And I set enrollment status to "Consent"
    And I set workflow status to "Call Answered"
    And I set appointment type to "Virtual"
    And I select the first available resource
    And I select the available appointment date and slot
    And I enter a the comment for the engagement
    And I save the patient enrollment
    Then Patient engagement should be saved successfully
    When I click on the Next Patient button
    Then I should see the next patient details in the dashboard

  @regression @smoke @allure.label.severity:critical
  Scenario: Schedule a physical appointment from the dashboard
    Given I am on User Dashboard page
    When I wait for patient details to load in the dashboard
    And I set enrollment status to "Consent"
    And I set workflow status to "Call Answered"
    And I set appointment type to "In Person"
    And I select the first available facility
    And I select the available appointment date and slot
    And I enter a the comment for the engagement
    And I save the patient enrollment
    Then Patient engagement should be saved successfully
    When I click on the Next Patient button
    Then I should see the next patient details in the dashboard