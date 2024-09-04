from dataclasses import dataclass
from numpy import ndarray, array_equal

@dataclass
class BoardData:
    board: ndarray
    score: int

    def __hash__(self):
        return hash(self.board.tobytes())

    def __eq__(self, other):
        return array_equal(self.board, other.board)
