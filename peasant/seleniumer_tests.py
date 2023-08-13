from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .seleniumer import Loginner, open_browser
from . import loggus as logging

def test_opening_example():
    with open_browser() as driver:
        driver.get("https://example.com/")
        assert 'Example Domain' in driver.title

        elem = driver.find_element(By.CSS_SELECTOR, "a")

        elem.click()

        body = driver.find_element(By.CSS_SELECTOR, "body")
        
        assert 'As described in RFC 2606' in body.text

    