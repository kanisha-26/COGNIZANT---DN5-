import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ------------------------------
# Simple Form Demo
# ------------------------------
@pytest.mark.parametrize("message", [
    "Hello",
    "Selenium",
    "Automation"
])
def test_simple_form_submission(driver, base_url, message):

    driver.get(base_url + "simple-form-demo/")

    message_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-message"))
    )

    message_box.clear()
    message_box.send_keys(message)

    driver.find_element(By.ID, "showInput").click()

    WebDriverWait(driver, 10).until(
        lambda d: message in d.page_source
    )

    assert message in driver.page_source


# ------------------------------
# Checkbox Demo
# ------------------------------
def test_checkbox_demo(driver, base_url):

    driver.get(base_url + "checkbox-demo/")

    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[type='checkbox']")
        )
    )

    checkbox.click()

    assert checkbox.is_selected()


# ------------------------------
# Dropdown Demo
# ------------------------------
def test_dropdown_selection(driver, base_url):

    driver.get(base_url + "select-dropdown-demo/")

    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "select-demo"))
    )

    select = Select(dropdown)

    select.select_by_visible_text("Wednesday")

    assert select.first_selected_option.text == "Wednesday"