@login_enroller_admin
Feature: tc24 - Facility Availability CRUD operations
  As an Enroller Admin
  I want to manage facility availability records
  So that I can maintain clinic-facility schedule windows

  @regression @smoke @allure.label.severity:critical
  Scenario: Master Facility Availability CRUD Operations
    Given I am on the Facility Availability page
    When I click "Add New Facility Availability" button
    And I fill the create facility availability form with valid data
    And I click "Create Facility Availability" button on the facility availability form
    Then notification "Facility availability created successfully" appears

    When I find the created facility availability in the list and click edit
    And I update the facility availability end date
    And I click "Update Facility Availability" button on the facility availability form
    Then notification "Facility availability updated successfully" appears

    When I find the updated facility availability in the list and click delete
    And I confirm the facility availability delete in the dialog
    Then notification "Facility availability deleted" appears

  @regression @allure.label.severity:critical
  Scenario: Cancel create operation
    Given I am on the Facility Availability page
    When I click "Add New Facility Availability" button
    And I fill the create facility availability form with valid data
    And I click "Cancel" button on the facility availability form
    Then facility availability form closes without creating record