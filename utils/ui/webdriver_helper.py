import os
import tempfile
import time
import requests
from utils.logger import printf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utils.ui.config_reader import is_headless_mode, is_running_in_pipeline, read_configuration, get_browser_config, \
    get_selenoid_url
from utils.ui.chromedriver_setup import setup_chromedriver


class WebDriverHelper:

    WINDOW_SIZE_ARG = "--window-size=1920,1080"

    @staticmethod
    def create_driver(browser_name, context):
        """Create a local WebDriver (Chrome, Firefox, Edge)"""
        browser_name = browser_name.lower()
        temp_user_data_dir = None

        if browser_name == "chrome":
            options = ChromeOptions()
            temp_user_data_dir = tempfile.mkdtemp()

            prefs = {
                "profile.default_content_setting_values.notifications": 1,
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.geolocation": 1,
                "profile.default_content_setting_values.media_stream": 1
            }

            options.add_experimental_option("prefs", prefs)
            options.add_argument(f"--user-data-dir={temp_user_data_dir}")
            options.add_argument("--disable-gpu")
            options.add_argument(WebDriverHelper.WINDOW_SIZE_ARG)
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-logging")
            options.add_argument("--log-level=3")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

            if is_headless_mode():
                options.add_argument("--headless=new")
                printf("Running Chrome in headless mode")

            if os.getenv('USE_SYSTEM_CHROMEDRIVER') or is_running_in_pipeline():
                driver = webdriver.Chrome(options=options)
            else:
                if hasattr(context, 'chromedriver_path') and context.chromedriver_path:
                    service = ChromeService(executable_path=context.chromedriver_path)
                    driver = webdriver.Chrome(service=service, options=options)
                else:
                    driver = webdriver.Chrome(options=options)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            driver = webdriver.Firefox(options=options)

        else:  # Edge
            options = EdgeOptions()
            options.add_argument("headless")
            options.add_argument("disable-gpu")
            options.add_argument(WebDriverHelper.WINDOW_SIZE_ARG)
            driver = webdriver.Edge(options=options)

        driver.implicitly_wait(10)
        if not is_headless_mode():
            driver.maximize_window()

        return driver, temp_user_data_dir

    @staticmethod
    def wait_for_selenoid_ready(selenoid_url, timeout=30):
        """Wait until Selenoid is ready before creating a session"""
        for _ in range(timeout):
            try:
                r = requests.get(f"{selenoid_url.replace('/wd/hub', '')}/status")
                if r.status_code == 200:
                    status = r.json()
                    if status.get("total", 0) > 0:
                        printf("Selenoid is ready")
                        return True
            except Exception as e:
                printf("Error checking Selenoid status:", e)
            time.sleep(1)
        raise ConnectionError("Selenoid did not become ready in time")

    @staticmethod
    def create_remote_driver(browser_name, session_name, context, selenoid_url=None):
        """Create a remote WebDriver for Selenoid using dynamic config capabilities"""
        browser_name = browser_name.lower()

        if not selenoid_url:
            selenoid_url = get_selenoid_url()

        printf(f"Creating remote driver for {browser_name} connecting to: {selenoid_url}")
        WebDriverHelper.wait_for_selenoid_ready(selenoid_url)

        # Read capabilities dynamically from config.ini
        enable_vnc = read_configuration("Selenoid", "enable_vnc").lower() in ("true", "1", "yes")
        enable_video = read_configuration("Selenoid", "enable_video").lower() in ("true", "1", "yes")
        enable_log = read_configuration("Selenoid", "enable_log").lower() in ("true", "1", "yes")
        session_timeout = read_configuration("Selenoid", "session_timeout") or "300s"

        # Setup browser options
        if browser_name == "chrome":
            options = ChromeOptions()
            if is_headless_mode():
                options.add_argument("--headless=new")
                printf("Running Chrome in headless mode")

            options.add_argument("--disable-gpu")
            options.add_argument(WebDriverHelper.WINDOW_SIZE_ARG)
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-logging")
            options.add_argument("--log-level=3")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            prefs = {
                "profile.default_content_setting_values.notifications": 1,
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.geolocation": 1,
                "profile.default_content_setting_values.media_stream": 1
            }
            options.add_experimental_option("prefs", prefs)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        else:  # Edge
            options = EdgeOptions()
            options.add_argument("--disable-gpu")
            options.add_argument(WebDriverHelper.WINDOW_SIZE_ARG)

        # Apply dynamic Selenoid capabilities
        options.set_capability('selenoid:options', {
            'enableVNC': enable_vnc,
            'enableVideo': enable_video,
            'enableLog': enable_log,
            'logName': f'{browser_name}.container.logs',
            'name': f'Automated test - {session_name}',
            'sessionTimeout': session_timeout
        })

        # Retry loop for robustness with session timeout handling
        driver = None
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts and not driver:
            try:
                driver = webdriver.Remote(command_executor=selenoid_url, options=options)
                driver.implicitly_wait(10)
                printf(f"Successfully created remote {browser_name} driver via Selenoid")
                break
            except Exception as e:
                error_msg = str(e).lower()
                attempt += 1

                # Handle session expired/reuse errors specifically
                if ("session expired" in error_msg or "session not found" in error_msg or
                    "invalid session id" in error_msg) and attempt < max_attempts:
                    printf(f"Session reuse issue detected, retrying with unique session name...")
                    # Add timestamp to make session name unique and force new session creation
                    options.set_capability('selenoid:options', {
                        'enableVNC': enable_vnc,
                        'enableVideo': enable_video,
                        'enableLog': enable_log,
                        'logName': f'{browser_name}.container.logs',
                        'name': f'Automated test - {session_name} - {int(time.time())}',
                        'sessionTimeout': session_timeout
                    })
                    time.sleep(1)  # Brief pause before retry
                    continue

                # For other errors, log and retry normally
                if attempt < max_attempts:
                    printf(f"Attempt {attempt} failed to create remote driver, retrying: {e}")
                    time.sleep(2)
                else:
                    printf(f"All {max_attempts} attempts failed to create remote driver: {e}")

        if not driver:
            raise ConnectionError(f"Failed to create remote driver for {browser_name} after {max_attempts} attempts")

        return driver, None  # No temp dir for remote drivers

    @staticmethod
    def setup_webdriver(context):
        """Setup ChromeDriver path for local execution"""
        browser_name = get_browser_config()
        if browser_name == "chrome":
            context.chromedriver_path = setup_chromedriver(context)
            if context.chromedriver_path:
                printf(f"ChromeDriver set up successfully at: {context.chromedriver_path}")
            else:
                printf("ChromeDriver setup failed. Will try to use default path.")
        else:
            context.chromedriver_path = None
            printf(f"Using {browser_name} browser - no special driver setup required.")