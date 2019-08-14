import pytest
from pytyperacer import TypingBot

USERNAME = "typeracer196"
PASSWORD = "typeracermail"


def test_pytyperacer():
    bot = TypingBot(USERNAME, PASSWORD)

    bot.race()
