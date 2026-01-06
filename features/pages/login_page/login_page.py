from time import sleep
from utils.logger import printf

from features.commons.routes import Routes
from features.pages.base_page import BasePage
from features.commons.locators import LoginPageLocators
from selenium.common.exceptions import TimeoutException
from utils.ui.config_reader import read_configuration, get_browser_config
from utils.ui.driver_manger import DriverRole


class LoginPage(BasePage):
    """Page Object for the Login page."""

    def __init__(self, driver):
        super().__init__(driver)
        self.url = Routes.get_full_url(Routes.LOGIN)

    def navigate_to_login(self):
        """Navigate to the login_page page."""
        self.driver.get(self.url)

    def enter_email(self, email):
        """Enter email in the email input field."""
        self.send_keys(LoginPageLocators.EMAIL_INPUT, email)

    def enter_password(self, password):
        """Enter password in the password input field."""
        self.send_keys(LoginPageLocators.PASSWORD_INPUT, password)

    def click_submit(self):
        """Click the submit button."""
        self.click(LoginPageLocators.SUBMIT_BUTTON)
        sleep(2)

    def click_sign_out(self):
        """Click the sign-out button."""
        self.click(LoginPageLocators.SIGN_OUT_BUTTON)
        sleep(2)
        self.click(LoginPageLocators.LOG_OUT_CONFIRM_BUTTON)

    def is_login_successful(self):
        """Verify if login_page was successful by checking for header logo."""
        try:
            return self.is_element_visible(LoginPageLocators.HEADER_LOGO)
        except TimeoutException:
            return False

    def is_error_message_displayed(self):
        """Check if error message is displayed."""
        try:
            return self.is_element_visible(LoginPageLocators.ERROR_MESSAGE)
        except TimeoutException:
            return False

    def is_password_error_displayed(self):
        """Check if password error message is displayed."""
        try:
            return self.is_element_visible(LoginPageLocators.PASSWORD_ERROR_MESSAGE)
        except TimeoutException:
            return False

    def is_logged_out(self):
        """Check if user is logged out by verifying presence of login button."""
        try:
            return self.is_element_visible(LoginPageLocators.SUBMIT_BUTTON)
        except TimeoutException:
            return False

    def login(self, email, password):
        """Perform login with given credentials."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_submit()
        sleep(1)
        self.check_url_changes(self.url)

    @classmethod
    def get_credentials_for_role(cls, user_role):
        """
        Get credentials for a specific user role from the config file.

        Args:
            user_role: Role of the user (e.g., 'doctor', 'nurse', 'care_coach')

        Returns:
            tuple: (username, password) for the specified role
        """
        config_username_key = f"{user_role}_user_name"
        try:
            username = read_configuration("Credentials", config_username_key)
            password = read_configuration("Credentials", f"common_{Routes.get_env()}_password")
            return username, password
        except KeyError:
            error_msg = (f"Username for user type '{user_role}' (key '{config_username_key}') "
                         f"not found in [Credentials] section of config.ini. "
                         f"Please ensure '{config_username_key}' is defined.")
            printf(error_msg)
            raise ValueError(error_msg)

    @staticmethod
    def get_driver_for_role(context, user_role):
        """
        Return a driver for a given role in parallel login features.
        Lazily creates and stores driver in context.user_drivers.
        """
        if not hasattr(context, "user_drivers"):
            context.user_drivers = {}

        if user_role in context.user_drivers:
            driver = context.user_drivers[user_role]
            printf(f"Reusing existing driver for {user_role}")
        else:
            browser_name = get_browser_config()
            driver = context.driver_manager.create_driver(
                browser_name,
                f"{user_role}_session",
                context,
                role=DriverRole.DEFAULT
            )
            context.user_drivers[user_role] = driver
            printf(f"Created new driver for {user_role}")

        return driver

    def login_as_role(self, user_role, max_retries=3):
        """
        Login using credentials for a specific user role with retry mechanism.

        Args:
            user_role: Role of the user (e.g., 'doctor', 'nurse', 'care_coach')
            max_retries: Maximum number of login attempts (default: 3)

        Returns:
            bool: True if login was successful, False otherwise
        """
        printf(f"Attempting to log in as {user_role}...")
        username, password = self.get_credentials_for_role(user_role)
        printf(f"Resolved username from config for '{user_role}': {username}")

        for attempt in range(max_retries):
            printf(f"Login attempt {attempt + 1}/{max_retries}")

            try:
                self.login(username, password)

                # Verify login was successful
                login_success = self.is_login_successful()
                if login_success:
                    printf(f"✅ Login as {user_role} successful on attempt {attempt + 1}")
                    return True
                else:
                    printf(f"❌ Login attempt {attempt + 1} failed - login not successful")
                    if attempt < max_retries - 1:  # Don't navigate on last attempt
                        printf("🔄 Retrying login...")
                        self.navigate_to_login()  # Navigate back to login page for retry

            except Exception as e:
                printf(f"❌ Login attempt {attempt + 1} failed with exception: {e}")
                if attempt < max_retries - 1:  # Don't navigate on last attempt
                    printf("🔄 Retrying login after exception...")
                    try:
                        self.navigate_to_login()  # Navigate back to login page for retry
                    except Exception as nav_e:
                        printf(f"❌ Failed to navigate to login page: {nav_e}")

        printf(f"❌ All {max_retries} login attempts failed for {user_role}")
        return False