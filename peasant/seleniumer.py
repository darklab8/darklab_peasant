from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from typing import NewType
from pathlib import Path
from . import loggus as logging

headless_options = Options()
# You comment the next 3 lines to debug if there is any issue
headless_options.add_argument('--no-sandbox')
headless_options.add_argument('--headless')
headless_options.add_argument('--disable-dev-shm-usage')

Url = NewType("url", str)

@contextmanager
def open_browser(debug: bool, url: Url):
    chorme_driver_path = Path(__file__).parent.parent / "docker" / "chromedriver" / "114.0.5735.90"
    chrome_options = headless_options if not debug else Options()
    service = Service(executable_path=chorme_driver_path)
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        yield driver
        driver.get(url)
    finally:
        driver.quit()


class Loginner:
    def __init__(self, url: Url, debug: bool = False):
        self.debug = debug
        self.url = url

    def login(self):
        
        with open_browser(debug=self.debug, url=self.url) as driver:
            logging.info("opened browser")
        