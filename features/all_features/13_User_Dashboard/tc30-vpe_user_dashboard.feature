@login_vpe_user
Feature: tc30 - Workflow Patient flow functionality
  As a VPE user
  I want to do patient engagement update functionality in VPE User portal
  So that I can verify the system handles patient updates as per workflow configured

  @regression @allure.label.severity:critical
  Scenario: Successful patient engagement update flow
    Given I logged in to dashboard as "vpe_user"
    When I select "Consent" from Enrollment Status dropdown as "vpe_user"
    And I select "Call Answered" from workflow Status dropdown as "vpe_user"
    And comments "Automation Test Patient update" are entered as "vpe_user"
    And I click "Save" button in the VPE user dashboard as "vpe_user"
    Then patient engagment should be updated succesfully for "vpe_user"
    When I click Next Patient button in the VPE user dashboard as "vpe_user"
    Then new patient details should be loaded for "vpe_user"
    Then I close all browser instances for patient engagement update flow feature
