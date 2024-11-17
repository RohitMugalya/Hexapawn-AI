"""
This module defines utility classes and functions for implementing a game-playing bot 
and tracking game states in the Hexapawn game. It provides the following functionalities:

1. **Node Class**:
   - Represents a node in the game tree, storing the current state, parent state, and action taken.
   - Enables traversal of the game tree to analyze the sequence of moves.

2. **Mistake Class**:
   - Represents a mistake as a combination of a board configuration and a faulty action.
   - Provides comparison capabilities for identifying repeated mistakes.

3. **Knowledge Class**:
   - Tracks known mistakes made during gameplay.
   - Evaluates configurations to detect deadlock situations ("Catch-22" scenarios).
   - Supports notifying and checking mistakes to enhance bot decision-making.

The module integrates with the `hexapawn` game engine for game state manipulation, 
action evaluation, and display rendering.

Example Usage:
    knowledge = Knowledge()
    mistake = Mistake(configuration, action)
    knowledge.notify(mistake)
    if knowledge.is_mistake(configuration, action):
        print("This move is a known mistake!")
"""
from typing import Self
from hexapawn import actions, BLACK, display


class Node:
    """Represents a state in the game tree."""
    def __init__(self, state: list[list[str]], parent: Self | None, action: list[tuple[int, int]]):
        self.state = state
        self.parent = parent
        self.action = action

    def __repr__(self):
        return f"Node(state={self.state}, parent={self.parent}, action={self.action})"

    def __str__(self):
        """Returns a readable string representation of the node and its ancestry."""
        output = []
        temp = self
        while temp:
            output.append(f"State:\n{temp.state}")
            output.append(f"Action: {temp.action}\n")
            temp = temp.parent
        return "\n".join(output)


class Mistake:
    """Represents a mistake, which is a configuration and a faulty action."""
    def __init__(self, configuration: list[list[str]], fault_action: list[tuple[int, int]]):
        self.configuration = configuration
        self.fault_action = fault_action

    def __eq__(self, other):
        if not isinstance(other, Mistake):
            return NotImplemented
        return (
            self.configuration == other.configuration and
            self.fault_action == other.fault_action
        )

    def __repr__(self):
        display(self.configuration)
        print(f"Faulty Action: {self.fault_action[0]} -> {self.fault_action[1]}")
        return "Mistake object"


class Knowledge:
    """Tracks and evaluates mistakes to improve gameplay."""
    def __init__(self):
        self.mistakes: list[Mistake] = []

    def notify(self, mistake: Mistake):
        """Adds a mistake to the knowledge base."""
        self.mistakes.append(mistake)

    def is_mistake(self, configuration: list[list[str]], action: list[tuple[int, int]]) -> bool:
        """Checks if a given configuration and action represent a known mistake."""
        return Mistake(configuration, action) in self.mistakes

    def catch22(self, configuration: list[list[str]]) -> bool:
        """Determines if the configuration is a deadlock situation for the player."""
        possible_moves = actions(configuration, BLACK)
        total_moves = sum(len(moves) for moves in possible_moves.values())
        fault_tally = sum(1 for mistake in self.mistakes if mistake.configuration == configuration)
        return total_moves - 1 == fault_tally
