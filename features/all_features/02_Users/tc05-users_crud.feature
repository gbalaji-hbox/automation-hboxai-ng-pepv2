@login_enroller_admin
Feature: tc05 - Enroller Admin Manage Users

  @regression @smoke @allure.label.severity:critical
  Scenario: Master User CRUD Operations
    Given I am on the Users page
    And I am on the User tab from Users
    When I click "Add New User" button
    And I fill the create user form with valid data
    And I click "Save" button on the modal
    Then notification "User Created" appears

    When I find the created user in the list and click edit
    And I update the user last name to "Edited"
    And I click "Save" button on the modal
    Then notification "User updated successfully" appears

    When I find the edited user in the list and click delete
    And I confirm the user delete in the dialog
    Then notification "User deleted successfully" appears

  @regression @allure.label.severity:critical
  Scenario Outline: Validation - required field validation on input interaction for <field>
    Given I am on the Users page
    And I am on the User tab from Users
    When I click "Add New User" button
    And I enter "<character>" in "<field>" input field
    And I clear the "<field>" input field
    Then validation error message appears for "<field>"

    Examples:
      | field         | character |
      | first name    | a         |
      | last name     | b         |
      | email         | c         |
      | phone number  | d         |
      | password      | e         |

  @regression @allure.label.severity:critical
  Scenario: Cancel create operation
    Given I am on the Users page
    And I am on the User tab from Users
    When I click "Add New User" button
    And I fill the create user form with valid data
    And I click "Cancel" button on the modal
    Then modal closes without creating user

  @regression @allure.label.severity:critical
  Scenario: Master Cleanup - Delete all remaining test data
    Given I am on the Users page
    And I am on the User tab from Users
    When I delete all users containing "automation" in their email
    Then all test automation users should be deleted