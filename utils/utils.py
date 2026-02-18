from selenium.webdriver import ActionChains

from utils.logger import printf
import re
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By



def slugify(text):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', text.lower())).strip('-')

def normalize(text):
    # Convert to lowercase, replace non-breaking space, collapse multiple spaces to one
    return re.sub(r'\s+', ' ', text.lower().replace('\u00a0', ' ')).strip()


def get_current_time():
    time_stamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    return time_stamp


def time_to_seconds(time_str):
    mins, secs = map(int, time_str.split(":"))
    return mins * 60 + secs


def get_fixed_dob(years=20, date_format='%d-%m-%Y'):
    """
    Returns a date string exactly `years` years before today.

    Args:
        years (int): Number of years to subtract. Default is 20.
        date_format (str): Format for the output date string. Default is 'YYYY-MM-DD'.

    Returns:
        str: Formatted date string.
    """
    past_date = datetime.now() - relativedelta(years=years)
    return past_date.strftime(date_format)


def get_fixed_start_date(years=1, date_format='%d-%m-%Y'):
    """
    Returns a date string exactly `years` years before today.
    """
    past_date = get_fixed_dob(years, date_format)
    return past_date


def get_current_date(date_format='%d-%m-%Y', days_offset=0, years_offset=0):
    """
    Returns today's date as a string, with optional offset for past or future dates.

    Args:
        date_format (str): Format for the output date string. Default is '%d-%m-%Y'.
        days_offset (int): Number of days to offset from today. Positive for future, negative for past. Default is 0.
        years_offset (int): Number of years to offset from today. Positive for future, negative for past. Default is 0.
    Returns:
        str: Formatted date string.
    """
    return (datetime.now() + timedelta(days=days_offset) + relativedelta(years=years_offset)).strftime(date_format)


def convert_dob_ddmmyyyy_to_yyyymmdd(dob_str: str) -> str:
    """
    Converts a date string from dd-mm-yyyy to yyyy-mm-dd format.
    Returns the converted string, or the original if conversion fails.
    """
    try:
        dob_obj = datetime.strptime(dob_str, "%d-%m-%Y")
        return dob_obj.strftime("%Y-%m-%d")
    except ValueError: # Catching the specific exception for date parsing errors
        return dob_str


def convert_to_human_readable_date(date_str, expected_format=None):
    """
    Converts a date string to human-readable format (e.g., 'Jan 1, 1991').

    Args:
        date_str (str): The date string to convert.
        expected_format (str, optional): The expected format of the input date string (e.g., "%m-%d-%y").
                                         If not provided, tries common formats.

    Returns:
        str: Human-readable date string like "Mar 4, 1954", or original if conversion fails.
    """

    # If expected format is given, try only that
    if expected_format:
        try:
            date_obj = datetime.strptime(date_str, expected_format)
            day = date_obj.strftime("%d").lstrip("0") or "0"
            month = date_obj.strftime("%b")
            year = date_obj.strftime("%Y")
            return f"{month} {day}, {year}"
        except ValueError as e:
            printf(f"Failed to parse date '{date_str}' with format '{expected_format}': {e}")
            return date_str

    # Otherwise, try all common formats in order of priority
    date_formats = [
        "%m-%d-%y",  # 03-04-54
        "%m-%d-%Y",  # 03-04-1954
        "%d-%m-%Y",  # 04-03-1954
        "%Y-%m-%d",  # 1954-03-04
        "%d/%m/%Y",  # 04/03/1954
        "%Y/%m/%d",  # 1954/03/04
        "%m/%d/%Y",  # 03/04/1954 (US style)
    ]

    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            day = date_obj.strftime("%d").lstrip("0") or "0"
            month = date_obj.strftime("%b")
            year = date_obj.strftime("%Y")
            return f"{month} {day}, {year}"
        except ValueError:
            continue

    return date_str


def row_count_check(expected, actual):
    actual_count = int(actual)
    expected_count = int(expected)
    if actual_count == 0:
        printf(f"Expected at least 1 row, but got {actual}")
        return False

    if actual_count < expected_count:
        printf(f"Only {actual} rows displayed, which is less than the requested {expected} entries per page.")
        return True,

    if actual_count > expected_count:
        printf(f"Expected at most {expected} rows, but got {actual}")
        return False

    printf(f"Found exactly {actual_count} rows as expected")
    return True

def format_number(number: str) -> str:
    """
    Normalize number by removing non-digit characters.
    """
    return ''.join(filter(lambda char: char.isdigit(), number))


def format_number_with_dashes(number: str) -> str:
    return f"{number[:3]}-{number[3:6]}-{number[6:]}"

# java, nodejs, allure-behave ||| npm install -g allure-commandline

# behave -f allure_behave.formatter:AllureFormatter -o Reports/features

# cmd prompt allure serve Reports/features

# jenkins allure and signing-panda plugins required


