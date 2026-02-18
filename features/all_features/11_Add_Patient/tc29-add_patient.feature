@login_enroller_admin
Feature: tc29 - Add Patient

  @regression @smoke @allure.label.severity:critica
  Scenario: Add new patient with all mandatory fields
    Given I am on the Add Patient page
    When I select "HBox Internal" clinic
    And I select "facility_01" facility
    And I select the first available provider
    And I fill the patient personal information with valid data
    And I fill the medical records with valid data
    And I click "Continue" button to proceed to address
    And I fill the address information with valid data
    And I click "Continue" button to proceed to summary
    And I click "Submit" button to create patient
    Then notification "Patient added successfully!" appears

  @regression @allure.label.severity:critical
  Scenario: Add new patient with all fields including optional
    Given I am on the Add Patient page
    When I select "HBox Internal" clinic
    And I select "facility_01" facility
    And I select the first available provider
    And I fill the patient personal information with valid data including optional fields
    And I fill the medical records with valid data including optional fields
    And I select "RPM Eligible" program eligibility
    And I fill the emergency contact information
    And I click "Continue" button to proceed to address
    And I fill the address information with valid data including optional fields
    And I click "Continue" button to proceed to summary
    And I verify the summary page displays all patient information
    And I click "Submit" button to create patient
    Then notification "Patient added successfully!" appears

  @regression @allure.label.severity:critical
  Scenario: Verify Continue button is disabled when mandatory fields are empty
    Given I am on the Add Patient page
    Then the Continue button should be disabled

  @regression @allure.label.severity:critical
  Scenario: Navigate back from address step to patient details
    Given I am on the Add Patient page
    When I select "HBox Internal" clinic
    And I select "facility_01" facility
    And I select the first available provider
    And I fill the patient personal information with valid data
    And I fill the medical records with valid data
    And I click "Continue" button to proceed to address
    And I click "Previous" button to go back
    Then I should be on the Patient Details step

  @regression @allure.label.severity:critical
  Scenario: Facility and Provider dropdowns are disabled before selecting clinic
    Given I am on the Add Patient page
    Then the Facility dropdown should be disabled
    And the Provider dropdown should be disabled