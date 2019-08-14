import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException, ElementClickInterceptedException
)
from .settings import URL


def wait_css_selector_visible(driver, selector):
    """ Wait until a particular css selector is visible. """
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            selector
        ))
    )


class TypingBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._driver = webdriver.Chrome()

    @property
    def driver(self):
        return self._driver

    def race(self):
        self.driver.get(URL)
        self._try_enter_race()
        self._login()
        self._try_enter_race()
        text = self._get_typing_text()
        print(text)

    def _enter_race(self):
        wait_css_selector_visible(self.driver, ".gwt-Anchor")
        self.driver.find_element_by_css_selector(".gwt-Anchor").click()

    def _try_enter_race(self):
        success = False
        counter = 0
        while not success and counter < 10:
            try:
                self.driver.find_element_by_css_selector('.mainMenu  a.gwt-Anchor').click()
            except (NoSuchElementException, ElementClickInterceptedException):
                success = False
            else:
                success = True
            counter += 1
            time.sleep(1)
        return success

    def _login(self):
        self.driver.find_element_by_css_selector(
            'input.gwt-TextBox'
        ).send_keys(self.username)

        self.driver.find_element_by_css_selector(
            'input.gwt-PasswordTextBox'
        ).send_keys(self.password)

        self.driver.find_element_by_css_selector('button.gwt-Button').click()

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
