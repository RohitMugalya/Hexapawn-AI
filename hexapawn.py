"""
This module provides utility functions for managing and manipulating the game state
of Hexapawn, a mxn grid strategy game. It defines functions for initializing the game board,
generating possible moves for each player, and evaluating the game state. The key functionality
includes state representation, move generation, result calculation, and
utility checks for win/loss conditions.

The following constants represent the different types of pieces:
    - WHITE: White player's pawn
    - BLACK: Black player's pawn
    - EMPTY: Empty space on the board
    - WHITE_JI: Symbol for White pawn in the display
    - BLACK_JI: Symbol for Black pawn in the display
    - EMPTY_JI: Symbol for empty space in the display

Functions:
    - initial_state(m: int, n: int) -> list[list[str]]:
        Initializes the Hexapawn board with the given dimensions (m x n),
        placing the white pawns on the last row and black pawns on the first row.

    - display(board: list[list[str]]) -> None:
        Displays the current board in a human-readable format using `tabulate`.

    - next_player(turn: str) -> str:
        Returns the opponent player based on the current turn.

    - actions(board: list[list[str]], turn: str) -> dict[tuple[int, int], list[tuple[int, int]]]:
        Generates all possible moves for the current player (White or Black),
        considering forward and diagonal moves.

    - result(board: list[list[str]],
             depart: tuple[int, int],
             dest: tuple[int, int]) -> list[list[str]]:
        Returns a new board state after applying a move from the
        'depart' position to the 'dest' position.

    - terminal(board: list[list[str]], turn: str) -> bool:
        Checks if the current game state is terminal,
        (i.e., if a player has won or if the game is trapped).

    - utility(board: list[list[str]], turn: str) -> str:
        Evaluates the current board state to determine the winner.
        Returns 'WHITE' or 'BLACK' based on the game result.
"""


import copy
from collections import defaultdict
from tabulate import tabulate

WHITE = "WHITE_PAWN"
BLACK = "BLACK_PAWN"
EMPTY = "EMPTY"

WHITE_JI = "W"
BLACK_JI = "B"
EMPTY_JI = " "

LOGOS = {
    WHITE: WHITE_JI,
    BLACK: BLACK_JI,
    EMPTY: EMPTY_JI,
}


def initial_state(m: int, n: int) -> list[list[str]]:
    """Creates the initial state of the board."""
    board = [[EMPTY for _ in range(n)] for _ in range(m)]
    for j in range(n):
        board[0][j] = BLACK
        board[m - 1][j] = WHITE
    return board


def display(board: list[list[str]]) -> None:
    """Displays the board in a grid format."""
    formatted_board = [
        [LOGOS[piece] for piece in row]
        for row in board
    ]
    print(tabulate(formatted_board, tablefmt="grid"))


def next_player(turn: str) -> str:
    """Returns the next player based on the current turn."""
    if turn == WHITE:
        return BLACK
    if turn == BLACK:
        return WHITE
    assert False, "Invalid player turn."


def actions(board: list[list[str]], turn: str) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """Generates possible moves for the given player's turn."""
    m, n = len(board), len(board[0])
    possible_moves = defaultdict(list)

    if turn == WHITE:
        direction, opponent = -1, BLACK
    elif turn == BLACK:
        direction, opponent = 1, WHITE
    else:
        assert False, "Invalid player turn."

    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            if piece != turn:
                continue

            forward = (i + direction, j)
            diag_left = (i + direction, j - 1)
            diag_right = (i + direction, j + 1)

            if 0 <= forward[0] < m and board[forward[0]][forward[1]] == EMPTY:
                possible_moves[(i, j)].append(forward)

            if 0 <= diag_left[0] < m and \
                    0 <= diag_left[1] < n and \
                    board[diag_left[0]][diag_left[1]] == opponent:
                possible_moves[(i, j)].append(diag_left)

            if 0 <= diag_right[0] < m and \
                    0 <= diag_right[1] < n and \
                    board[diag_right[0]][diag_right[1]] == opponent:
                possible_moves[(i, j)].append(diag_right)

    return dict(possible_moves)


def result(board: list[list[str]],
           depart: tuple[int, int],
           dest: tuple[int, int]) -> list[list[str]]:
    """Applies a move and returns the resulting board."""
    m, n = len(board), len(board[0])
    i, j = depart
    di, dj = dest
    assert 0 <= di < m and 0 <= dj < n, "Move out of board bounds."

    new_board = copy.deepcopy(board)
    new_board[di][dj] = new_board[i][j]
    new_board[i][j] = EMPTY
    return new_board


def terminal(board: list[list[str]], turn: str) -> bool:
    """Checks if the game has reached a terminal state."""
    white_reached_top = any(piece == WHITE for piece in board[0])
    black_reached_bottom = any(piece == BLACK for piece in board[-1])
    white_trapped = turn == WHITE and not actions(board, WHITE)
    black_trapped = turn == BLACK and not actions(board, BLACK)

    return white_reached_top or black_reached_bottom or white_trapped or black_trapped


def utility(board: list[list[str]], turn: str) -> str:
    """Evaluates the utility of the current board."""
    if any(piece == WHITE for piece in board[0]):
        return WHITE
    if any(piece == BLACK for piece in board[-1]):
        return BLACK

    if turn == BLACK and not actions(board, BLACK):
        return WHITE
    if turn == WHITE and not actions(board, WHITE):
        return BLACK

    assert False, "Utility calculation failed."
