@login_vpe_internal
Feature: tc28 - Patient Search Dynamic validation

  @regression
  Scenario Outline: Dynamic search validation using extracted data
    Given I am on the Search Patients page
    When I extract first patient data from results table
    And perform search using "<field>" with extracted value
    Then search results should contain the matching patient data

    Examples:
      | field         |
      | Full Name     |
      | DOB           |
      | Mobile Number |
      | Home Number   |
      | Email         |
      | Clinic Name   |
      | EMR           |

  @negative
  Scenario: Non-existent search negative testing
    Given I am on the Search Patients page
    When I am searching for "NonExistentSearch123"
    Then system displays "No results found" message
    When I click "Reset" button
    Then search input field is cleared and all patients are displayed

  @smoke @allure.label.severity:minor
  Scenario Outline: Pagination validation with different row counts
    Given I am on the Search Patients page
    When I am changing rows per page to "<rows_per_page>"
    Then pagination shows "<rows_per_page>" results per page

    Examples:
      | rows_per_page |
      | 25            |
      | 50            |

  @smoke @allure.label.severity:minor
  Scenario: Patient details navigation
    Given I am on the Search Patients page
    When I click "View details" for any patient
    Then patient details page loads correctly
    When I click "Back" button
    Then returns to search results page