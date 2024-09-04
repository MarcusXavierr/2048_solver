from dataclasses import dataclass
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from core import BoardData
from time import sleep
from numpy import zeros

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

    def get_board_data(self) -> BoardData:
        parsed_html = self._parse_html()
        # score = self.driver.find_element(By.CLASS_NAME, "score-container").text
        # TODO: Achar uma forma de obter o score pelo score-container. Separando o score do +N que vem no text junto
        score = self.driver.find_element(By.CLASS_NAME, "best-container").text
        return convert_to_board(parsed_html, int(score))

    def _parse_html(self, error_counter: int = 0) -> list[ParsedHTML]:
        tile_div = self.driver.find_element(By.CLASS_NAME, "tile-container")
        tiles = tile_div.find_elements(By.XPATH, "div")
        data: list[ParsedHTML] = []
        for tile in tiles:
            try:
                class_info = tile.get_attribute("class")
                if class_info is None or class_info == '':
                    raise Exception("Class info is None")
                position_x_y = parse_tile_title(class_info)
                value = int(tile.text or 0)
                is_new = 'tile-new' in class_info
                position_hash = hash(position_x_y)
                was_merged = 'tile-merged' in class_info

                parsed = ParsedHTML(value=value, is_new=is_new, position_x_y=position_x_y, position_hash=position_hash, was_merged=was_merged)
                data.append(parsed)
            except Exception as e:
                print(f'Erro ao parsear os dados: {tile}')
                print(e)
                if error_counter <= 3:
                    sleep(0.01)
                    return self._parse_html(error_counter + 1)
                print('calma calebreso')
                exit()

        return data

def parse_tile_title(tile_class: str) -> tuple[int, int]:
    # If the position does not exists, throw an error anyway
    position_tile = list(filter(lambda c: 'position' in c, tile_class.split(" ")))[0]
    x = position_tile.split("-")[3]
    y = position_tile.split("-")[2]
    return int(x) - 1, int(y) - 1

def convert_to_board(parsed_html: list[ParsedHTML], score: int) -> BoardData:
    seen = dict()
    for tile in parsed_html:
        if tile.position_hash not in seen:
            seen[tile.position_hash] = tile
        else:
            if tile.was_merged:
                seen[tile.position_hash] = tile

    filterd_data = list(seen.values())
    board = zeros((4,4))
    for tile in filterd_data:
        board[tile.position_x_y[0]][tile.position_x_y[1]] = tile.value

    return BoardData(board=board, score=score)
