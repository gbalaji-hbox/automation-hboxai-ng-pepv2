from behave import when, then

from features.pages.search_patients_page.search_patients_page import SearchPatientsPage


@when(u'I extract first patient data from results table')
def step_impl(context):
    context.search_patients_page = SearchPatientsPage(context.driver)
    context.first_patient_data = context.search_patients_page.extract_first_patient_data()
    if not context.first_patient_data:
        raise AssertionError("Failed to extract first patient data from the results table.")


@when(u'perform search using "{field}" with extracted value')
def step_impl(context, field):
    if not hasattr(context, 'first_patient_data') or not context.first_patient_data:
        context.first_patient_data = context.search_patients_page.extract_first_patient_data()

    context.search_field = field
    context.search_value = context.first_patient_data.get(field)

    result = context.search_patients_page.perform_search_by_field(field, context.search_value)
    if not result:
        raise AssertionError(f"Failed to perform patient search for field: '{field}'")


@then(u'search results should contain the matching patient data')
def step_impl(context):
    if not hasattr(context, 'search_field') or not hasattr(context, 'search_value'):
        raise AssertionError("Search field and value not set. Run the search step first.")

    assert context.search_patients_page.verify_search_results_contain_patient_data(
        context.search_field,
        context.search_value,
    ), f"Search results do not contain matching data for '{context.search_field}': '{context.search_value}'"


@when(u'I am searching for "{term}"')
def step_impl(context, term):
    context.search_patients_page = SearchPatientsPage(context.driver)
    result = context.search_patients_page.search_for_term(term)
    if not result:
        raise AssertionError(f"Failed to submit search for term: '{term}'")


@then(u'system displays "{message}" message')
def step_impl(context, message):
    assert context.search_patients_page.is_no_results_message_displayed(), \
        f"Expected '{message}' message to be displayed but it was not found."


@when(u'I click "Reset" button')
def step_impl(context):
    context.search_patients_page.click_reset_button()


@then(u'search input field is cleared and all patients are displayed')
def step_impl(context):
    assert context.search_patients_page.is_search_cleared_and_results_displayed(), \
        "Search input was not cleared or no patients are displayed after clicking Reset."


@when(u'I am changing rows per page to "{rows_per_page}"')
def step_impl(context, rows_per_page):
    context.search_patients_page = SearchPatientsPage(context.driver)
    context.search_patients_page.navigate_to_search_patients()
    context.search_patients_page.select_rows_per_page(rows_per_page)


@then(u'pagination shows "{rows_per_page}" results per page')
def step_impl(context, rows_per_page):
    assert context.search_patients_page.verify_rows_per_page(rows_per_page), \
        f"Pagination did not show '{rows_per_page}' results per page."


@when(u'I click "View details" for any patient')
def step_impl(context):
    context.search_patients_page = SearchPatientsPage(context.driver)
    context.search_patients_page.navigate_to_search_patients()
    context.search_patients_page.click_view_details_for_first_patient()


@then(u'patient details page loads correctly')
def step_impl(context):
    assert context.search_patients_page.is_patient_details_page_loaded(), \
        "Patient details page did not load correctly after clicking View Details."


@when(u'I click "Back" button')
def step_impl(context):
    context.search_patients_page.click_back_button()


@then(u'returns to search results page')
def step_impl(context):
    assert context.search_patients_page.is_back_on_search_patients_page(), \
        "Did not return to the Search Patients page after clicking Back."
