"""
Our main configuration settings.
"""
from enum import Enum


URL = "https://play.typeracer.com/"

MAX_WAIT_SECONDS = 20
CHARS_PER_WORD = 5  # typeracer counts X characers as a word

HTML_SIGN_IN = '<a class="gwt-Anchor" href="javascript:;">Sign In</a>'

CSS_SELECTOR_LOGIN = "a.gwt-Anchor"
CSS_SELECTOR_ENTER_RACE = ".mainMenu  a.gwt-Anchor"
CSS_SELECTOR_RACE_AGAIN = ".raceAgainLink"
CSS_SELECTOR_USER = "input.gwt-TextBox"
CSS_SELECTOR_PASS = "input.gwt-PasswordTextBox"
CSS_SELECTOR_BTN_LOGIN = "button.gwt-Button"
CSS_SELECTOR_RACING = "input.txtInput"

CSS_SELECTORS = [
    CSS_SELECTOR_LOGIN,
    CSS_SELECTOR_ENTER_RACE,
    CSS_SELECTOR_RACE_AGAIN,
    CSS_SELECTOR_USER,
    CSS_SELECTOR_PASS,
    CSS_SELECTOR_BTN_LOGIN,
    CSS_SELECTOR_RACING,
]


class State(Enum):
    LOGIN = 1
    ENTER_RACE = 2
    RACING = 3
    UNKNOWN = 4
