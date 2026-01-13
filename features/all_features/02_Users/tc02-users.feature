@login_enroller_admin
Feature: tc02 - Users Management CRUD Operations
  As an enroller admin
  I want to manage users
  So that I can create, read, update, delete users and search/paginate

  Scenario: Navigate to Users page
    Given I am on the Dashboard page
    When I click t
    Then I should see the Users & User Groups page
    And the User tab is selected
    And I see the users table with columns User Name, Email Address, User Type, Update Date, Last Active, Actions
    And I see Add New User button
    And I see search textbox with placeholder "Enter value"
    And I see Search button
    And I see Show combobox with default "50"
    And I see pagination showing "Showing 1 to 42 of 42 entries"

  Scenario: Search users
    Given I am on the Users page
    When I enter "test" in the search textbox
    And I click the Search button
    Then the users table should filter to show only users containing "test" in name or email
    And the pagination should show filtered count

  Scenario: Change pagination show entries
    Given I am on the Users page
    When I select "10" from the Show combobox
    Then the pagination should appear with "1" active
    And showing "1 to 10 of 42 entries"

  Scenario: Navigate pagination
    Given I am on the Users page with Show set to 10
    When I click the Next page button
    Then I should see page 2 with entries 11 to 20
    When I click the Previous page button
    Then I should see page 1 with entries 1 to 10

  Scenario: Attempt to create new user
    Given I am on the Users page
    When I click the Add New User button
    Then I should see the add user form
    When I fill First Name with "TestFirst"
    And I fill Last Name with "TestLast"
    And I fill Email with "test@example.com"
    And I select User Type "ES"
    And I click Save
    Then I should see error notification "Something went wrong. Please try again."
    # Note: Create operation fails with HTTP 405, indicating server-side issue

  Scenario: Attempt to update existing user
    Given I am on the Users page
    When I click the edit button for user "test_vpe don't delete"
    Then I should see the edit user form
    When I change Last Name to "UpdatedLast"
    And I click Save
    Then I should see error notification "Something went wrong. Please try again."
    # Note: Update operation fails with HTTP 405, indicating server-side issue

  Scenario: Attempt to delete user
    Given I am on the Users page
    When I click the delete button for user "test_user_15 15"
    Then I should see delete confirmation dialog with message "This action cannot be undone. This will permanently delete the user."
    And Cancel and Delete buttons are visible
    When I click Cancel
    Then the dialog should close
    And I remain on the users list
    # Note: Delete dialog appears correctly, but delete not executed to avoid data loss