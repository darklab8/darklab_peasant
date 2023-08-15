from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from contextlib import contextmanager
from pathlib import Path
from typing import Generator
from . import settings
import secrets
from . import captch_solver
from .notificator import logger
import selenium.common.exceptions
from selenium.webdriver.remote.webelement import WebElement
from . import types
from . import exceptions
import os

headless_options = Options()
# You comment the next 3 lines to debug if there is any issue
headless_options.add_argument("--no-sandbox")
headless_options.add_argument("--headless")
headless_options.add_argument("--disable-dev-shm-usage")

class FailedOpenBrowser(exceptions.PeasantException):
    pass


class FailedLogin(exceptions.PeasantException):
    pass

class ZeroDriver:
    def quit(self) -> None:
        pass


@contextmanager
def open_browser(
    awaited: types.Seconds = settings.SELENIUM_AWAIT_TIME,
) -> Generator[webdriver.Chrome, None, None]:
    chorme_driver_path = (
        Path(__file__).parent.parent
        / "docker"
        / "chromedriver"
        / settings.DRIVER_VERSION
    )
    chrome_options = headless_options if not settings.DEBUG else Options()
    service = Service(executable_path=chorme_driver_path)
    driver: webdriver.Chrome | ZeroDriver = ZeroDriver()
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(awaited)
        logger.debug("opened browser")
        yield driver
    except Exception as err:
        raise FailedOpenBrowser() from err
    finally:
        logger.debug("exited browser")
        driver.quit()

def find_element(driver: webdriver.Chrome, selector: str) -> WebElement:
    try:
        driver.implicitly_wait(types.Seconds(1))
        elem = driver.find_element(By.CSS_SELECTOR, selector)
    except selenium.common.exceptions.NoSuchElementException:
        logger.panic(f"not found expected element by {selector=}", error_cls=FailedLogin)
    finally:
        driver.implicitly_wait(settings.SELENIUM_AWAIT_TIME)

    return elem

class Loginner:
    def __init__(self, url: types.GovRegistryLink):
        self.url = url

    def login(self) -> None:
        try:
            self._login()
        except Exception as exc:
            logger.panic(str(exc),from_exc=exc)

    def _login(self) -> None:
        with open_browser() as driver:
            driver.get(self.url)

            # ====================== First page =======================
            first_page_body = find_element(driver, "body")

            if "Введите символы с картинки" not in first_page_body.text:
                logger.panic(f"expected to find 'Введите симолы с картинки'. Found {first_page_body.text=}", error_cls=FailedLogin)
            
            picture = find_element(driver, "#ctl00_MainContent_imgSecNum")
            captcha_src = picture.get_attribute("src")

            if captcha_src is None:
                logger.panic("Expected to find src attribute in captcha element", error_cls=FailedLogin)

            captcha_path = Path(__file__).parent / f"{secrets.token_hex(4)}.captcha"

            with open(captcha_path, 'wb') as file:
                file.write(picture.screenshot_as_png)

            captcha_result = captch_solver.captchaSolver(captcha_path).run()
            os.remove(captcha_path)

            input_elem = find_element(driver, "#ctl00_MainContent_txtCode")
            
            input_elem.clear()
            input_elem.send_keys(captcha_result)

            button_elem = find_element(driver, "#ctl00_MainContent_ButtonA")
            
            button_elem.click()

            # ====================== Second page =======================
            body_elem = find_element(driver, "body")
            if "Символы с картинки введены не правильно. Пожалуйста, повторите попытку" in body_elem.text:
                logger.panic(f"Символы с картинки введены не правильно. Пожалуйста, повторите попытку", error_cls=FailedLogin)

            if "Для проверки наличия свободного времени" not in body_elem.text:
                logger.panic(f"expected to find 'Для проверки наличия свободного времени' at second page, found {body_elem.text=}", error_cls=FailedLogin)

            button_elem = find_element(driver, "#ctl00_MainContent_ButtonB")
            button_elem.click()

            # ====================== Third page =======================
            body_elem = find_element(driver, "body")
            
            if "записи нет свободного времени" in body_elem.text:
                logger.debug("записи нет свободного времени OK")
                return

            logger.info("THERE IS FREE AVAILABLE TIME!!!!!!!")
