import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .util import *
from .settings import *


class BotException(Exception):
    """ The base exception for our typing bot. """


class UnknownStateError(Exception):
    """ We have landed on a page we were not expecting. """


class TypingBot:
    _driver = None

    def __init__(self, username: str, password: str, wpm=None):
        self.username = username
        self.password = password
        self.wpm = wpm

    @property
    def driver(self):
        if self._driver is None:
            self._driver = webdriver.Chrome()
            self._driver.get(URL)
        return self._driver

    def quit(self):
        self.driver.quit()

    def race(self, max_actions=None):
        num_actions = 0
        while True:
            time.sleep(1)
            self._take_action()
            num_actions += 1
            if max_actions is not None:
                if num_actions >= max_actions:
                    break
        self.quit()

    def _take_action(self):
        wait_for_visible_link(self.driver)
        if is_link_visible(self.driver, LINK_SIGN_IN):
            self._login()
        elif is_link_visible(self.driver, LINK_ENTER_RACE):
            link_click(self.driver, LINK_ENTER_RACE)
        elif is_link_visible(self.driver, LINK_RACE_AGAIN):
            link_click(self.driver, LINK_RACE_AGAIN)
        elif is_link_visible(self.driver, LINK_LEAVE_RACE):
            self._enter_typing_text()
        else:
            raise UnknownStateError

    def _login(self):
        if is_link_visible(self.driver, LINK_SIGN_IN):
            link_click(self.driver, LINK_SIGN_IN)

            self.driver.find_element_by_css_selector(
                CSS_SELECTOR_USER
            ).send_keys(self.username)

            self.driver.find_element_by_css_selector(
                CSS_SELECTOR_PASS
            ).send_keys(self.password)

            css_selector_click(self.driver, CSS_SELECTOR_BTN_LOGIN)

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
            EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_INPUT))
        )

        send_keys = txt_input.send_keys
        sleep = time.sleep
        current_time = time.time
        if self.wpm is None:
            # send keys as fast as possible
            for character in text:
                send_keys(character)
        else:
            # target some words per minute
            start_time = current_time()
            num_characters = len(text)
            num_words = num_characters / CHARS_PER_WORD
            target_time_sec = (num_words / self.wpm) * 60
            target_end_time = start_time + target_time_sec
            wait_time_per_char = target_time_sec / num_characters
            for character in text:
                send_keys(character)
                sleep(wait_time_per_char)
                # recalculate the wait time per character
                # as sending keys / executing code takes time...
                target_time_sec = max(target_end_time - current_time(), 0)
                wait_time_per_char = target_time_sec / num_characters

        # wait for the race again link
        counter = 0
        while (
            not is_link_visible(self.driver, LINK_RACE_AGAIN)
            and counter < MAX_WAIT_SECONDS
        ):
            time.sleep(1)
            counter += 1
