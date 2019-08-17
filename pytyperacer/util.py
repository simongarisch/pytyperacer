import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .settings import *


def get_state(driver):
    """ Get the current racing state. """
    css_selectors = wait_for_any_css_selector()

    if (
        CSS_SELECTOR_LOGIN in css_selectors
        or CSS_SELECTOR_USER in css_selectors
    ):
        return State.LOGIN

    if CSS_SELECTOR_ENTER_RACE in css_selectors:
        return State.ENTER_RACE

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


def css_selector_click(driver, css_selector):
    wait_for_specific_css_selector(driver, css_selector)
    driver.find_element_by_css_selector(css_selector).click()

