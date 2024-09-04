import numpy as np
from core.data import BoardData
from core.valid_keys import ValidKeys

from utils.board import move_board, slide_row_to_left

def test_validate_slide_row_to_left():
    row = np.array([2, 0, 0, 2])
    want = np.array([4, 0, 0, 0])
    got, score = slide_row_to_left(row)

    assert got.all() == want.all()
    assert score == 4

def test_validate_move_board_to_down():
    board = np.array([
        [0, 0, 8, 0],
        [2, 0, 0, 0],
        [2, 0, 0, 2],
        [0, 0, 8, 0]
    ])
    want = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 0, 16, 2]
    ])
    got = move_board(BoardData(board, 0), ValidKeys.DOWN)
    assert got.board.all() == want.all()
    assert got.score == 20

def test_validate_move_board_to_up():
    board = np.array([
        [0, 0, 8, 0],
        [2, 0, 0, 0],
        [2, 0, 4, 2],
        [0, 0, 8, 0]
    ])
    want = np.array([
        [4, 0, 8, 2],
        [0, 0, 4, 0],
        [0, 0, 8, 0],
        [0, 0, 0, 0]
    ])
    got = move_board(BoardData(board, 0), ValidKeys.UP)
    assert got.board.all() == want.all()
    assert got.score == 4

def test_validate_move_board_to_left():
    board = np.array([
        [0, 0, 8, 0],
        [2, 0, 0, 0],
        [2, 0, 4, 2],
        [0, 0, 8, 0]
    ])
    want = np.array([
        [8, 0, 0, 0],
        [2, 0, 0, 0],
        [2, 4, 2, 0],
        [8, 0, 0, 0]
    ])
    got = move_board(BoardData(board, 0), ValidKeys.LEFT)
    assert got.board.all() == want.all()
    assert got.score == 0
