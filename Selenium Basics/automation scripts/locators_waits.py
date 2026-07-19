from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")

# ID
element = driver.find_element(By.ID, "user-message")
print("ID Locator Works")

# Name
element = driver.find_element(By.NAME, "message")
print("Name Locator Works")

# Class Name
element = driver.find_element(By.CLASS_NAME, "form-control")
print("Class Name Locator Works")

# Tag Name
element = driver.find_element(By.TAG_NAME, "input")
print("Tag Name Locator Works")

# Absolute XPath
element = driver.find_element(By.XPATH, "//*[@id='user-message']")

print("Absolute XPath Works")

# Relative XPath
element = driver.find_element(By.XPATH, "//input[@id='user-message']")
print("Relative XPath Works")

# CSS Selector using ID
element = driver.find_element(By.CSS_SELECTOR, "#user-message")
print("CSS ID Works")

# CSS Selector using Attribute
element = driver.find_element(By.CSS_SELECTOR, "input[name='message']")
print("CSS Attribute Works")

# CSS Selector using Parent > Child
element = driver.find_element(By.CSS_SELECTOR, "div > input")
print("CSS Parent Child Works")

driver.quit()