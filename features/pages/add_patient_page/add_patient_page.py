from time import sleep

from faker.proxy import Faker
from selenium.webdriver.common.by import By

from features.commons.locators import AddPatientPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import get_fixed_dob


class AddPatientPage(BasePage):
    """Page object for the Add Patient page."""

    def __init__(self, driver):
        super().__init__(driver)
        self.faker = Faker()

    # -------------------- Navigation --------------------

    def is_on_add_patient_page(self):
        """Check if currently on the Add Patient page."""
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.ADD_PATIENT, partial=True)

    # -------------------- Step 1: Clinic Selection --------------------

    def select_clinic(self, clinic_name):
        """Select a clinic from the dropdown."""
        try:
            self.wait_for_loader()
            printf(f"Selecting clinic: {clinic_name}")
            self.click(AddPatientPageLocators.SELECT_CLINIC_DROPDOWN)
            sleep(0.5)
            clinic_option = AddPatientPageLocators.SELECT_CLINIC_OPTION(clinic_name)
            self.click(clinic_option)
            self.wait_for_dom_stability()
            printf(f"Successfully selected clinic: {clinic_name}")
        except Exception as e:
            printf(f"Error selecting clinic: {e}")
            raise

    def select_facility(self, facility_name):
        """Select a facility from the dropdown."""
        try:
            printf(f"Selecting facility: {facility_name}")
            self.click(AddPatientPageLocators.SELECT_FACILITY_DROPDOWN)
            sleep(0.5)
            facility_option = AddPatientPageLocators.SELECT_FACILITY_OPTION(facility_name)
            self.click(facility_option)
            self.wait_for_dom_stability()
            printf(f"Successfully selected facility: {facility_name}")
        except Exception as e:
            printf(f"Error selecting facility: {e}")
            raise

    def select_first_available_provider(self):
        """Select the first available provider from the dropdown."""
        try:
            printf("Selecting first available provider")
            self.click(AddPatientPageLocators.SELECT_PROVIDER_DROPDOWN)
            sleep(0.5)
            # Click the first option in the provider dropdown
            first_option = (By.XPATH, "//div[@role='option'][1]")
            self.click(first_option)
            self.wait_for_dom_stability()
            printf("Successfully selected first available provider")
        except Exception as e:
            printf(f"Error selecting provider: {e}")
            raise

    def is_facility_dropdown_disabled(self):
        """Check if the Facility dropdown is disabled."""
        try:
            dropdown = self.find_element(AddPatientPageLocators.SELECT_FACILITY_DROPDOWN)
            parent = dropdown.find_element(By.XPATH, "..")
            class_attr = parent.get_attribute("class") or ""
            return "disabled" in class_attr.lower() or dropdown.get_attribute("disabled") is not None
        except Exception as e:
            printf(f"Error checking facility dropdown state: {e}")
            return False

    def is_provider_dropdown_disabled(self):
        """Check if the Provider dropdown is disabled."""
        try:
            dropdown = self.find_element(AddPatientPageLocators.SELECT_PROVIDER_DROPDOWN)
            parent = dropdown.find_element(By.XPATH, "..")
            class_attr = parent.get_attribute("class") or ""
            return "disabled" in class_attr.lower() or dropdown.get_attribute("disabled") is not None
        except Exception as e:
            printf(f"Error checking provider dropdown state: {e}")
            return False

    # -------------------- Step 1: Personal Information --------------------

    def fill_personal_information(self, include_optional=False):
        """Fill the patient personal information fields with valid data."""
        try:
            first_name = f"Automation-{self.faker.first_name()}"
            last_name = self.faker.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@hbox.ai"
            phone = self.faker.numerify(text="##########")
            birth_date = get_fixed_dob()

            self.send_keys(AddPatientPageLocators.FIRST_NAME_INPUT, first_name)
            self.send_keys(AddPatientPageLocators.LAST_NAME_INPUT, last_name)
            self.send_keys(AddPatientPageLocators.EMAIL_INPUT, email)
            self.send_keys(AddPatientPageLocators.PHONE_NUMBER_INPUT, phone)
            self.send_keys(AddPatientPageLocators.BIRTH_DATE_INPUT, birth_date)
            self._select_gender("Male")

            if include_optional:
                self._fill_optional_personal_info()

            printf(f"Filled personal information for {first_name} {last_name}")
            return {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "birth_date": birth_date,
                "gender": "Male"
            }
        except Exception as e:
            printf(f"Error filling personal information: {e}")
            raise

    def _fill_optional_personal_info(self):
        """Fill optional personal information fields."""
        try:
            alias_name = self.faker.first_name()
            alt_phone = self.faker.numerify(text="##########")
            
            self.send_keys(AddPatientPageLocators.ALIAS_NAME_INPUT, alias_name)
            self.send_keys(AddPatientPageLocators.ALTERNATE_PHONE_INPUT, alt_phone)
            self._select_height("5", "10")
            printf("Filled optional personal information")
        except Exception as e:
            printf(f"Error filling optional personal info: {e}")
            raise

    def _select_gender(self, gender):
        """Select gender from dropdown."""
        try:
            self.click(AddPatientPageLocators.GENDER_DROPDOWN)
            sleep(0.3)
            gender_option = AddPatientPageLocators.GENDER_OPTION(gender)
            self.click(gender_option)
            printf(f"Selected gender: {gender}")
        except Exception as e:
            printf(f"Error selecting gender: {e}")
            raise

    def _select_height(self, feet, inches):
        """Select height from dropdowns."""
        try:
            self.click(AddPatientPageLocators.HEIGHT_FEET_DROPDOWN)
            sleep(0.3)
            feet_option = AddPatientPageLocators.HEIGHT_OPTION(feet)
            self.click(feet_option)
            
            self.click(AddPatientPageLocators.HEIGHT_INCHES_DROPDOWN)
            sleep(0.3)
            inches_option = AddPatientPageLocators.HEIGHT_OPTION(inches)
            self.click(inches_option)
            printf(f"Selected height: {feet}'{inches}\"")
        except Exception as e:
            printf(f"Error selecting height: {e}")
            raise

    # -------------------- Step 1: Medical Records --------------------

    def fill_medical_records(self, include_optional=False):
        """Fill the medical records fields with valid data."""
        try:
            emr_id = f"EMR-{self.faker.numerify(text='######')}"
            primary_insurance_id = f"INS-{self.faker.numerify(text='#########')}"
            primary_insurance_payer = "Blue Cross Blue Shield"
            insurance_plan = "PPO Premium"

            self.send_keys(AddPatientPageLocators.EMR_ID_INPUT, emr_id)
            self.send_keys(AddPatientPageLocators.PRIMARY_INSURANCE_ID_INPUT, primary_insurance_id)
            self.send_keys(AddPatientPageLocators.PRIMARY_INSURANCE_PAYER_INPUT, primary_insurance_payer)
            self.send_keys(AddPatientPageLocators.INSURANCE_PLAN_INPUT, insurance_plan)

            if include_optional:
                self._fill_optional_medical_records()

            printf(f"Filled medical records with EMR ID: {emr_id}")
            return {
                "emr_id": emr_id,
                "primary_insurance_id": primary_insurance_id,
                "primary_insurance_payer": primary_insurance_payer,
                "insurance_plan": insurance_plan
            }
        except Exception as e:
            printf(f"Error filling medical records: {e}")
            raise

    def _fill_optional_medical_records(self):
        """Fill optional medical records fields."""
        try:
            secondary_insurance_id = f"INS-{self.faker.numerify(text='#########')}"
            secondary_insurance_payer = "Aetna"
            
            self.send_keys(AddPatientPageLocators.SECONDARY_INSURANCE_ID_INPUT, secondary_insurance_id)
            self.send_keys(AddPatientPageLocators.SECONDARY_INSURANCE_PAYER_INPUT, secondary_insurance_payer)
            printf("Filled optional medical records")
        except Exception as e:
            printf(f"Error filling optional medical records: {e}")
            raise

    # -------------------- Step 1: Program Eligibility --------------------

    def select_program_eligibility(self, program):
        """Select program eligibility checkbox."""
        try:
            if program == "CCM Eligible":
                self.click(AddPatientPageLocators.CCM_ELIGIBLE_CHECKBOX)
            elif program == "RPM Eligible":
                self.click(AddPatientPageLocators.RPM_ELIGIBLE_CHECKBOX)
            elif program == "PCM Eligible":
                self.click(AddPatientPageLocators.PCM_ELIGIBLE_CHECKBOX)
            printf(f"Selected program eligibility: {program}")
        except Exception as e:
            printf(f"Error selecting program eligibility: {e}")
            raise

    # -------------------- Step 1: Emergency Contact --------------------

    def fill_emergency_contact(self):
        """Fill the emergency contact information."""
        try:
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            phone = self.faker.numerify(text="##########")

            self.send_keys(AddPatientPageLocators.EMERGENCY_FIRST_NAME_INPUT, first_name)
            self.send_keys(AddPatientPageLocators.EMERGENCY_LAST_NAME_INPUT, last_name)
            self.send_keys(AddPatientPageLocators.EMERGENCY_PHONE_INPUT, phone)

            printf(f"Filled emergency contact: {first_name} {last_name}")
            return {
                "emergency_first_name": first_name,
                "emergency_last_name": last_name,
                "emergency_phone": phone
            }
        except Exception as e:
            printf(f"Error filling emergency contact: {e}")
            raise

    # -------------------- Step 1: Navigation --------------------

    def click_continue_button(self):
        """Click the Continue button to proceed to the next step."""
        try:
            self.click(AddPatientPageLocators.CONTINUE_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked Continue button")
        except Exception as e:
            printf(f"Error clicking Continue button: {e}")
            raise

    def is_continue_button_disabled(self):
        """Check if the Continue button is disabled."""
        try:
            button = self.find_element(AddPatientPageLocators.CONTINUE_BUTTON)
            return button.get_attribute("disabled") is not None
        except Exception as e:
            printf(f"Error checking Continue button state: {e}")
            return False

    # -------------------- Step 2: Address --------------------

    def fill_address_information(self, include_optional=False):
        """Fill the address information fields."""
        try:
            address_line_1 = f"{self.faker.building_number()} {self.faker.street_name()}"
            city = self.faker.city()
            state = self.faker.state()
            zip_code = self.faker.postcode()

            self.send_keys(AddPatientPageLocators.ADDRESS_LINE_1_INPUT, address_line_1)
            self.send_keys(AddPatientPageLocators.CITY_INPUT, city)
            self.send_keys(AddPatientPageLocators.STATE_INPUT, state)
            self.send_keys(AddPatientPageLocators.ZIP_CODE_INPUT, zip_code)

            if include_optional:
                self.send_keys(AddPatientPageLocators.ADDRESS_LINE_2_INPUT, "Apt 4B")

            printf(f"Filled address: {address_line_1}, {city}, {state} {zip_code}")
            return {
                "address_line_1": address_line_1,
                "city": city,
                "state": state,
                "zip_code": zip_code
            }
        except Exception as e:
            printf(f"Error filling address information: {e}")
            raise

    # -------------------- Step 2: Navigation --------------------

    def click_previous_button(self):
        """Click the Previous button to go back to the previous step."""
        try:
            self.click(AddPatientPageLocators.PREVIOUS_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked Previous button")
        except Exception as e:
            printf(f"Error clicking Previous button: {e}")
            raise

    # -------------------- Step 3: Summary --------------------

    def is_on_summary_page(self):
        """Check if currently on the Summary step."""
        try:
            return self.is_element_visible(AddPatientPageLocators.SUMMARY_HEADING, timeout=5)
        except Exception:
            return False

    def verify_summary_displays_patient_info(self):
        """Verify that the summary page displays all patient information sections."""
        try:
            is_personal_visible = self.is_element_visible(AddPatientPageLocators.PERSONAL_INFO_SECTION, timeout=5)
            is_medical_visible = self.is_element_visible(AddPatientPageLocators.MEDICAL_RECORDS_SECTION, timeout=5)
            is_address_visible = self.is_element_visible(AddPatientPageLocators.ADDRESS_SECTION, timeout=5)
            
            all_visible = is_personal_visible and is_medical_visible and is_address_visible
            printf(f"Summary page verification - Personal: {is_personal_visible}, Medical: {is_medical_visible}, Address: {is_address_visible}")
            return all_visible
        except Exception as e:
            printf(f"Error verifying summary page: {e}")
            return False

    # -------------------- Step 3: Submit --------------------

    def click_submit_button(self):
        """Click the Submit button to create the patient."""
        try:
            self.click(AddPatientPageLocators.SUBMIT_BUTTON)
            self.wait_for_dom_stability()
            printf("Clicked Submit button")
        except Exception as e:
            printf(f"Error clicking Submit button: {e}")
            raise

    # -------------------- Notifications --------------------

    def is_patient_added_notification_visible(self):
        """Check if the patient added success notification is visible."""
        try:
            return self.is_element_visible(AddPatientPageLocators.PATIENT_ADDED_SUCCESS_NOTIFICATION, timeout=10)
        except Exception as e:
            printf(f"Error checking patient added notification: {e}")
            return False

    # -------------------- Step Verification --------------------

    def is_on_patient_details_step(self):
        """Check if currently on the Patient Details step (Step 1)."""
        try:
            # Check for elements that are only visible on Step 1
            return self.is_element_visible(AddPatientPageLocators.SELECT_CLINIC_DROPDOWN, timeout=5)
        except Exception:
            return False

    def is_redirected_to_dashboard(self):
        """Check if redirected to the dashboard after patient creation."""
        try:
            return self.check_url_contains(Routes.DASHBOARD, partial=True)
        except Exception as e:
            printf(f"Error checking dashboard redirect: {e}")
            return False