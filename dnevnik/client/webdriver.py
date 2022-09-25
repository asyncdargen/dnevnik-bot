from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome

from time import sleep

from .elements import *

DNEVNIK_AUTH_END_POINT = "https://school.mos.ru/"

WEBDRIVER_SERVICE = Service(ChromeDriverManager().install())

WEBDRIVER_OPTIONS = Options()
WEBDRIVER_OPTIONS.add_argument("--headless")


def type_keys(element: WebElement, value):
    element.send_keys(value)


class DnevnikWebdriver:

    @staticmethod
    def fetch_cookies(login: str, password: str) -> dict[str, str]:
        driver = DnevnikWebdriver(login, password)

        try:
            driver.login()
            driver.wait_cookie_loading(3)

            print("[WebDriver] Responding cookies...")
            return driver.cookies()
        finally:
            print("[WebDriver] Closing connection...")
            driver.close()

    def __init__(self, login: str, password: str):
        self.__login = login
        self.__password = password
        self.driver = Chrome(options=WEBDRIVER_OPTIONS, service=WEBDRIVER_SERVICE)
        self.driver.get(DNEVNIK_AUTH_END_POINT)
        print("[WebDriver] Connecting to auth endpoint...")

    def login(self):
        self.find_element(*MOS_ENTER).click()

        self.wait_login_form()

        print("[WebDriver] Logining on mos.ru...")
        type_keys(self.find_element(*LOGIN_FIELD), self.__login)
        type_keys(self.find_element(*PASSWORD_FIELD), self.__password)

        self.find_element(*MOS_LOGIN).submit()

    def wait_cookie_loading(self, max_seconds: int):
        while self.cookies().get("profile_id") is None:
            if max_seconds <= 0:
                raise IOError
            sleep(.1)
            max_seconds -= .1

    # I know its shit
    def wait_login_form(self):
        print("[WebDriver] Waiting cookies loading...")
        captured = False

        while True:
            try:
                self.find_element(*LOGIN_FORM_LOADING_LOCK)
                captured = True
            except:
                if captured:
                    break
                else:
                    sleep(.17)

    def find_element(self, by, value: str) -> WebElement:
        return self.driver.find_element(by, value)

    def close(self):
        self.driver.close()

    def cookies(self) -> dict[str, str]:
        cookies = dict[str, str]()

        for cookie in self.driver.get_cookies():
            cookies[cookie["name"]] = cookie["value"]

        return cookies
