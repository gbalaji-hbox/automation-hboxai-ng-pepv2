from features.pages.base_page import BasePage


class VpeUserDashboardPage(BasePage):
    """Page object for VPE User Dashboard page."""

    def __init__(self, driver):
        super().__init__(driver)