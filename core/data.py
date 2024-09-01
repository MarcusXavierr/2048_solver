from dataclasses import dataclass
from numpy import matrix

@dataclass
class BoardData:
    board: matrix
    score: int
