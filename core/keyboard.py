from typing import cast
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from core.valid_keys import ValidKeys

class Keyboard:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.action = ActionChains(self.driver)
        self.valid_keys = [Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT]

    def press_key(self, key: str):
        """Presses a key on the keyboard, only accepts arrow keys"""
        if key not in self.valid_keys:
            raise ValueError(f"Invalid key: {key}")

        self.action.key_down(key)
        self.action.key_up(key)
        self.action.perform()

