from bot import Knowledge, Mistake, Node
from hexapawn import actions, BLACK, display, initial_state, result, terminal, utility, WHITE


CONTROLS: dict[str, tuple[int, int]] = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
}
M, N = 3, 3


def white_chance() -> list[tuple[int, int]]:
    """Handles the player's move input for the white pieces."""
    depart, dest = input("You: ").split()
    return [(int(depart[0]), int(depart[1])), (int(dest[0]), int(dest[1]))]


def display_flaws(mistakes: list[Mistake]) -> None:
    """Displays mistakes identified during the game."""
    print("The incorrect moves are:")
    for mistake in mistakes:
        display(mistake.configuration)
        print(f"{mistake.fault_action[0]} -> {mistake.fault_action[1]}")


def retry() -> bool:
    """Prompts the user to retry the game."""
    response = input("Try Again [Y/N]? ").strip().lower()
    return response == "y"


def review_reflect(knowledge: Knowledge, history: Node | None) -> None:
    """Analyzes and logs mistakes for reflection."""
    while history and knowledge.catch22(history.state):
        mistake = Mistake(history.state, history.action)
        knowledge.notify(mistake)
        history = history.parent
        print("Climbing up the game tree...")
    if history:
        knowledge.notify(Mistake(history.state, history.action))


def play() -> None:
    """Main function to handle the game loop."""
    game_board = initial_state(M, N)
    chance = [WHITE, BLACK]
    history = None
    knowledge = Knowledge()

    while True:
        display(game_board)

        if terminal(game_board, chance[0]):
            if utility(game_board, chance[0]) == WHITE:
                print("Reviewing the mistakes...")
                review_reflect(knowledge, history)

            if retry():
                game_board = initial_state(M, N)
                chance = [WHITE, BLACK]
                history = None
            else:
                break
            continue

        if chance[0] == WHITE:
            depart, dest = white_chance()
        else:
            possible_moves = actions(game_board, chance[0]).items()
            for pawn, moves in possible_moves:
                for move in moves:
                    if not knowledge.is_mistake(game_board, [pawn, move]):
                        depart, dest = pawn, move
                        break
                else:
                    continue
                break
            else:
                # Handle no valid moves case (shouldn't normally occur)
                depart, (dest, *_) = list(possible_moves)[0]
                assert False  # Shouldn't happen in a valid game

            history = Node(game_board, history, [depart, dest])

        game_board = result(game_board, depart, dest)
        print("*" * 30)
        chance.reverse()

    display_flaws(knowledge.mistakes)


if __name__ == "__main__":
    play()
