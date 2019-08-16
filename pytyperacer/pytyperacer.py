import time
from enum import Enum
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)

from .settings import (
    URL,
    MAX_WAIT_SECONDS,
    CSS_SELECTOR_ENTER,
    CSS_SELECTOR_ENTER_ALT,
    CSS_SELECTOR_USER,
    CSS_SELECTOR_PASS,
    CSS_SELECTOR_BTN_LOGIN,
    CSS_SELECTOR_RACING,
)


CSS_SELECTORS = [
    CSS_SELECTOR_ENTER,
    CSS_SELECTOR_ENTER_ALT,
    CSS_SELECTOR_USER,
    CSS_SELECTOR_PASS,
    CSS_SELECTOR_BTN_LOGIN,
    CSS_SELECTOR_RACING,
]


class State(Enum):
    ENTER = 1
    LOGIN = 2
    RACING = 3
    UNKNOWN = 4


def get_state(driver):
    """ Get the current racing state. """
    css_selectors = wait_for_any_css_selector()

    if CSS_SELECTOR_ENTER in css_selectors:
        return State.ENTER

    if CSS_SELECTOR_PASS in css_selectors:
        return State.LOGIN

    if CSS_SELECTOR_RACING in css_selectors:
        return State.RACING

    return State.UNKNOWN


def is_css_selector_visible(driver, css_selector):
    """ Is a particular css selector visible. """
    elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
    if len(elements) == 0:
        return False
    else:
        return True


def get_visible_css_selectors(driver):
    """ Are any of the css selectors we are after
        e.g. '.gwt-Anchor', 'input.gwt-PasswordTextBox' ...
        visible on this page.
    """
    visible_css_selectors = []
    for css_selector in CSS_SELECTORS:
        if is_css_selector_visible(driver, css_selector):
            visible_css_selectors.append(css_selector)
    return visible_css_selectors


def wait_for_any_css_selector(driver):
    """ Wait until any css selectors of interest are visible. """
    attempts = 0
    max_attempts = 10
    wait_time = float(MAX_WAIT_SECONDS) / max_attempts

    while True:
        attempts += 1
        visible_css_selectors = get_visible_css_selectors(driver)
        if len(visible_css_selectors) != 0:
            break
        if attempts >= max_attempts:
            break
        time.sleep(wait_time)

    return visible_css_selectors


def wait_for_specific_css_selector(driver, css_selector):
    """ Wait until a specific css selector is visible. """
    WebDriverWait(driver, MAX_WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
    )


class TypingBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def driver(self):
        return self._driver

    def race(self):
        self._reset_driver()
        wait_for_any_css_selector(self.driver)
        self._enter_race()
        if self._login_required():
            self._login()
        self._try_enter_race()  # look into this...
        text = self._get_typing_text()
        self._start_typing(text)

    def _reset_driver(self):
        self._driver = webdriver.Chrome()
        self.driver.get(URL)

    def _enter_race(self):
        """ Wait for the enter race css selector and click on it. """
        wait_for_specific_css_selector(self.driver, CSS_SELECTOR_ENTER)
        self.driver.find_element_by_css_selector(CSS_SELECTOR_ENTER).click()

    def _try_enter_race(self):
        success = False
        counter = 0
        while not success and counter < 10:
            try:
                self.driver.find_element_by_css_selector(
                    ".mainMenu  a.gwt-Anchor"
                ).click()
            except (NoSuchElementException, ElementClickInterceptedException):
                success = False
            else:
                success = True
            counter += 1
            time.sleep(1)
        return success

    def _login_required(self):
        """ Have we been presented with a login prompt. """
        if is_css_selector_visible(self.driver, CSS_SELECTOR_USER):
            return True
        return False

    def _login(self):
        self.driver.find_element_by_css_selector(CSS_SELECTOR_USER).send_keys(
            self.username
        )

        self.driver.find_element_by_css_selector(CSS_SELECTOR_PASS).send_keys(
            self.password
        )

        self.driver.find_element_by_css_selector(
            CSS_SELECTOR_BTN_LOGIN
        ).click()

    def _get_typing_text(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        span_list = soup.find_all("span")

        typing_content = []
        for span in span_list:
            attrs = span.attrs
            if "unselectable" in attrs:
                typing_content.append(span.text)

        return "".join(typing_content)

    def _start_typing(self, text):
        txt_input = WebDriverWait(self.driver, MAX_WAIT_SECONDS).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_RACING))
        )

        for character in text:
            txt_input.send_keys(character)
