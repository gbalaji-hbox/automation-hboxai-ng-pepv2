Feature: tc00 - Login Functionality Verification

  As a user
  I want to be able to log in to the application
  So that I can access my account

  @smoke
  Scenario: Successful login with valid credentials
    Given I navigate to the Login page
    When I enter valid email and password
    And I click the Submit button
    Then I should be logged in successfully
    When I click on logout from dashboard header
    Then I should be logged out successfully

  @regression
  Scenario: Failed login with invalid credentials
    Given I navigate to the Login page
    When I enter invalid email and password
    And I click the Submit button
    Then I should see an error message

  @negative
  Scenario: Failed login with invalid password
    Given I navigate to the Login page
    When I enter invalid password
    And I click the Submit button
    Then I should see a password error message