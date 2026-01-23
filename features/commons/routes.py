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
