import pytest
from utils.html_parser import convert_to_board

@pytest.fixture(autouse=True)
def before_all():
    pass

def test_initial_game_board_parsing():
    with open("tests/initial_game_board.html", "r") as f:
        html = f.read()

    board_data = convert_to_board(html)
    assert board_data.board.shape == (4, 4)
    assert True
