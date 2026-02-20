# python
from enum import Enum
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from utils.ui.webdriver_helper import WebDriverHelper
from utils.logger import printf
from utils.ui.config_reader import get_driver_mode, get_execution_mode


class DriverRole(Enum):
    DEFAULT = "default"
    VPE_ADMIN = "vpe_admin"
    CS_ADMIN = "cs_admin"
    PES_ADMIN = "pes_admin"
    VPE_USER = "vpe_user"
    CS_USER = "cs_user"
    PES_USER = "pes_user"
    ENROLLER_ADMIN = "enroller_admin"


class DriverManager:
    def __init__(self):
        self.drivers = {}
        self.execution_mode = get_execution_mode()
        self.driver_mode = get_driver_mode()

    def create_driver(self, browser_name, session_name, context, role=DriverRole.DEFAULT, selenoid_url=None):
        """
        Create and add a driver for the specified browser and role.
        Uses smart detection based on execution_mode and driver_mode.
        """
        printf(f"Execution Mode: {self.execution_mode}, Driver Mode: {self.driver_mode}")

        if self.driver_mode == 'remote':
            driver, temp_dir = WebDriverHelper.create_remote_driver(browser_name, session_name, context, selenoid_url)
            printf(f"Created remote driver for {browser_name} via Selenoid")
        else:
            # Only download ChromeDriver if we're in local execution mode and need local driver
            if self.execution_mode == 'local':
                WebDriverHelper.setup_webdriver(context)
                driver, temp_dir = WebDriverHelper.create_driver(browser_name, context)
                printf(f"Created local driver for {browser_name}")
            else:
                # CI/CD with local driver - try remote first, fallback to local
                try:
                    driver, temp_dir = WebDriverHelper.create_remote_driver(browser_name, session_name, context,
                                                                            selenoid_url)
                    printf(f"Created remote driver for {browser_name} via Selenoid (CI/CD)")
                except Exception as e:
                    printf(f"Remote driver failed, falling back to local: {e}")
                    driver, temp_dir = WebDriverHelper.create_driver(browser_name, context)
                    printf(f"Created local driver for {browser_name} (CI/CD fallback)")

        self.add_driver(role, driver)
        if temp_dir:
            # Store temp_dir for cleanup, but since quit_driver handles it, maybe not needed
            pass
        return driver

    def create_remote_driver(self, browser_name, context, role=DriverRole.DEFAULT, selenoid_url=None):
        """
        Create and add a remote driver for Selenoid for the specified browser and role.

        Args:
            browser_name: Browser name (chrome, firefox, edge)
            context: Behave context object
            role: Driver role (enum or string)
            selenoid_url: Optional Selenoid URL override
        """
        driver, temp_dir = WebDriverHelper.create_remote_driver(browser_name, context, selenoid_url)
        self.add_driver(role, driver)
        printf(f"Created remote Selenoid driver for {browser_name} with role {role.value}")
        return driver

    def add_driver(self, role, driver):
        if isinstance(role, DriverRole):
            role = role.value
        if not isinstance(driver, RemoteWebDriver):
            raise TypeError("The provided 'driver' is not a valid WebDriver instance.")
        if role in self.drivers:
            printf(f"Warning: Driver for role '{role}' already exists. Overwriting.")
            self.quit_driver(role)
        self.drivers[role] = driver
        printf(f"Driver added for role: '{role}'.")

    def get_driver(self, role):
        if isinstance(role, DriverRole):
            role = role.value
        return self.drivers.get(role)

    def quit_driver(self, role):
        if isinstance(role, DriverRole):
            role = role.value
        driver = self.drivers.get(role)
        if driver is not None:
            try:
                if driver.session_id:
                    driver.quit()
                    printf(f"Driver for role '{role}' has been quit.")
                else:
                    printf(f"Driver for role '{role}' was already quit.")
            except Exception as e:
                printf(f"Error quitting driver for role '{role}': {e}")
            self.drivers.pop(role, None)
        else:
            printf(f"No driver found for role '{role}' to quit.")

    def quit_all_drivers(self):
        roles_to_quit = list(self.drivers.keys())
        if not roles_to_quit:
            printf("No active drivers to quit.")
            return

        printf(f"Quitting all {len(roles_to_quit)} active drivers...")
        for role in roles_to_quit:
            self.quit_driver(role)
        printf("All drivers have been quit.")