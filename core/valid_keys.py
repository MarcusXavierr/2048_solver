from enum import Enum
from selenium.webdriver.common.keys import Keys

class ValidKeys(Enum):
    UP = Keys.UP,
    DOWN = Keys.DOWN,
    LEFT = Keys.LEFT,
    RIGHT = Keys.RIGHT,
