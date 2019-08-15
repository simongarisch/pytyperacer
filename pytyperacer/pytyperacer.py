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
from .settings import URL, MAX_WAIT_SECONDS, SELECTORS


class State(Enum):
    MAIN_PAGE = 1
    ENTER_LOGIN = 2
    RACING = 3
    DEAD = 4


def get_state(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")


def get_visible_selectors(driver):
    """ Are any of the css selectors we are after
        e.g. '.gwt-Anchor', 'input.gwt-PasswordTextBox' ...
        visible on this page.
    """
    selectors_visible = []
    for css_selector in SELECTORS.values():
        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        selectors_visible.extend(elements)
    return selectors_visible


def wait_for_targeted_css_selector(driver):
    """ Wait until any of our targeted selectors are visible. """
    attempts = 0
    max_attempts = 10
    wait_time = float(MAX_WAIT_SECONDS) / max_attempts
    selectors_visible = get_visible_selectors()
    while len(selectors_visible) == 0:
        time.sleep(wait_time)
        selectors_visible = get_visible_selectors()
        print(selectors)
    return selectors


def wait_for_specific_css_selector(driver, selector):
    """ Wait until a specific css selector is visible. """
    WebDriverWait(driver, MAX_WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
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
        wait_for_targeted_css_selector(self.driver)
        self._try_enter_race()
        self._login()
        self._try_enter_race()
        text = self._get_typing_text()
        print(text)

    def _reset_driver(self):
        self._driver = webdriver.Chrome()
        self.driver.get(URL)

    def _enter_race(self):
        wait_for_specific_css_selector(self.driver, ".gwt-Anchor")
        self.driver.find_element_by_css_selector(".gwt-Anchor").click()

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

    def _login(self):
        self.driver.find_element_by_css_selector("input.gwt-TextBox").send_keys(
            self.username
        )

        self.driver.find_element_by_css_selector(
            "input.gwt-PasswordTextBox"
        ).send_keys(self.password)

        self.driver.find_element_by_css_selector("button.gwt-Button").click()

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
