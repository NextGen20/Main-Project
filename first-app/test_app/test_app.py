import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_signup(driver):
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler('test.log')
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    # logger.info('This is a log message')

    chrome_driver_path = ChromeDriverManager().install()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    service_obj = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    
    logger.info("Chrome browser opened")
    driver.get("http://localhost:5000/signup")
    logger.info("Navigated to signup page")
    first_name_input = driver.find_element(By.NAME, "fname")
    first_name_input.send_keys("amit")
    logger.info("Entered first name")
    last_name = driver.find_element(By.NAME, "lname")
    last_name.send_keys("bachars")
    logger.info("Entered last name")
    email = driver.find_element(By.NAME, "email")
    email.send_keys("amitbachargmail.com")
    logger.info("Entered email")
    password = driver.find_element(By.NAME, "password")
    password.send_keys("ab123456")
    logger.info("Entered password")
    submit_btn = driver.find_element(By.XPATH, "//input[@type='submit']")
    submit_btn.click()
    logger.info("Clicked on submit button")
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    logger.info("Welcome message displayed")
    welcome_message = driver.find_element(By.TAG_NAME, "h1").text
    expected_message = f"Welcome to our website, amit!"
    
    assert welcome_message == expected_message
    logger.info("Test case passed")

    


