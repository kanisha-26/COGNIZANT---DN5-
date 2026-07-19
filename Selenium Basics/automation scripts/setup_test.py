from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()

driver.get("https://www.lambdatest.com/selenium-playground/")

driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

assert "simple-form-demo" in driver.current_url

print("Current URL:", driver.current_url)

driver.back()

driver.execute_script("window.open('https://www.google.com');")

print("Total Tabs:", len(driver.window_handles))

driver.switch_to.window(driver.window_handles[1])

print("Google Title:", driver.title)

driver.switch_to.window(driver.window_handles[0])

driver.save_screenshot("playground_screenshot.png")

print("Screenshot Saved")

print("Window Size:", driver.get_window_size())

driver.set_window_size(1280, 800)

print("New Window Size:", driver.get_window_size())

driver.quit()