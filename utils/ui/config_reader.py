from configparser import ConfigParser
import os


def read_configuration(category, key):
    config = ConfigParser()
    config.read("configuration/config.ini")
    return config.get(category, key)


def is_allure_enabled():
    """Check if Allure reporting is enabled via environment variable"""
    return os.getenv('DISABLE_ALLURE_REPORTS', 'false').lower() != 'true'


def get_ci_environment():
    """Get the CI environment type"""
    return os.getenv('CI_ENVIRONMENT', 'stg')


def is_headless_mode():
    """Check if browser should run in headless mode"""
    return os.getenv('HEADLESS_MODE', 'false').lower() == 'true'


def get_base_url(environment):
    """Get base URL for the specified environment"""
    env_section = f"{environment}_env"
    try:
        return read_configuration(env_section, "url")
    except KeyError:
        printf(f"Warning: URL for environment '{environment}' not found in config.ini. Falling back to a default.")
        return "https://ngpep-sandbox.hbox.ai/"


def get_browser_config():
    """Get browser configuration from environment variable or config file"""
    return os.getenv('BROWSER', read_configuration("basic info", "browser") or "chrome").lower()


def get_driver_mode():
    """
    Detect if should use local or remote WebDriver.
    Priority: env var > config > default
    Returns: 'local' or 'remote'
    """
    # 1. Check environment variable first
    driver_setup = os.getenv('DRIVER_MODE', '').lower()
    if driver_setup in ['local', 'remote']:
        return driver_setup

    # 2. Check configuration
    try:
        driver_setup = read_configuration("Execution Environment", "driver_mode")
        if driver_setup in ['local', 'remote']:
            return driver_setup
    except Exception as e:
        printf(f"Error reading driver_mode from config: {e}")
        return 'local'


def get_execution_mode():
    """
    Detect if running in local development or CI/CD environment.
    Returns: 'local' or 'remote'
    """
    try:
        # Check for CI/CD environment variables
        execution_setup = is_running_in_pipeline()
        if execution_setup:
            return 'remote'
        try:
            execution_setup = read_configuration("Execution Environment", "execution_mode")
            if execution_setup in ['local', 'remote']:
                return execution_setup
        except Exception as e:
            printf(f"Error reading execution_mode from config: {e}")
    except Exception as e:
        printf(f"Error detecting execution mode: {e}")
        return 'local'


def is_running_in_pipeline():
    """Check if running in a CI/CD pipeline based on common environment variables"""
    ci_indicators = ['CI', 'JENKINS_URL', 'BUILD_NUMBER', 'GITHUB_ACTIONS', 'GITLAB_CI', 'BITBUCKET_BUILD_NUMBER',
                     'TRAVIS', 'GITHUB_ACTIONS', 'JENKINS_HOME']
    return any(os.getenv(indicator) for indicator in ci_indicators)

def get_selenoid_url():
    """Determine the correct Selenoid URL based on environment"""
    return os.getenv('SELENOID_URL',
                     read_configuration("Selenoid", "selenoid_url") or 'http://localhost:4444/wd/hub')


def get_log_to_file():
    """Check if logging to file is enabled"""
    try:
        return read_configuration("Logging", "log_to_file").lower() == 'true'
    except Exception as e:
        printf(f"Error reading log_to_file from config: {e}")
        return False


def get_log_file_path():
    """Get the log file path"""
    try:
        return read_configuration("Logging", "log_file_path")
    except Exception as e:
        printf(f"Error reading log_file_path from config: {e}")
        return "logs/automation.log"


def get_log_to_console():
    """Check if logging to console is enabled"""
    try:
        return read_configuration("Logging", "log_to_console").lower() == 'true'
    except Exception as e:
        printf(f"Error reading log_to_console from config: {e}")
        return True