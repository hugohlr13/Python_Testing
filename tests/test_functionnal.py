import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    yield browser
    browser.quit()

def test_successful_login(browser):
    browser.get('http://localhost:5000')
    time.sleep(2)  
    email_field = browser.find_element(By.NAME, 'email')
    email_field.send_keys('john@simplylift.co')
    time.sleep(2)
    email_field.submit()
    time.sleep(2)  
    assert 'Welcome, john@simplylift.co' in browser.page_source

def test_login_with_nonexistent_email(browser):
    # Go to login page
    browser.get('http://localhost:5000')
    time.sleep(2)

    # Enter an email that doesn't exist in the DB
    email_field = browser.find_element(By.NAME, 'email')
    email_field.send_keys('email@example.com')
    time.sleep(2)
    email_field.submit()
    time.sleep(2)

    # Check if the expected error message is displayed
    assert "Sorry, that email wasn't found." in browser.page_source


