import os
import platform
import requests
import zipfile

from utils.logger import printf
from utils.ui.config_reader import get_browser_config


def download_chromedriver():
    """Downloads ChromeDriver if not present in the driver's directory."""
    drivers_dir = "drivers"
    if not os.path.exists(drivers_dir):
        os.makedirs(drivers_dir)


    browser = get_browser_config()

    if browser.lower() != "chrome":
        printf("ChromeDriver download is only supported for Chrome browser.")
        return None

    chromedriver_filename = "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
    chromedriver_dirname = "chromedriver-win64" if platform.system() == "Windows" else "chromedriver-linux64"
    chromedriver_path = os.path.join(drivers_dir, chromedriver_dirname, chromedriver_filename)

    if os.path.exists(chromedriver_path):
        printf("ChromeDriver already exists.")
        return chromedriver_path

    chromedriver_version = get_chromedriver_version()
    printf("Downloading ChromeDriver...")
    chromedriver_url = get_chromedriver_url(chromedriver_version)
    if not chromedriver_url:
        printf("Could not determine ChromeDriver download URL.")
        return None

    try:
        response = requests.get(chromedriver_url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        zip_filepath = os.path.join(drivers_dir, "chromedriver.zip")
        with open(zip_filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract the zip file
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(drivers_dir)

        os.remove(zip_filepath)

        # Check if the extracted directory exists
        extracted_dir = os.path.join(drivers_dir, chromedriver_dirname)
        if not os.path.exists(extracted_dir):
            printf(f"Error: Extracted directory '{extracted_dir}' not found.")
            return None

        if platform.system() != "Windows":
            try:
                os.chmod(chromedriver_path, 0o755)
                printf(f"Set executable permission for {chromedriver_path}")
            except Exception as e:
                printf(f"Failed to set executable permission: {e}")
                return None

        # Ensure the chromedriver executable is in the extracted directory
        if not os.path.exists(chromedriver_path):
            printf(f"Error: ChromeDriver executable '{chromedriver_path}' not found.")
            return None

        printf("ChromeDriver downloaded and extracted successfully.")
        return chromedriver_path

    except requests.exceptions.RequestException as e:
        printf(f"Error downloading ChromeDriver: {e}")
        return None
    except zipfile.BadZipFile as e:
        printf(f"Error extracting ChromeDriver: {e}")
        return None


def get_chromedriver_version():
    try:
        url = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE"
        response = requests.get(url)
        response.raise_for_status()
        chromedriver_version = response.text.strip()
        printf(f"ChromeDriver version found: {chromedriver_version}")
        return chromedriver_version
    except requests.exceptions.RequestException as e:
        printf(f"Error getting ChromeDriver version: {e}")
        return None


def get_chromedriver_url(chromedriver_version):
    """Gets the ChromeDriver download URL."""
    os_name = platform.system()
    if os_name == "Windows":
        chromedriver_filename = "win64/chromedriver-win64.zip"
    elif os_name == "Darwin":
        chromedriver_filename = "mac-x64/chromedriver-mac-x64.zip"
    elif os_name == "Linux":
        chromedriver_filename = "linux64/chromedriver-linux64.zip"
    else:
        return None

    return f"https://storage.googleapis.com/chrome-for-testing-public/{chromedriver_version}/{chromedriver_filename}"


def set_driver_path():
    """Downloads ChromeDriver and returns the path."""
    chromedriver_path = download_chromedriver()
    if chromedriver_path:
        printf(f"ChromeDriver path set: {chromedriver_path}")
        return chromedriver_path
    else:
        printf("ChromeDriver download or configuration failed.")
        return None


def setup_chromedriver(context):
    driver_path = set_driver_path()
    if driver_path:
        printf("ChromeDriver is ready to use.")
        return driver_path
    else:
        printf("ChromeDriver setup failed.")
        return None

if __name__ == '__main__':
    driver_path = set_driver_path()
    if driver_path:
        printf("ChromeDriver is ready to use.")
    else:
        printf("ChromeDriver setup failed.")