from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import secrets
from . import captch_solver
import selenium.common.exceptions
from selenium.webdriver.remote.webelement import WebElement
from . import types
from . import exceptions
import os
import time
from .notificator.aggregator import iNotificator, NotificatorAggregator
from peasant.settings import Settings
import subprocess

headless_options = Options()
# You comment the next 3 lines to debug if there is any issue
headless_options.add_argument("--no-sandbox")
headless_options.add_argument("--headless")
headless_options.add_argument("--disable-dev-shm-usage")
headless_options.add_argument("--disable-gpu")
headless_options.add_argument('--host-resolver-rules="MAP localhost 127.0.0.1"')

class FailedOpenBrowser(exceptions.PeasantException):
    pass


class FailedLoginException(exceptions.PeasantException):
    pass


class ZeroDriver:
    def quit(self) -> None:
        pass

def delay_between_actions(delay: types.Seconds) -> None:
    time.sleep(delay)

class MyDriver:
    def __init__(self, driver: webdriver.Chrome, settings: Settings) -> None:
        self.settings = settings
        self.driver = driver
        self.logger: iNotificator = NotificatorAggregator(settings=self.settings)

    def delay_between_actions(self) -> None:
        delay_between_actions(self.settings.selenium_delay)
    
    def find_element(self, selector: str) -> WebElement:
        self.logger.debug(f'find_element({selector}=)')
        try:
            self.delay_between_actions()
            elem = self.driver.find_element(By.CSS_SELECTOR, selector)
        except selenium.common.exceptions.NoSuchElementException as err:
            panic_msg = f"not found expected element by {selector=}"
            self.logger.panic(panic_msg)
            raise FailedLoginException(panic_msg) from err

        return elem

    def get(self, url: types.SeleniumLink) -> None:
        self.driver.get(url)
        self.delay_between_actions()

    def refresh(self) -> None:
        self.driver.refresh()
        self.delay_between_actions()

    @property
    def title(self) -> str:
        return self.driver.title



class Loginner:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.url = self.settings.selenium_reg_link
        self.logger = NotificatorAggregator(settings=settings)

    @contextmanager
    def open_browser(self) -> Generator[MyDriver, None, None]:
        chorme_driver_path = (
            Path(__file__).parent.parent
            / "docker"
            / "chromedriver"
            / self.settings.driver_version
        )
        chrome_options = headless_options if not self.settings.debug else Options()
        service = Service(executable_path=chorme_driver_path)
        driver: webdriver.Chrome | ZeroDriver = ZeroDriver()
        try:
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(self.settings.selenium_await_time)
            self.logger.debug("opened browser")
            yield MyDriver(driver=driver, settings=self.settings)
        except Exception as err:
            raise FailedOpenBrowser(str(err)) from err
        finally:
            self.logger.debug("exited browser")
            driver.quit()

    def login(self) -> None:
        try:
            self._login()
        except Exception as exc:
            self.logger.panic(f"{type(exc)=},{str(exc)=}")
            raise FailedOpenBrowser(str(exc)) from exc

    def delay_between_actions(self) -> None:
        delay_between_actions(self.settings.selenium_delay)

    def _login(self) -> None:
        with self.open_browser() as driver:
            driver.get(self.url)
            self.logger.debug(f"opened {self.url=}")

            # ====================== First page =======================
            text_asking_to_solve_captcha = "Введите символы с картинки"
            text_telling_captcha_was_answered_incorrectly = (
                "Символы с картинки введены не правильно. Пожалуйста, повторите попытку"
            )
            for _ in range(self.settings.selenium_attempts_solving_captcha):
                first_page_body = driver.find_element("body")

                if text_asking_to_solve_captcha not in first_page_body.text:
                    panic_msg = f"expected to find '{text_asking_to_solve_captcha}'. Found {first_page_body.text=}"
                    self.logger.panic(panic_msg)
                    raise FailedLoginException(panic_msg)

                picture = driver.find_element("#ctl00_MainContent_imgSecNum")
                captcha_src = picture.get_attribute("src")

                if captcha_src is None:
                    panic_msg = "Expected to find src attribute in captcha element"
                    self.logger.panic(panic_msg)
                    raise FailedLoginException(panic_msg)
                
                captcha_filename = f"{secrets.token_hex(4)}.captcha"
                if self.settings.debug:
                    captcha_path = Path(__file__).parent / captcha_filename
                else:
                    captcha_path = Path("/tmp") / captcha_filename

                try:
                    with open(captcha_path, "wb") as file:
                        file.write(picture.screenshot_as_png)

                    captcha_result = captch_solver.captchaSolver(captcha_path, settings=self.settings).run()
                except captch_solver.RecognitionError as err:
                    self.logger.debug(f'caught RecognitionError.err:{str(err)=}')
                    driver.refresh()
                    continue
                finally:
                    os.remove(captcha_path)

                input_elem = driver.find_element("#ctl00_MainContent_txtCode")

                input_elem.clear()
                self.delay_between_actions()
                input_elem.send_keys(captcha_result)
                self.delay_between_actions()

                button_elem = driver.find_element("#ctl00_MainContent_ButtonA")

                button_elem.click()

                body_elem = driver.find_element("body")
                if text_telling_captcha_was_answered_incorrectly not in body_elem.text:
                    break
            else: 
                panic_msg = (
                    f"{text_telling_captcha_was_answered_incorrectly}, "
                    f"failed {self.settings.selenium_attempts_solving_captcha} times"
                )
                self.logger.panic(panic_msg)
                raise FailedLoginException(panic_msg)

            # ====================== Second page =======================
            body_elem = driver.find_element("body")
            text_asking_to_check_free_time = "Для проверки наличия свободного времени"
            if text_asking_to_check_free_time not in body_elem.text:
                panic_msg = f"expected to find '{text_asking_to_check_free_time}' at second page, found {body_elem.text=}"
                self.logger.panic(panic_msg)
                raise FailedLoginException(panic_msg)

            button_elem = driver.find_element("#ctl00_MainContent_ButtonB")
            button_elem.click()

            # ====================== Third page =======================
            body_elem = driver.find_element("body")

            text_no_free_time_is_found = "записи нет свободного времени"
            if text_no_free_time_is_found in body_elem.text:
                self.logger.debug(text_no_free_time_is_found)
                return

            # 🎉
            self.logger.info("THERE IS FREE AVAILABLE TIME!!!!!!!")
