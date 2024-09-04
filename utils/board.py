from typing import cast
from core import BoardData
from core import ValidKeys
import numpy as np

def transiction_board(data: BoardData, move: ValidKeys) -> BoardData:
    new_board = move_board(data, move)
    new_board.board = insert_value_at_random_empty_position(new_board.board)

    return new_board

# TODO: Refatorar pra remover a parte repetitiva de dentro dos ifs
def move_board(data: BoardData, move: ValidKeys) -> BoardData:
    new_board = np.zeros(data.board.shape)
    score = data.score
    if move == ValidKeys.LEFT:
        for i in range(data.board.shape[0]):
            new_row, row_score = slide_row_to_left(data.board[i])
            new_board[i] = new_row
            score += row_score
    if move == ValidKeys.RIGHT:
        for i in range(data.board.shape[0]):
            # Aqui eu simplesmente inverto o array, e mando fazer o slide pra esquerda
            new_row, row_score = slide_row_to_left(data.board[i][::-1])
            # E inverto de volta na hora de colocar no array
            new_board[i] = new_row[::-1]
            score += row_score
    if move == ValidKeys.UP:
        # Aqui eu transponho pra lidar com o slide pra esquerda (horizontalmente) quando o movimento deveria ser pra cima (verticalmente)
        transposed = data.board.T
        for i in range(data.board.shape[0]):
            new_row, row_score = slide_row_to_left(transposed[i])
            new_board[i] = new_row
            score += row_score
        new_board = new_board.T
    if move == ValidKeys.DOWN:
        # Aqui transponho e inverto, como se fosse um movimento pra direita
        transposed = data.board.T
        for i in range(data.board.shape[0]):
            new_row, row_score = slide_row_to_left(transposed[i][::-1])
            new_board[i] = new_row[::-1]
            score += row_score
        new_board = new_board.T

    # E por fim, retorno meu novo board
    return BoardData(new_board, score)

def slide_row_to_left(row: np.ndarray) -> tuple[np.ndarray,int]:
    # Remove todos os valores zerados pra simplificar o trabalho, imagine [0, 2, 0, 2]
    # removendo os zeros, fica [2, 2], então fica muito mais obvio que um movimento pra esquerda gera o [4, 0, 0, 0]
    non_zero = row[row != 0]
    new_row = []
    score = 0
    merged = False
    # Aqui eu percorro cada item do meu array, e se ele for igual ao proximo, eu faço o merge, senão, eu só adiciono no array
    for i in range(len(non_zero)):
        if merged:
            merged = False
            continue
        current_value = non_zero[i].astype(int).item()
        if i + 1 < len(non_zero) and non_zero[i] == non_zero[i+1]:
            new_row.append(current_value * 2)
            score += current_value * 2
            merged = True
        else:
            new_row.append(current_value)

    # E por fim, preciso preencher o resto do array com zeros e transformar em um vetor numpy
    n_of_zeros = len(row) - len(new_row)
    return np.array(new_row + [0] * n_of_zeros), cast(int, score)

def insert_value_at_random_empty_position(board: np.ndarray) -> np.ndarray:
    # Aqui eu preciso verificar se existe algum espaço vazio, eu posso inserir o numero 2
    empty_positions = []
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == 0:
                empty_positions.append((i, j))

    if len(empty_positions) == 0:
        return board

    np.random.shuffle(empty_positions)
    i, j = empty_positions[np.random.choice(len(empty_positions))]
    board[i][j] = 2
    return board

