@login_parallel @e2e
Feature: tc16 - Activities CRUD E2E Test with Patient Workflow Movement
  As an Enroller Admin
  I want to create a complete workflow system with users, groups, patient groups, workflows, and activities
  and validate patient movement across sequential workflows based on status changes
  So that I can ensure the entire patient care coordination system works end-to-end

  @regression @smoke @allure.label.severity:blocker
  Scenario: Complete E2E Activities CRUD with Patient Workflow Movement
    # ===== SETUP PHASE: Create Users, Groups, Patient Groups, Workflows =====
    
    # Create 3 users with specific roles
    Given I login as "enroller_admin"
    And I am on the Users page
    And I am on the User tab from Users
    When I create ES user with automation email and password "123456"
    Then notification "User Created" appears
    And I store the created user email as "ES_User_Email"

    When I create CS user with automation email and password "123456"
    Then notification "User Created" appears
    And I store the created user email as "CS_User_Email"

    When I create PE user with automation email and password "123456"
    Then notification "User Created" appears
    And I store the created user email as "PE_User_Email"
    
    # Create 3 groups and assign users

    Given I am on the Users page
    And I am on the User Group tab from Users
    When I create user group "ES_Group" and assign user with email stored as "ES_User_Email"
    Then notification "User Group Created" appears

    When I create user group "CS_Group" and assign user with email stored as "CS_User_Email"
    Then notification "User Group Created" appears

    When I create user group "PE_Group" and assign user with email stored as "PE_User_Email"
    Then notification "User Group Created" appears

    # Create patient group with 10 patients using filters
    Given I am on the Patient Groups page
    When I create patient group "Automation_Patient_Group_10" with 10 patients using filters
    Then the patient group should be created successfully

    # Create Workflow_1 (no trigger, ES_Group)
    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I create workflow "Automation_Workflow_1" with program "CCM" and no trigger
    And I assign task "Call" with 0 days waiting period
    And I assign user group "ES_Group"
    And I submit the workflow
    Then notification "Workflow created successfully" appears

    # Create Workflow_2 (triggered by Workflow_1 status = Consent, CS_Group)
    When I create workflow "Automation_Workflow_2" with program "CCM" triggered by "Automation_Workflow_1" status "Consent"
    And I assign task "Call" with 0 days waiting period
    And I assign user group "CS_Group"
    And I submit the workflow
    Then notification "Workflow created successfully" appears

    # Create Workflow_3 (triggered by Workflow_2 status = Enrolled (Virtual), PE_Group)
    When I create workflow "Automation_Workflow_3" with program "CCM" triggered by "Automation_Workflow_2" status "Enrolled (Virtual)"
    And I assign task "Call" with 0 days waiting period
    And I assign user group "PE_Group"
    And I submit the workflow
    Then notification "Workflow created successfully" appears

    # ===== ACTIVITY CREATION PHASE =====

    # Create activity for the test patient in Workflow_1
    Given I am on the Activities page
    When I click Add New Activity button
    And I fill activity form with name "Automation_TC16_Test_Activity" for patient group "Automation_Patient_Group_10" and workflow "Automation_Workflow_1"
    And I set activity execution timeline from yesterday to 3 months as per timezone
    And I submit the activity
    Then the activity should be created successfully

    # ===== WORKFLOW MOVEMENT PHASE: Role-Based Actions =====

    # ES_User changes patient status to Consent
    Given I login as ES user with stored email "ES_User_Email" and password "123456" as "es_user"
    When I navigate to dashboard as "es_user"
    And I change enrollment status to "Consent" as "es_user"
    And I Change workflow status to "Call Answered" as "es_user"
    And I enter the comment of the update as "es_user"
    And I click on save button for status update as "es_user"
    Then status update notification appears for "es_user"
    When I click on next patient button as "es_user"
    Then I should see next patient loaded in dashboard as "es_user"
    And I logout from the application as "es_user"

     # Verify patient moved to Workflow_2 (CS_User can see it)
    Given I login as CS user with stored email "CS_User_Email" and password "123456" as "cs_user"
    When I navigate to dashboard as "cs_user"
    Then I should see patient from previous workflow step in my dashboard as "cs_user"
    When I change enrollment status to "Enrolled (Virtual)" as "cs_user"
    And I Change workflow status to "Call Answered" as "cs_user"
    And I enter the comment of the update as "cs_user"
    And I click on save button for status update as "cs_user"
    Then status update notification appears for "cs_user"
    When I click on next patient button as "cs_user"
    Then I should see next patient loaded in dashboard as "cs_user"
    And I logout from the application as "cs_user"

     # Verify patient moved to Workflow_3 (PE_User can see it)
    Given I login as PE user with stored email "PE_User_Email" and password "123456" as "pe_user"
    When I navigate to dashboard as "pe_user"
    Then I should see patient from previous workflow step in my dashboard as "pe_user"
    When I change enrollment status to "Transferred" as "pe_user"
    And I Change workflow status to "Call Answered" as "pe_user"
    And I enter the comment of the update as "pe_user"
    And I click on save button for status update as "pe_user"
    Then status update notification appears for "pe_user"
    When I click on next patient button as "pe_user"
    Then I should see next patient loaded in dashboard as "pe_user"
    And I logout from the application as "pe_user"

    # Cleanup: Delete all created entities
    Given I returned to "enroller_admin" dashboard
    And I am on the Activities page
    When I delete all activities containing "Automation_TC16_Test_Activity" in their name
    Then all test activities should be deleted
#
    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I delete workflow "Automation_Workflow_3"
    Then notification "Workflow deleted successfully" appears

    When I delete workflow "Automation_Workflow_2"
    Then notification "Workflow deleted successfully" appears

    When I delete workflow "Automation_Workflow_1"
    Then notification "Workflow deleted successfully" appears

    Given I am on the Patient Groups page
    When I find and delete patient group "Automation_Patient_Group_10"
    Then the patient group should be deleted successfully

    Given I am on the Users page
    And I am on the User Group tab from Users
    When I find and delete user group "PE_Group"
    Then notification "User group deleted successfully" appears

    When I find and delete user group "CS_Group"
    Then notification "User group deleted successfully" appears

    When I find and delete user group "ES_Group"
    Then notification "User group deleted successfully" appears

    Given I am on the Users page
    And I am on the User tab from Users
    When I find and delete user with email stored as "PE_User_Email"
    Then notification "User deleted successfully" appears

    When I find and delete user with email stored as "CS_User_Email"
    Then notification "User deleted successfully" appears

    When I find and delete user with email stored as "ES_User_Email"
    Then notification "User deleted successfully" appears
    Then I close all browser instances for parallel users

  @regression @allure.label.severity:critical
  Scenario: Master Cleanup - Delete all remaining test activities
    Given I login as "enroller_admin"
    And I am on the Activities page
    When I delete all activities containing "Automation" in their name
    Then all test activities should be deleted

    Given I am on the Workflow & Tasks page
    And I am on the Workflow tab from workflow tasks
    When I delete all workflows containing "Automation" in their name
    Then all test automation workflows should be deleted

    Given I am on the Patient Groups page
    When I delete all patient groups containing "Automation" in their name
    Then all test automation patient groups should be deleted

    Given I am on the Users page
    And I am on the User Group tab from Users
    When I delete all user groups containing "Automation" in their name
    Then all test automation user groups should be deleted

    Given I am on the Users page
    And I am on the User tab from Users
    When I delete all users containing "Automation" in their email
    Then all test automation users should be deleted
