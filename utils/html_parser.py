from dataclasses import dataclass
from selenium.webdriver.chrome.webdriver import WebDriver
from core import BoardData
from numpy import matrix

@dataclass
class ParsedHTML:
    value: int
    is_new: bool
    position_x_y: tuple[int, int]
    position_hash: int
    was_merged: bool

class HTMLHelper:
    # TODO: Use this to extract the HTML from the page and then call the convert_to_board function
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

def parse_html(html: str) -> list[ParsedHTML]:
    # TODO: Parse the acual HTML, maybe with xpath
    return []

def convert_to_board(html: str) -> BoardData:
    # TODO: Convert the parsed HTML into a board, without repeated position_hashes. Fill the board with 0 for empty positions.
    # Also I will consider work with log2(n) for values. because instead of 2, 4, 8, 16. It will be 1,2,3,4...
    print(html)
    return BoardData(board=matrix([]), score=0)
