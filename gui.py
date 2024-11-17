import pygame
from pygame import Rect, mouse, Surface
from pygame.rect import RectType

from bot import Knowledge, Mistake, Node
from hexapawn import actions, BLACK, display, initial_state, result, terminal, utility, WHITE

ROWS = 3
GAP = 1
TILE_SIZE = 120
BOARD_WIDTH = ROWS * TILE_SIZE
BORDER_GAP = GAP * 50
DIMENSION = (BOARD_WIDTH + BORDER_GAP * 2,) * 2

COIN_SIZE = (100, 100)

DARK = (23, 41, 0)
TILE_COLOR = "yellow"
TILE_BORDER_THICKNESS = 2
BANNER_MESSAGE = "Press ENTER to Try Again!"
BANNER_COLOR = (255, 255, 0, 100)
BANNER_BORDER_RADIUS = 50
TEXT_COLOR = DARK
FONT_SIZE = 42

# Load and scale images
white_img = pygame.transform.scale(pygame.image.load(r"images\white.png"), COIN_SIZE)
black_img = pygame.transform.scale(pygame.image.load(r"images\black.png"), COIN_SIZE)

white_rect = white_img.get_rect()
black_rect = black_img.get_rect()

pygame.init()
screen = pygame.display.set_mode(DIMENSION)
font = pygame.font.Font(None, FONT_SIZE)


def fit_piece(box: Rect | RectType, piece: Rect | RectType) -> tuple[int, int]:
    """Centers a piece within a box."""
    tx, ty = box.topleft
    bx, _ = box.bottomright
    outer = bx - tx
    inner = piece.width
    offset = (outer - inner) // 2
    return tx + offset, ty + offset


def clicked_index() -> tuple[int, int]:
    """Returns the board index corresponding to the current mouse position."""
    x, y = mouse.get_pos()
    x, y = x - BORDER_GAP, y - BORDER_GAP
    return y // TILE_SIZE, x // TILE_SIZE


def is_white_pawn(board: list[list[str]], index: tuple[int, int]) -> bool:
    """Checks if a specific index contains a white pawn."""
    i, j = index
    return 0 <= i < ROWS and 0 <= j < ROWS and board[i][j] == WHITE


def tessellate(w: int, h: int) -> list[list[Rect]]:
    """Creates a grid of tiles on the screen."""
    start = BORDER_GAP
    stop = DIMENSION[0] - BORDER_GAP
    return [
        [
            pygame.draw.rect(
                screen,
                TILE_COLOR,
                (j, i, w - 2, h - 2),
                TILE_BORDER_THICKNESS,
            )
            for j in range(start, stop, h)
        ]
        for i in range(start, stop, w)
    ]


def locate_pawns(board: list[list[str]], table: list[list[Rect]]) -> list[tuple[Surface, Rect]]:
    """Locates pawns on the board and positions them on the screen."""
    pawns = []
    for i, row in enumerate(table):
        for j, tile in enumerate(row):
            if board[i][j] == WHITE:
                pawn = white_rect.copy()
                pawn.topleft = fit_piece(tile, pawn)
                pawns.append((white_img, pawn))
            elif board[i][j] == BLACK:
                pawn = black_rect.copy()
                pawn.topleft = fit_piece(tile, pawn)
                pawns.append((black_img, pawn))
    return pawns


def update_pawn_state(pawns: list[tuple[Surface, Rect]]) -> None:
    """Updates the positions of pawns on the screen."""
    for pawn_img, pawn_rect in pawns:
        screen.blit(pawn_img, pawn_rect.topleft)


def clicked_pawn(pawns: list[tuple[Surface, Rect]]) -> Rect:
    """Returns the pawn rect that was clicked."""
    x, y = mouse.get_pos()
    for _, pawn_rect in pawns:
        if pawn_rect.collidepoint(x, y):
            return pawn_rect
    raise AssertionError("No pawn was clicked.")


def review_reflect(knowledge: Knowledge, history: Node | None) -> None:
    """Reviews and reflects on mistakes during the game."""
    while history and knowledge.catch22(history.state):
        knowledge.notify(Mistake(history.state, history.action))
        history = history.parent
        print("Climbing up...")
    if history:
        knowledge.notify(Mistake(history.state, history.action))


def display_banner(message: str) -> None:
    """Displays a banner with a message on the screen, allowing for opacity adjustment."""
    banner_surface = pygame.Surface((DIMENSION[0], 100), pygame.SRCALPHA)

    pygame.draw.rect(
        banner_surface,
        BANNER_COLOR,
        banner_surface.get_rect(),
        border_radius=BANNER_BORDER_RADIUS,
    )

    text = font.render(message, True, TEXT_COLOR)
    text_rect = text.get_rect(center=(DIMENSION[0] // 2, DIMENSION[1] // 2))

    screen.blit(banner_surface, (0, DIMENSION[1] // 2 - 50))
    screen.blit(text, text_rect)
    pygame.display.flip()


def retry() -> bool:
    """Prompts the player to retry the game."""
    display_banner(BANNER_MESSAGE)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True


def play() -> None:
    """Main game loop."""
    game_board = initial_state(ROWS, ROWS)
    chance = [WHITE, BLACK]
    history = None
    knowledge = Knowledge()
    try_again = True

    table = tessellate(TILE_SIZE, TILE_SIZE)
    pawns = locate_pawns(game_board, table)
    dragging = False
    cursor_pawn = None
    pawn_selected = None
    running = True

    while running and try_again:
        if terminal(game_board, chance[0]):
            if utility(game_board, chance[0]) == WHITE:
                print("Reviewing the mistakes...")
                review_reflect(knowledge, history)
            display(game_board)
            try_again = retry()
            if try_again:
                game_board = initial_state(ROWS, ROWS)
                pawns = locate_pawns(game_board, table)
                chance = [WHITE, BLACK]
                history = None
            continue

        if chance[0] == WHITE:
            made_a_move = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and \
                        is_white_pawn(game_board, clicked_index()):
                    dragging = True
                    pawn_selected = clicked_index()
                    cursor_pawn = clicked_pawn(pawns)
                elif event.type == pygame.MOUSEMOTION and dragging:
                    cursor_pawn.topleft = (mouse.get_pos()[0] - 50, mouse.get_pos()[1] - 50)
                elif event.type == pygame.MOUSEBUTTONUP and dragging:
                    dragging = False
                    pawn_action = clicked_index()
                    if pawn_action in actions(game_board, WHITE).get(pawn_selected, []):
                        game_board = result(game_board, pawn_selected, pawn_action)
                        made_a_move = True
                    pawns = locate_pawns(game_board, table)

            if made_a_move:
                chance.reverse()
        else:
            for pawn, moves in actions(game_board, BLACK).items():
                for move in moves:
                    if not knowledge.is_mistake(game_board, [pawn, move]):
                        history = Node(game_board, history, [pawn, move])
                        game_board = result(game_board, pawn, move)
                        pawns = locate_pawns(game_board, table)
                        break
                else:
                    continue
                break
            chance.reverse()

        screen.fill(DARK)
        tessellate(TILE_SIZE, TILE_SIZE)
        update_pawn_state(pawns)
        pygame.display.flip()


if __name__ == "__main__":
    play()
    pygame.quit()
