import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from .settings import *


def is_link_visible(driver, link_text):
    try:
        driver.find_element_by_link_text(link_text)
        return True
    except NoSuchElementException:
        return False


def link_click(driver, link_text):
    driver.find_element_by_link_text(link_text).click()


def wait_for_visible_link(driver):
    """ Wait for any link of interest to be visible. """
    wait_time = 0
    while wait_time < MAX_WAIT_SECONDS:
        for link in LINKS:
            if is_link_visible(driver, link):
                return
        time.sleep(1)
        wait_time += 1
    raise TimeoutException


def wait_for_specific_css_selector(driver, css_selector):
    """ Wait until a specific css selector is visible. """
    WebDriverWait(driver, MAX_WAIT_SECONDS).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
    )


def css_selector_click(driver, css_selector):
    wait_for_specific_css_selector(driver, css_selector)
    driver.find_element_by_css_selector(css_selector).click()
