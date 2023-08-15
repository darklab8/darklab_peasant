from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .seleniumer import Loginner, open_browser
import pytest
import os


def test_opening_example():
    with open_browser() as driver:
        driver.get("https://example.com/")
        assert "Example Domain" in driver.title

        elem = driver.find_element(By.CSS_SELECTOR, "a")

        elem.click()

        body = driver.find_element(By.CSS_SELECTOR, "body")

        assert "As described in RFC 2606" in body.text


# never run with all tests :scream:
@pytest.mark.skipif(
    condition=os.environ.get("PYTEST_ALLOW_VISUAL_DEBUG_ONLY") != "true",
    reason="You get banned if u ran this more than 24 times per day",
)
@pytest.mark.allow_visual_debug_only
def test_check_queue():
    with open_browser() as driver:
        print(123)
