import pytest

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage


@pytest.mark.parametrize("message", [
    "Hello",
    "Selenium",
    "Automation"
])
def test_simple_form_submission(driver, base_url, message):

    page = SimpleFormPage(driver)

    page.navigate_to(base_url + "simple-form-demo/")

    page.enter_message(message)

    page.click_submit()

    assert message in page.get_displayed_message()


def test_checkbox_demo(driver, base_url):

    page = CheckboxPage(driver)

    page.navigate_to(base_url + "checkbox-demo/")

    page.check_option()

    assert page.is_option_checked()


def test_dropdown_selection(driver, base_url):

    page = DropdownPage(driver)

    page.navigate_to(base_url + "select-dropdown-demo/")

    page.select_day("Wednesday")

    assert page.get_selected_day() == "Wednesday"


@pytest.mark.skip(reason="Input Form page has changed on the current TestMu AI website.")
def test_input_form_submit(driver, base_url):
    pass