@login_enroller_admin
Feature: tc12 - Patient Groups creation by filters and EMRs
  As an Enroller Admin
  I want to create patient groups using different methods
  So that I can efficiently manage patient populations

  Scenario: Create patient group by filters and extract EMR IDs
    Given I am on the Patient Groups page
    When I click on "Create New Group" button
    And I select "Create New Group By Filters" from the create menu
    Then I should be navigated to the "Create Group By Filters" page
    When I apply filters with clinic "HBox Internal"
    And I select 5 random patients from the filtered results
    And I extract the EMR IDs from the selected patients
    And I name the group "Test Group - HBox Internal Patients" and save it
    Then the patient group should be created successfully

  Scenario: Create patient group by EMRs using extracted IDs
    Given I am on the Patient Groups page
    When I click on "Create New Group" button
    And I select "Create New Group By EMRs" from the create menu
    Then I should be navigated to the "Create Group By EMRs" page
    When I create patient group by EMRs with clinic "HBox Internal" and the previously extracted EMR IDs
    And I name the group "Test Group - HBox Internal EMRs" and save it
    Then the patient group should be created successfully