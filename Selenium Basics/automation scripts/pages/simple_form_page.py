from selenium.webdriver.common.by import By
from .base_page import BasePage


class SimpleFormPage(BasePage):

    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BUTTON = (By.ID, "showInput")

    def enter_message(self, text):
        box = self.wait_for_element(self.MESSAGE_INPUT)
        box.clear()
        box.send_keys(text)

    def click_submit(self):
        self.wait_for_element(self.SUBMIT_BUTTON).click()

    def get_displayed_message(self):
        return self.driver.page_source