"""
Our main configuration settings.
"""
from enum import Enum


URL = "https://play.typeracer.com/"

MAX_WAIT_SECONDS = 5


class State(Enum):
    ENTER_RACE = 1
    LOGIN = 2
    RACING = 3
    UNKNOWN = 4


CSS_SELECTORS = {
    State.ENTER_RACE: ".gwt-Anchor",
    State.LOGIN: "input.gwt-PasswordTextBox",
    State.RACING: "input.txtInput",
}
