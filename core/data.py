from dataclasses import dataclass
from numpy import ndarray

@dataclass
class BoardData:
    board: ndarray
    score: int
