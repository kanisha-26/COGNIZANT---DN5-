from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckboxPage(BasePage):

    CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")

    def check_option(self, index=0):
        checkbox = self.wait_for_element(self.CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self, index=0):
        checkbox = self.wait_for_element(self.CHECKBOX)
        return checkbox.is_selected()