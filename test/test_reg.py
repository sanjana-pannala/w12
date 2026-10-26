
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pytest


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install())
    )
    yield driver
    driver.quit()


def get_alert_text(driver):
    alert = WebDriverWait(driver, 5).until(
        EC.alert_is_present()
    )
    text = alert.text
    alert.accept()
    return text


def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()

    assert get_alert_text(driver) == "Username cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")

    driver.find_element(By.NAME, "username").send_keys("Jaya")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()

    assert get_alert_text(driver) == (
        "Password must be at least 6 characters long."
    )


def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5001/")

    driver.find_element(By.NAME, "username").send_keys("Jaya")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/submit")
    )

    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Hello, Jaya! Welcome to the website" in body_text
