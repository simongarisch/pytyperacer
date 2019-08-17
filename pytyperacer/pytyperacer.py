import time
from abc import ABC, abstractmethod
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


class BotException(Exception):
    """ The base exception for our typing bot. """


class UnknownStateError(Exception):
    """ We have landed on a page we were not expecting. """


class TypingBot:
    _driver = None

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def driver(self):
        if self._driver is None:
            self._driver = webdriver.Chrome()
            self._driver.get(URL)
        return self._driver

    def race(self):
        while True:
            self._take_action()
            time.sleep(3)

    def _take_action(self):
        state = util.get_state(self.driver)
        print(state)
        if not isinstance(state, State):
            raise TypeError("Must be an instance of State!")
        if state is State.LOGIN:
            self._login()
        elif state is State.ENTER_RACE:
            self._enter_race()
        elif state is State.RACING:
            self._enter_typing_text()
        elif state is State.UNKNOWN:
            raise UnknownStateError

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

    def _enter_race(self):
        """ Wait for the enter race css selector and click on it. """
        util.css_selector_click(self.driver, CSS_SELECTOR_ENTER_RACE)

    def _enter_typing_text(self):
        """ Collect the text we need to type and send each character. """
        self._send_typing_text(self._get_typing_text())

    def _get_typing_text(self):
        """ Collect the text that we need to type. """
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        span_list = soup.find_all("span")

        typing_content = []
        for span in span_list:
            attrs = span.attrs
            if "unselectable" in attrs:
                typing_content.append(span.text)

        return "".join(typing_content)

    def _send_typing_text(self, text):
        """ There will be a wait time for other competitors to join before
            the txtInput box becomes clickable.
            Make sure that you don't apply a timeout too soon.
        """
        txt_input = WebDriverWait(self.driver, MAX_WAIT_SECONDS).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_RACING))
        )

        for character in text:
            txt_input.send_keys(character)