def verify_search_results_in_table(base_page, search_value, table_rows_locator, criteria=None):
    try:
        # Handle DOB format conversion for multiple formats
        if criteria and criteria.lower() == "dob":
            # Try multiple format conversions to match different table formats
            original_value = search_value

            # Try human-readable format first (for patient list: "Oct 10, 1950")
            human_readable = convert_to_human_readable_date(search_value, "%m-%d-%Y")

            # Try YYYY-MM-DD format (for dashboard: "1970-02-15")
            try:
                date_obj = datetime.strptime(search_value, "%m-%d-%Y")
                yyyy_mm_dd = date_obj.strftime("%Y-%m-%d")
            except Exception as e:
                printf(f"Failed to convert DOB '{search_value}' to YYYY-MM-DD: {e}")
                yyyy_mm_dd = search_value

            printf(f"DOB search formats - Original: {original_value}, Human: {human_readable}, YYYY-MM-DD: {yyyy_mm_dd}")

            # We'll check all formats in the search loop
            search_formats = [original_value, human_readable, yyyy_mm_dd]
        else:
            search_formats = [search_value]


        # Get search results rows
        rows = base_page.find_elements(table_rows_locator)

        if not rows:
            printf("No search results found in the table")
            return False

        # Check each row for the search value using multiple formats if DOB
        for i, row in enumerate(rows):
            row_text = row.text.strip().replace("\n", " ").lower()
            normalized_row = normalize(row_text)
            printf(f"[Row {i + 1}] Text: {row_text}")

            # Check all search formats
            for search_format in search_formats:
                normalized_search = normalize(search_format)

                # For name searches, handle partial/jumbled matching (e.g., "Aaeon Rademacher" should match "Aaeon J. Rademacher")
                if criteria and criteria.lower() == "name":
                    # Split search into parts and check if all parts are present in the row (partial match)
                    search_parts = normalized_search.split()
                    if all(part in normalized_row for part in search_parts):
                        printf(f"Found partial name match for: {search_format} in row")
                        return True
                else:
                    # Default substring match for other criteria
                    if normalized_search in normalized_row:
                        printf(f"Found matching result containing: {search_format}")
                        return True

        printf(f"No matching results found for: {search_value}")
        return False

    except Exception as e:
        printf(f"Error verifying search results: {e}")
        return False


def select_calendar_date(base_page, calendar_header, calendar_container_locator, day_locator, target_date):
    # Find the calendar container (the visible month grid)
    calendar = base_page.find_element(calendar_container_locator)
    
    # Get month/year header to check if we are on the correct month
    header = base_page.find_element(calendar_header)
    month_year_text = header.text.strip()  # e.g., "September 2025"
    target_month_year = target_date.strftime("%B %Y")
    
    # Navigate to correct month if necessary
    while month_year_text != target_month_year:
        if target_date > datetime.strptime(month_year_text, "%B %Y"):
            # Click next month button
            next_btn = calendar.find_element(By.XPATH, "//button[@name='next-month']")
            next_btn.click()
        else:
            # Click previous month button
            prev_btn = calendar.find_element(By.XPATH, "//button[@name='previous-month']")
            prev_btn.click()
        month_year_text = base_page.find_element(calendar_header).text.strip()
    
    # Now select the day from the grid
    all_days = base_page.find_elements(day_locator)  # Usually each day is a button
    day_to_select = str(target_date.day)
    
    for day_btn in all_days:
        if day_btn.text.strip() == day_to_select and day_btn.is_enabled():
            ActionChains(base_page.driver).move_to_element(day_btn).click(day_btn).perform()
            return True
    
    raise ValueError(f"Target date {target_date} not found or not enabled in the calendar")


def extract_table_row_as_dict(base_page, table_locator, header_locator=None, specific_row=1):
    """
    Extract a specific data row from a table as a dictionary based on table headers.

    Args:
        base_page: BasePage instance with driver and utility methods
        table_locator: Locator for the table element
        header_locator: Optional locator for header row. If None, assumes first row is header

    Returns:
        dict: Dictionary mapping header names to first row cell values, or None if extraction fails
    """
    try:
        printf("🔍 Extracting table row data as dictionary...")

        # Wait for table to be visible
        if not base_page.is_element_visible(table_locator):
            printf("❌ Table not visible")
            return None

        # Get table element
        table_element = base_page.find_element(table_locator)

        # Get all rows in the table
        rows = table_element.find_elements(By.XPATH, ".//tr")
        if len(rows) < 2:  # Need at least header + 1 data row
            printf(f"❌ Not enough rows in table: {len(rows)}")
            return None

        # Determine header row
        if header_locator:
            # Use specific header locator
            header_row = base_page.find_element(header_locator)
            header_cells = header_row.find_elements(By.XPATH, ".//th | .//td")
        else:
            # Assume first row is header
            header_row = rows[0]
            header_cells = header_row.find_elements(By.XPATH, ".//th | .//td")

        # Extract header texts
        headers = []
        for cell in header_cells:
            header_text = cell.text.strip()
            if header_text:  # Only include non-empty headers
                headers.append(header_text)

        printf(f"📋 Found {len(headers)} headers: {headers}")

        if not headers:
            printf("❌ No headers found in table")
            return None

        # Get specific data row (skip header row)
        if isinstance(specific_row, int):
            data_row_index = specific_row if not header_locator else 0
        else:
            # specific_row is a WebElement, find its index
            try:
                data_row_index = rows.index(specific_row)
            except ValueError:
                printf("❌ Specified row WebElement not found in table rows")
                return None

        if data_row_index >= len(rows):
            printf("❌ No data rows found after header")
            return None

        data_row = rows[data_row_index]
        data_cells = data_row.find_elements(By.XPATH, ".//td")

        printf(f"📊 Found {len(data_cells)} data cells in first row")

        # Map headers to data cells
        row_dict = {}
        for i, header in enumerate(headers):
            if i < len(data_cells):
                cell_value = data_cells[i].text.strip()
                row_dict[header] = cell_value
                printf(f"  {header}: {cell_value}")
            else:
                row_dict[header] = ""
                printf(f"  {header}: (empty)")

        printf(f"✅ Successfully extracted row data: {row_dict}")
        return row_dict

    except Exception as e:
        printf(f"❌ Error extracting table row as dict: {e}")
        import traceback
        traceback.print_exc()
        return None