@login_enroller_admin
Feature: tc12 - Patient Groups creation by filters and EMRs
  As an Enroller Admin
  I want to create patient groups using different methods
  So that I can efficiently manage patient populations

  @only
  Scenario: Create patient group by filters and extract EMR IDs
    Given I am on the Patient Groups page
    When I click on "Create New Group" button
    And I select "Create New Group By Filters" from the create menu
    And I apply filters with clinic "HBox Internal"
    And I extract the EMR IDs from the selected patients
    And returned to Patient Groups page
    When I click on "Create New Group" button
    And I select "Create New Group By EMRs" from the create menu
    When I create patient group by EMRs with clinic "HBox Internal" and the previously extracted EMR IDs
    And I click Create Group and enter valid group name and note
    Then the patient group should be created successfully