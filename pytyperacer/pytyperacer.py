import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)

from . import util
from .settings import *


class TypingBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def driver(self):
        return self._driver

    def race(self):
        self._reset_driver()
        util.wait_for_any_css_selector(self.driver)
        if self._login_required():
            self._login()
        self._enter_race()
        text = self._get_typing_text()
        self._start_typing(text)

    def _reset_driver(self):
        self._driver = webdriver.Chrome()
        self.driver.get(URL)

    def _enter_race(self):
        """ Wait for the enter race css selector and click on it. """
        util.css_selector_click(self.driver, CSS_SELECTOR_ENTER_RACE)

    """
    def _try_enter_race(self):
        success = False
        counter = 0
        while not success and counter < 10:
            try:
                util.css_selector_click(self.driver, CSS_SELECTOR_ENTER_RACE)
            except (NoSuchElementException, ElementClickInterceptedException):
                success = False
            else:
                success = True
            counter += 1
            time.sleep(1)
        return success
    """

    def _login_required(self):
        """ Have we been presented with a login prompt. """
        if util.is_css_selector_visible(self.driver, CSS_SELECTOR_LOGIN):
            return True
        if util.is_css_selector_visible(self.driver, CSS_SELECTOR_USER):
            return True
        return False

    def _login(self):
        if util.is_css_selector_visible(self.driver, CSS_SELECTOR_LOGIN):
            util.css_selector_click(self.driver, CSS_SELECTOR_LOGIN)

        self.driver.find_element_by_css_selector(CSS_SELECTOR_USER).send_keys(
            self.username
        )

        self.driver.find_element_by_css_selector(CSS_SELECTOR_PASS).send_keys(
            self.password
        )

        util.css_selector_click(self.driver, CSS_SELECTOR_BTN_LOGIN)

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
        """ There will be a wait time for other competitors to join before
            the txtInput box becomes clickable.
            Make sure that you don't apply a timeout too soon.
        """
        txt_input = WebDriverWait(self.driver, MAX_WAIT_SECONDS).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_RACING))
        )

        for character in text:
            txt_input.send_keys(character)
