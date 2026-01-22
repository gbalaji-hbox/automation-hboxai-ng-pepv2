from behave import given, when, then

from features.pages.program_type_page.program_page import ProgramPage


@given(u'I am on the {tab_name} tab from program type')
def step_impl(context, tab_name):
    context.program_page = ProgramPage(context.driver)
    context.program_page.navigate_to_tab(tab_name)


@when(u'I fetch the first row data from the programs table')
def step_impl(context):
    raise StepNotImplementedError(u'When I fetch the first row data from the programs table')


@when(u'I select Program Name option and enter the fetched data in the search box')
def step_impl(context):
    raise StepNotImplementedError(u'When I select Program Name option and enter the fetched data in the search box')


@then(u'the Program table should show matching results')
def step_impl(context):
    raise StepNotImplementedError(u'Then the Program table should show matching results')
