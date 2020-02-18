from pytyperacer import TypingBot

USERNAME = "racemeifyoucan"
PASSWORD = "myracepassword"
WPM = 98


def test_pytyperacer():
    bot = TypingBot(USERNAME, PASSWORD, WPM)
    bot.race(max_actions=6)
