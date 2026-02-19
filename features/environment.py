import traceback

from features.commons.routes import Routes
from utils.logger import printf
from utils.ui.allure_helper import AllureHelper
from utils.ui.config_reader import read_configuration
from utils.ui.driver_manger import DriverManager
from utils.ui.driver_manger import DriverRole
from utils.ui.login_utility import LoginHelper
from utils.ui.popup_handler import PopupHandler


def before_all(context):
    # Setup Allure folders
    AllureHelper.setup_allure_folders()

    # Initialize DriverManager once for the entire test run
    context.driver_manager = DriverManager()
    printf("DriverManager initialized.")

    # Setup environment configuration
    context.environment = context.config.userdata.get("env", "stg").lower()
    env_section = f"{context.environment}_env"

    try:
        context.base_url = read_configuration(env_section, "url")
        printf(f"Tests will run against {context.environment} environment: {context.base_url}")
    except KeyError:
        printf(f"Warning: URL for environment '{context.environment}' not found in config.ini. "
               "Falling back to a default or raising an error.")
        context.base_url = "https://ngpepv2-sandbox.hbox.ai/"

    Routes.set_base_url(context.base_url, context.environment)
    printf("Routes module's base URL set dynamically.")


def before_feature(context, feature):
    """Initialize browser and login before each feature except the login feature, only if not already logged in."""

    # Handle automatic login for features with login tags (this now handles driver creation internally)
    LoginHelper.handle_automatic_login(context, feature)

    PopupHandler.inject_appointment_reminder_killer(context.driver)

    # Assign Allure suite for the feature
    AllureHelper.assign_feature_suite(context, feature)

    # Assign Allure suites for scenarios in this feature
    AllureHelper.assign_scenario_tags_for_feature(context, feature)


# Scenario hook not needed - tags assigned in before_feature


def after_feature(context, feature):
    printf(f"Finished feature: {feature.name}, closing browser.")
    if hasattr(context, 'driver_manager') and hasattr(context, 'current_driver_role'):
        context.driver_manager.quit_driver(context.current_driver_role)
    elif hasattr(context, 'driver_manager') and hasattr(context, 'user_drivers'):
        for role, driver in context.user_drivers.items():
            context.driver_manager.quit_driver(role)
        context.user_drivers.clear()
    elif hasattr(context, 'driver_manager'):
        # Fallback to default if no specific role was set
        context.driver_manager.quit_driver(DriverRole.DEFAULT)


def after_step(context, step):
    if step.status == 'failed':
        # Use hasattr to safely check if the attribute exists
        if hasattr(context, 'active_step_driver') and context.active_step_driver:
            driver_to_screenshot = context.active_step_driver
        else:
            driver_to_screenshot = context.driver

        AllureHelper.attach_failure(driver_to_screenshot, step)


def after_all(context):
    """Cleanup after all tests complete"""

    try:
        # Ensure all drivers are quit at the very end
        if hasattr(context, 'driver_manager'):
            context.driver_manager.quit_all_drivers()
            printf("All drivers managed by DriverManager have been closed.")
    except Exception as e:
        printf(f"Error during final driver cleanup: {e}")
        traceback.print_exc()

    # Accumulate results and generate cumulative report
    AllureHelper.accumulate_results()
    AllureHelper.generate_cumulative_report()
