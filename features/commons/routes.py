"""
Centralized route definitions for page navigation.
This file contains all URL paths used in the application for consistent navigation across page objects.
"""

BASE_URL = None
ENV = "stg"  # Default environment, can be overridden by environment.py


class Routes:
    """
    Class containing all route paths for the application.
    All page objects should use these constants for navigation instead of hardcoded paths.
    """

    def __init__(self, base_url):
        self._base_url = base_url
        Routes.set_base_url(base_url, ENV)

    SUPPORT_BOOKING = "https://hbox.setmore.com"

    # Route paths
    LOGIN = "/"
    DASHBOARD = "/admin/dashboard"
    USERS_PAGE = "/admin/users"
    EDIT_USER = "/admin/users/edit/"
    EDIT_GROUP = "/admin/users/groups/edit/"
    PROGRAM_TYPE = "/admin/program-type"
    PROGRAM_EDIT = "/admin/program-type/edit/"
    PATIENT_PROGRAM_STATUS_EDIT = "/admin/patient-program-status/edit/"
    WORKFLOW_TASKS = "/admin/workflow"
    WORKFLOW_EDIT = "/admin/workflow/edit/"
    WORKFLOW_STATUS_EDIT = "/admin/workflow-status/edit/"
    TASK_EDIT = "/admin/tasks/edit/"
    PATIENT_GROUPS = "/admin/patient-groups"
    EDIT_PATIENT_GROUP = "/admin/patient-groups/edit/"
    DUPLICATE_PATIENT_GROUP = "/admin/patient-groups/duplicate/"
    ARCHIVED_PATIENT_GROUPS = "/admin/patient-groups/archived"
    CREATE_NEW_PATIENT_GROUP_BY_EMRS = "/admin/patient-groups/create-by-emrs"
    CREATE_NEW_PATIENT_GROUP_BY_FILTERS = "/admin/patient-groups/create-by-filters"
    CREATE_NEW_PATIENT_GROUP_BY_EXCEL = "/admin/patient-groups/create-by-excel"
    ADD_PATIENTS_TO_GROUP = "/add-patients"
    FACILITY_AVAILABILITY = "/admin/facility-availability"
    ADD_FACILITY_AVAILABILITY = "/admin/facility-availability/add"
    FACILITY_AVAILABILITY_EDIT = "/admin/facility-availability/edit/"
    ACTIVITIES = "/admin/activity"
    ACTIVITY_ADD = "/admin/activity/add"
    ACTIVITY_EDIT = "/admin/activity/edit/"
    ACTIVITY_DUPLICATE = "/admin/activity/duplicate/"
    SEARCH_PATIENTS = "/global-search"
    PATIENT_DETAILS = "/es-dashboard"
    ADD_PATIENT = "/add-patient"
    USER_DASHBOARD= "/dashboard"


    @staticmethod
    def get_full_url(route_path):
        if BASE_URL is None:
            raise RuntimeError("Routes.BASE_URL has not been set by environment.py!")
        else:
            return BASE_URL + route_path

    @staticmethod
    def get_env():
        return ENV

    @staticmethod
    def set_base_url(base_url, env):
        global BASE_URL
        global ENV
        BASE_URL = base_url
        ENV = env
