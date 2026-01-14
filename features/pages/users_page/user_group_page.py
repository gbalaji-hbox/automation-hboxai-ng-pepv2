from features.commons.locators import UserGroupPageLocators
from features.commons.routes import Routes
from features.pages.base_page import BasePage
from utils.logger import printf
from utils.utils import extract_table_row_as_dict, row_count_check


class UserGroupPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def get_first_row_data(self):
        return extract_table_row_as_dict(self, UserGroupPageLocators.USER_GROUPS_TABLE)

    def is_user_group_history_dialog_open(self):
        """Check if the User Operation History dialog is open."""
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(UserGroupPageLocators.HISTORY_DIALOG)
            self.click(UserGroupPageLocators.HISTORY_DIALOG_CLOSE_BUTTON)
            self.wait_for_dom_stability()
            return True
        except Exception as e:
            printf(f"Error during user history dialog: {e}")
            return False

    def is_navigated_to_edit_user_group_page(self):
        self.wait_for_dom_stability()
        return self.check_url_contains(Routes.EDIT_GROUP, partial=False)

    def is_delete_confirmation_dialog_open(self):
        """Check if the confirmation dialog appears."""
        try:
            self.wait_for_dom_stability()
            self.is_element_visible(UserGroupPageLocators.DELETE_DIALOG)
            self.click(UserGroupPageLocators.DELETE_DIALOG_CANCEL_BUTTON)
            return True
        except Exception as e:
            printf(f"Error during user history dialog: {e}")
            return False

    def verify_rows_per_page(self, expected_count):
        """Verify the number of rows displayed per page matches expected count."""
        try:
            self.wait_for_loader()
            actual_count = self.get_number_of_table_rows(UserGroupPageLocators.USER_GROUPS_TABLE)
            printf(f"Expected rows per page: {expected_count}, Actual rows displayed: {actual_count}")
            return row_count_check(expected_count, actual_count)
        except Exception as e:
            printf(f"Error verifying rows per page: {e}")
            return False