import pytest
from utils.html_parser import convert_to_board, ParsedHTML

@pytest.fixture(autouse=True)
def before_all():
    pass

def test_initial_game_board_parsing():
    parsed_data = [ParsedHTML(value=2, is_new=True, position_x_y=(3,2), position_hash=hash((3,2)), was_merged=False)]
    board_data = convert_to_board(parsed_data, 0)
    assert board_data.board.shape == (4,4)
    assert board_data.board[3][2] == 2
    assert board_data.board[0][0] == 0

def test_initial_game_board_parsing_with_merged_tiles():
    parsed_data = [
                    ParsedHTML(value=2, is_new=False, position_x_y=(3,3), position_hash=hash((3,3)), was_merged=False),
                    ParsedHTML(value=4, is_new=False, position_x_y=(3,3), position_hash=hash((3,3)), was_merged=True),
                    ParsedHTML(value=2, is_new=False, position_x_y=(3,3), position_hash=hash((3,3)), was_merged=False)
                   ]
    board_data = convert_to_board(parsed_data, 0)
    assert board_data.board.shape == (4,4)
    assert board_data.board[3][3] == 4
    assert board_data.board[0][0] == 0
