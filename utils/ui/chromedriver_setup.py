import os
import platform
import re
import shutil
import subprocess
import requests
import zipfile

from utils.logger import printf
from utils.ui.config_reader import get_browser_config


def download_chromedriver():
    """Downloads a ChromeDriver version that matches the installed Chrome major version."""
    drivers_dir = "drivers"
    if not os.path.exists(drivers_dir):
        os.makedirs(drivers_dir)


    browser = get_browser_config()

    if browser.lower() != "chrome":
        printf("ChromeDriver download is only supported for Chrome browser.")
        return None

    chromedriver_filename = "chromedriver.exe" if platform.system() == "Windows" else "chromedriver"
    chromedriver_dirname = get_chromedriver_dirname()
    if not chromedriver_dirname:
        printf(f"Unsupported OS for ChromeDriver download: {platform.system()}")
        return None

    chromedriver_path = os.path.join(drivers_dir, chromedriver_dirname, chromedriver_filename)

    installed_chrome_version = get_installed_chrome_version()
    installed_chrome_major = get_major_version(installed_chrome_version)

    if installed_chrome_version:
        printf(f"Installed Chrome version detected: {installed_chrome_version}")
    else:
        printf("Could not detect installed Chrome version. Falling back to stable ChromeDriver.")

    if os.path.exists(chromedriver_path):
        existing_driver_version = get_existing_chromedriver_version(chromedriver_path)
        existing_driver_major = get_major_version(existing_driver_version)

        if installed_chrome_major and existing_driver_major == installed_chrome_major:
            printf(
                f"Existing ChromeDriver version {existing_driver_version} matches installed Chrome major "
                f"{installed_chrome_major}. Reusing it."
            )
            return chromedriver_path

        printf(
            "Existing ChromeDriver does not match installed Chrome major version. "
            "Downloading a compatible driver."
        )
        remove_existing_chromedriver(drivers_dir, chromedriver_dirname, chromedriver_path)

    chromedriver_version = get_chromedriver_version(installed_chrome_major)
    if not chromedriver_version:
        printf("Could not determine ChromeDriver version.")
        return None

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


def get_chromedriver_version(chrome_major=None):
    """Gets latest ChromeDriver version for a Chrome major version, with stable fallback."""
    try:
        if chrome_major:
            version_url = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{chrome_major}"
            response = requests.get(version_url, timeout=30)
            if response.ok and response.text.strip():
                chromedriver_version = response.text.strip()
                printf(
                    f"ChromeDriver version found for Chrome major {chrome_major}: {chromedriver_version}"
                )
                return chromedriver_version

            printf(
                f"No exact ChromeDriver release found for Chrome major {chrome_major}. "
                "Falling back to stable release."
            )

        stable_url = "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE"
        stable_response = requests.get(stable_url, timeout=30)
        stable_response.raise_for_status()
        chromedriver_version = stable_response.text.strip()
        printf(f"Stable ChromeDriver version found: {chromedriver_version}")
        return chromedriver_version
    except requests.exceptions.RequestException as e:
        printf(f"Error getting ChromeDriver version: {e}")
        return None


def get_installed_chrome_version():
    """Detects installed Chrome version across OSes."""
    os_name = platform.system()

    if os_name == "Windows":
        registry_paths = [
            r"HKLM\SOFTWARE\Google\Chrome\BLBeacon",
            r"HKCU\SOFTWARE\Google\Chrome\BLBeacon",
            r"HKLM\SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon",
        ]

        for reg_path in registry_paths:
            try:
                result = subprocess.run(
                    ["reg", "query", reg_path, "/v", "version"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if result.returncode == 0:
                    match = re.search(r"version\s+REG_SZ\s+([\d.]+)", result.stdout, re.IGNORECASE)
                    if match:
                        return match.group(1)
            except Exception as e:
                printf(f"Error reading Chrome version from registry path {reg_path}: {e}")

    commands = [
        ["google-chrome", "--version"],
        ["chrome", "--version"],
        ["chromium", "--version"],
        ["chromium-browser", "--version"],
        ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"],
    ]

    for cmd in commands:
        version = run_version_command(cmd)
        if version:
            return version

    return None


def run_version_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        output = (result.stdout or "") + " " + (result.stderr or "")
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
    except Exception:
        return None
    return None


def get_major_version(version):
    if not version:
        return None
    parts = version.split(".")
    return parts[0] if parts else None


def get_existing_chromedriver_version(chromedriver_path):
    """Reads the current downloaded ChromeDriver version by executing binary."""
    if not os.path.exists(chromedriver_path):
        return None

    try:
        result = subprocess.run([chromedriver_path, "--version"], capture_output=True, text=True, check=False)
        output = (result.stdout or "") + " " + (result.stderr or "")
        match = re.search(r"(\d+\.\d+\.\d+\.\d+)", output)
        if match:
            return match.group(1)
    except Exception as e:
        printf(f"Could not read existing ChromeDriver version: {e}")
    return None


def remove_existing_chromedriver(drivers_dir, chromedriver_dirname, chromedriver_path):
    """Removes previously downloaded chromedriver files to avoid stale binary usage."""
    try:
        extracted_dir = os.path.join(drivers_dir, chromedriver_dirname)
        if os.path.isdir(extracted_dir):
            shutil.rmtree(extracted_dir, ignore_errors=True)
        if os.path.isfile(chromedriver_path):
            os.remove(chromedriver_path)
    except Exception as e:
        printf(f"Warning: failed to remove old ChromeDriver files cleanly: {e}")


def get_chromedriver_dirname():
    os_name = platform.system()
    machine = platform.machine().lower()

    if os_name == "Windows":
        return "chromedriver-win64"
    if os_name == "Linux":
        return "chromedriver-linux64"
    if os_name == "Darwin":
        if "arm" in machine or "aarch" in machine:
            return "chromedriver-mac-arm64"
        return "chromedriver-mac-x64"
    return None


def get_chromedriver_url(chromedriver_version):
    """Gets the ChromeDriver download URL."""
    os_name = platform.system()
    machine = platform.machine().lower()

    if os_name == "Windows":
        chromedriver_filename = "win64/chromedriver-win64.zip"
    elif os_name == "Darwin":
        if "arm" in machine or "aarch" in machine:
            chromedriver_filename = "mac-arm64/chromedriver-mac-arm64.zip"
        else:
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