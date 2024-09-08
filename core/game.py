from functools import lru_cache
import time
from typing import cast, Optional
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from core.data import BoardData
from core.valid_keys import ValidKeys
# from utils import transiction_board
import numpy as np

GAME_OVER_MOVE = -1
INVALID_MOVE = -2

class Game:
    ## TODO: Pensar em COMO passar do limite de 15000 pontos
    def __init__(self, driver: WebDriver|None, num_of_simulations: int = 5) -> None:
        self.driver = driver
        self.num_of_simulations = num_of_simulations
        self.counter = 0

    def deal_with_paused_game(self, driver: WebDriver):
        won_the_game = driver.find_elements(By.CSS_SELECTOR, ".game-message.game-won")
        lose_the_game = driver.find_elements(By.CSS_SELECTOR, ".game-message.game-over")
        if len(won_the_game) == 0 and len(lose_the_game) == 0:
            return

        if len(lose_the_game) != 0:
            choice = input('1 - Tentar novamente\n2 - Parar\n')
            if choice == '2':
                exit()

            driver.find_element(By.CLASS_NAME, "retry-button").click()
            return

        # Win the game
        choice = input("1 - Continuar\n2 - Tentar novamente\n3 - Parar\n")
        if choice == '3':
            exit()

        if choice == '2':
            driver.find_element(By.CLASS_NAME, "retry-button").click()
            return

        driver.find_element(By.CLASS_NAME, "keep-playing-button").click()
        return

    def get_best_next_move(self, board: BoardData) -> str:
        _, best_move, _ = self._simulate_next_move_multiple(board, 0)
        if best_move is None:
            raise Exception("Erro na lógica: Eu não deveria passar o None da ultima recursão pra trás")

        if best_move is ValidKeys.UP:
            return Keys.UP
        if best_move is ValidKeys.DOWN:
            return Keys.DOWN
        if best_move is ValidKeys.LEFT:
            return Keys.LEFT
        return Keys.RIGHT

    @lru_cache(maxsize=None)
    def _simulate_next_move(self, board: BoardData, recurse_counter: int) -> tuple[BoardData, ValidKeys|None, int]:
        if recurse_counter == self.num_of_simulations:
            return board, None, count_empty_positions(board.board)

        boards: list[tuple[BoardData, ValidKeys|None, int]] = []
        for move in [ValidKeys.UP, ValidKeys.DOWN, ValidKeys.LEFT, ValidKeys.RIGHT]:
            b, e = transiction_board(board, move)
            if b.score <= GAME_OVER_MOVE:
                boards.append((b, move, e))
                continue
            x, _, e = self._simulate_next_move(b, recurse_counter + 1)
            boards.append((x, move, e))

        return max(boards, key=lambda x: (x[0].score, x[2]))

    def _simulate_next_move_multiple(self, board: BoardData, recurse_counter: int) -> tuple[BoardData, ValidKeys|None, int]:
        if recurse_counter == self.num_of_simulations:
            return board, None, count_empty_positions(board.board)

        boards: list[tuple[BoardData, ValidKeys|None, int]] = []
        num_simulations = 3 if recurse_counter == 0 or recurse_counter == 1 else 1
        for _ in range(num_simulations):
            for i, move in enumerate([ValidKeys.UP, ValidKeys.DOWN, ValidKeys.LEFT, ValidKeys.RIGHT]):
                b, e = transiction_board(board, move)
                if b.score <= GAME_OVER_MOVE:
                    if len(boards) <= i:
                        boards.append((b, move, e))
                    else:
                        tmp = boards[i]
                        b.score = (b.score + tmp[0].score) // 2
                        mean_empty_spots = (e + tmp[2]) // 2
                        boards[i] = (b, move, mean_empty_spots)
                    continue

                x, _, e = self._simulate_next_move_multiple(b, recurse_counter + 1)
                if len(boards) <= i:
                    boards.append((x, move, e))
                else:
                    tmp = boards[i]
                    x.score = (x.score + tmp[0].score) // 2
                    mean_empty_spots = (e + tmp[2]) // 2
                    boards[i] = (x, move, mean_empty_spots)

        return max(boards, key=lambda x: (x[0].score, x[2]))

# TODO: Resolver esse import circular depois
def transiction_board(data: BoardData, move: ValidKeys) -> tuple[BoardData, int]:
    new_board = move_board(data, move)
    if np.array_equal(new_board.board, data.board):
        return BoardData(new_board.board, INVALID_MOVE), INVALID_MOVE
    new_board.board, empty_positions = insert_value_at_random_empty_position(new_board.board)
    # if empty_positions == 0:
    #     return BoardData(new_board.board, GAME_OVER_MOVE)

    return new_board, empty_positions

# TODO: Refatorar pra remover a parte repetitiva de dentro dos ifs
def move_board(data: BoardData, move: ValidKeys) -> BoardData:
    new_board = np.zeros(data.board.shape)
    score = data.score
    if move == ValidKeys.LEFT:
        for i in range(data.board.shape[0]):
            new_row, row_score = slide_row_to_left(array_to_tuple(data.board[i]))
            new_board[i] = new_row
            score += row_score
    if move == ValidKeys.RIGHT:
        for i in range(data.board.shape[0]):
            # Aqui eu simplesmente inverto o array, e mando fazer o slide pra esquerda
            new_row, row_score = slide_row_to_left(array_to_tuple(data.board[i][::-1]))
            # E inverto de volta na hora de colocar no array
            new_board[i] = new_row[::-1]
            score += row_score
    if move == ValidKeys.UP:
        # Aqui eu transponho pra lidar com o slide pra esquerda (horizontalmente) quando o movimento deveria ser pra cima (verticalmente)
        transposed = data.board.T
        for i in range(data.board.shape[0]):
            new_row, row_score = slide_row_to_left(array_to_tuple(transposed[i]))
            new_board[i] = new_row
            score += row_score
        new_board = new_board.T
    if move == ValidKeys.DOWN:
        # Aqui transponho e inverto, como se fosse um movimento pra direita
        transposed = data.board.T
        for i in range(data.board.shape[0]):
            new_row, row_score = slide_row_to_left(array_to_tuple(transposed[i][::-1]))
            new_board[i] = new_row[::-1]
            score += row_score
        new_board = new_board.T

    # E por fim, retorno meu novo board
    return BoardData(new_board, score)

def array_to_tuple(array: np.ndarray) -> tuple:
    return tuple(array.tolist())

# TODO: mover essa função com otimização para o utils depois
@lru_cache(maxsize=None)
def slide_row_to_left(data: tuple) -> tuple[np.ndarray,int]:
    # Remove todos os valores zerados pra simplificar o trabalho, imagine [0, 2, 0, 2]
    # removendo os zeros, fica [2, 2], então fica muito mais obvio que um movimento pra esquerda gera o [4, 0, 0, 0]
    row = np.array(data)
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

def insert_value_at_random_empty_position(board: np.ndarray) -> tuple[np.ndarray, int]:
    # Aqui eu preciso verificar se existe algum espaço vazio, eu posso inserir o numero 2
    empty_positions = []
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i][j] == 0:
                empty_positions.append((i, j))

    if len(empty_positions) == 0:
        return board, 0

    np.random.seed(round(time.time() * 1000000) % 2 ** 32)
    np.random.shuffle(empty_positions)
    i, j = empty_positions[np.random.choice(len(empty_positions))]
    board[i][j] = cast(int, np.random.choice([2, 4], p=[0.9, 0.1]))
    return board, len(empty_positions) - 1
