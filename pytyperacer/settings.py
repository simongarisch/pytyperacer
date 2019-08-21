"""
Our main configuration settings.
"""

URL = "https://play.typeracer.com/"

MAX_WAIT_SECONDS = 20
CHARS_PER_WORD = 5  # typeracer counts X characers as a word

LINK_SIGN_IN = "Sign In"
LINK_ENTER_RACE = "Enter a typing race"
LINK_RACE_AGAIN = "Race Again »"
LINK_LEAVE_RACE = "« main menu (leave race)"

LINKS = [LINK_SIGN_IN, LINK_ENTER_RACE, LINK_RACE_AGAIN, LINK_LEAVE_RACE]

CSS_SELECTOR_USER = "input.gwt-TextBox"
CSS_SELECTOR_PASS = "input.gwt-PasswordTextBox"
CSS_SELECTOR_BTN_LOGIN = "button.gwt-Button"
CSS_SELECTOR_INPUT = "input.txtInput"
