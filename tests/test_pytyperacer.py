from pytyperacer import TypingBot

USERNAME = "typeracer196"
PASSWORD = "typeracermail"
WPM = 100


def test_pytyperacer():
    bot = TypingBot(USERNAME, PASSWORD, WPM)
    bot.race(max_actions=10)
