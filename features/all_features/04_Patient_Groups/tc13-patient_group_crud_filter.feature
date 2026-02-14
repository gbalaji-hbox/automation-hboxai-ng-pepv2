@login_enroller_admin
Feature: tc13 - Patient Groups creation by filters
  As an Enroller Admin
  I want to create patient groups using different methods
  So that I can efficiently manage patient populations


  Scenario: Create patient group by filters and extract EMR IDs
    Given I am on the Patient Groups page
    When I click on "Create New Group" button
    And I select "Create New Group By Filters" from the create menu
    And I apply filters with clinic "HBox Internal"
    And I select first 5 patients in the patient results table
    And I click Create Group and enter valid group name and note
    Then the patient group should be created successfully

    When I find the created patient group in the list and click edit
    And I update the patient group name and save
    Then the patient group name should be updated successfully

    When I click the add patients button for the edited patient group
    And I apply filters with clinic "HBox Internal"
    And I select the first patient in the patient results table
    And I click add selected button on edited patient group page
    Then the patients should be added to the patient group successfully

    When I click the remove patients button for the edited patient group
    And I select the first patient in the table to be removed
    And I click remove selected button on edited patient group page
    Then the patients should be removed from the patient group successfully

    When returned to Patient Groups page from edited patient group page
    And I find the edited patient group in the list and click delete
    And I confirm the patient group delete in the dialog
    Then the patient group should be deleted successfully

  Scenario: Create duplicate patient group
    Given I am on the Patient Groups page
    When I find a patient group and click duplicate
    Then the duplicate page should open with correct heading
    And the default group name should contain "(Copy)"
    When I click create group button on duplicate page
    Then the duplicate patient group should be created successfully

  Scenario: Archive and unarchive patient group
    Given I am on the Patient Groups page
    When I find a patient group and click archive
    Then the archive confirmation dialog should appear
    When I confirm the archive action
    Then the patient group should be archived successfully
    When I click on Archived Groups button
    Then the archived groups page should open
    And the archived group should appear in the list
    When I click the unarchive button for the archived group
    Then the unarchive confirmation dialog should appear
    When I confirm the unarchive action
    Then the patient group should be restored to active status

  Scenario: Master Cleanup - Delete all remaining test Patient Groups
    Given I am on the Patient Groups page
    When I delete all patient groups containing "Automation" in their name
    Then all test automation patient groups should be deleted