from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from contextlib import contextmanager
from typing import NewType
from pathlib import Path
from . import loggus as logging
from typing import Generator
from . import settings
from unittest.mock import MagicMock

headless_options = Options()
# You comment the next 3 lines to debug if there is any issue
headless_options.add_argument('--no-sandbox')
headless_options.add_argument('--headless')
headless_options.add_argument('--disable-dev-shm-usage')

Url = NewType("Url", str)
Seconds = NewType("Seconds", int)

class FailedOpenBrowser(Exception):
    pass

@contextmanager
def open_browser(awaited: Seconds = 10) -> Generator[webdriver.Chrome, None, None]:
    chorme_driver_path = Path(__file__).parent.parent / "docker" / "chromedriver" / settings.DRIVER_VERSION
    chrome_options = headless_options if not settings.DEBUG else Options()
    service = Service(executable_path=chorme_driver_path)
    driver = MagicMock()
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(awaited)
        logging.info("opened browser")
        yield driver
    except Exception as err:
        raise FailedOpenBrowser() from err
    finally:
        driver.quit()

class Loginner:
    def __init__(self, url: Url, debug: bool = False):
        self.debug = debug
        self.url = url

    def login(self) -> None:
        
        with open_browser(debug=self.debug, url=self.url) as driver:
            logging.info("opened browser")
