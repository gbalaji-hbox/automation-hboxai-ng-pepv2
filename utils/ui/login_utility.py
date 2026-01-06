import re

from selenium.webdriver.remote.webdriver import WebDriver

from features.commons.routes import Routes
from features.pages.login_page.login_page import LoginPage
from utils.ui.config_reader import get_browser_config
from utils.ui.driver_manger import DriverRole, DriverManager
from utils.logger import printf


def perform_role_based_login(driver: WebDriver, user_role: str, session_name: str = "default",
                              auto_login: bool = True) -> bool:
    """Perform role-based login by wrapping the LoginPage.login_as_role method for backward compatibility."""

    if not auto_login:
        printf(f"[{session_name}] Auto-login disabled.")
        return False

    try:
        # Create LoginPage instance and use the original login_as_role method
        login_page = LoginPage(driver)

        # Check if already logged in by checking current URL
        dashboard_url = Routes.get_full_url(Routes.DASHBOARD)
        if driver.current_url == dashboard_url:
            printf(f"[{session_name}] Already logged in.")
            return True

        # Navigate to login page if not already there
        if driver.current_url != login_page.url:
            printf(f"[{session_name}] Navigating to login page...")
            login_page.navigate_to_login()

        # Use the original login_as_role method from LoginPage with retry and case handling
        printf(f"[{session_name}] Attempting login as {user_role}...")
        login_success = login_page.login_as_role(user_role)

        if login_success:
            printf(f"[{session_name}] Login successful as {user_role}.")
            return True
        else:
            printf(f"[{session_name}] Login failed as {user_role}.")
            return False

    except Exception as e:
        printf(f"[{session_name}] Login failed with exception: {e}")
        return False


def perform_role_based_login_with_driver(driver_manager, user_role: str, browser_name: str, context,
                                        session_name: str = "default", auto_login: bool = True, parallel_login = False) -> tuple:
    """Perform role-based login with automatic driver creation/management for the specified role."""

    # Map user role to DriverRole enum
    role_mapping = {
        'vpe_admin': DriverRole.VPE_ADMIN,
        'cs_admin': DriverRole.CS_ADMIN,
        'pes_admin': DriverRole.PES_ADMIN,
        'vpe_user': DriverRole.VPE_USER,
        'cs_user': DriverRole.CS_USER,
        'pes_user': DriverRole.PES_USER
    }
    driver_role = role_mapping.get(user_role, DriverRole.DEFAULT)

    printf(f"[{session_name}] Creating/getting driver for role: {driver_role.value}")

    if parallel_login:
        if not hasattr(context, "user_drivers"):
            context.user_drivers = {}
            printf(f"[{session_name}] Initialized context.user_drivers for parallel login")

        if user_role in context.user_drivers:
            driver = context.user_drivers[user_role]
            printf(f"[{session_name}] Reusing existing driver for {user_role} in parallel login")
        else:
            driver = driver_manager.create_driver(browser_name, session_name, context, role=driver_role)
            context.user_drivers[user_role] = driver
            printf(f"[{session_name}] Created new driver for {user_role} in parallel login")
    else:
        # Get existing driver for this role, or create a new one
        existing_driver = driver_manager.get_driver(driver_role)
        if existing_driver:
            printf(f"[{session_name}] Reusing existing driver for role: {driver_role.value}")
            driver = existing_driver
        else:
            printf(f"[{session_name}] Creating new driver for role: {driver_role.value}")
            driver = driver_manager.create_driver(browser_name, session_name, context, role=driver_role)

    # Perform login using the driver
    login_success = perform_role_based_login(driver, user_role, session_name, auto_login)

    return driver, login_success, driver_role


class LoginHelper:
    """Helper class for handling automatic login in Behave tests."""

    @staticmethod
    def extract_role_from_tags(tags):
        """Extract user role from login tags in feature file."""
        login_tag_pattern = re.compile(r'^login_(\w+)$')

        for tag in tags:
            match = login_tag_pattern.match(tag)
            if match:
                return match.group(1)

        return None

    @staticmethod
    def get_driver_for_role(context, user_role):
        """
        Return the driver for a role, create if it does not exist.
        Also updates context.active_step_driver for screenshot handling.
        """
        driver_manager: DriverManager = context.driver_manager
        browser_name = get_browser_config()
        session_name = f"{user_role}_session"
        # Reuse driver if already exists
        if not hasattr(context, "user_drivers"):
            context.user_drivers = {}
            printf("Initialized context.user_drivers for parallel login")

        if user_role in context.user_drivers:
            driver = context.user_drivers[user_role]
            printf(f"Reusing existing driver for {user_role} in parallel login")
        else:
            driver = driver_manager.create_driver(browser_name, session_name, context, role=user_role)
            context.user_drivers[user_role] = driver
            printf(f"[{session_name}] Created new driver for {user_role} in parallel login")

        # Update context for current step
        context.active_step_driver = driver
        context.driver = driver
        context.current_driver = driver

        return driver

    @staticmethod
    def handle_automatic_login(context, feature):
        """Handle automatic login for features with login tags using role-based driver management."""

        if not hasattr(feature, 'tags'):
            printf("Feature has no tags, skipping automatic login.")
            return

        # Skip automatic login for login_page.feature since it's testing login functionality
        feature_file_name = feature.filename.lower() if hasattr(feature, 'filename') else ""
        is_login_feature = "login_page.feature" in feature_file_name or "login_page/login_page.feature" in feature_file_name

        if is_login_feature:
            printf(f"Skipping automatic login for login feature: {feature.name}")

        user_role = LoginHelper.extract_role_from_tags(feature.tags)
        printf(f"Extracted user role from tags: {user_role}")

        if user_role != "parallel":
            printf(f"Feature '{feature.name}' has a login tag for role: {user_role}")
            try:
                # Get browser configuration
                browser_name = get_browser_config()

                # Use the role-based login function that handles driver creation internally
                driver, login_success, driver_role = perform_role_based_login_with_driver(
                    driver_manager=context.driver_manager,
                    user_role=user_role,
                    browser_name=browser_name,
                    context=context,
                    session_name=f"feature_{feature.name}",
                    auto_login=True,
                    parallel_login=False
                )

                # Update context with the role-based driver
                context.current_driver = driver
                context.driver = driver  # Keep context.driver for compatibility
                context.current_driver_role = driver_role

                if login_success:
                    printf(f"Successfully logged in as {user_role} for feature: {feature.name}")
                else:
                    printf(f"Login as {user_role} was not successful for feature: {feature.name}")
            except Exception as e:
                printf(f"Error during automatic login for role {user_role}: {e}")
        elif user_role == "parallel":
            printf(f"Feature '{feature.name}' has a 'parallel' login tag, skipping automatic login.")
            if not hasattr(context, 'user_drivers'):
                context.user_drivers = {}
                printf("Initialized context.user_drivers for parallel login feature")
        else:
            printf(f"Feature '{feature.name}' does not have a login tag, creating default driver.")
            try:
                # Get browser configuration
                browser_name = get_browser_config()

                default_driver = context.driver_manager.create_driver(browser_name, feature.name, context, role=DriverRole.DEFAULT)

                # Update context with the default driver
                context.current_driver = default_driver
                context.driver = default_driver  # Keep context.driver for compatibility
                context.current_driver_role = DriverRole.DEFAULT

                printf(f"Created default driver for feature: {feature.name}")
            except Exception as e:
                printf(f"Error creating default driver for feature {feature.name}: {e}")