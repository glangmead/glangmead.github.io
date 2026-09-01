"""
CLASS 5 - GAMES, AND THE TREE OF GAME STATES
================================================================================

THE PROMPT
----------
Teach my beginners how a computer plays a game perfectly, using tic-tac-toe,
and make the TREE the star of the lesson rather than the code.

Build it in this order:
1. Represent a board. Use a tuple of nine cells so it can't be modified by
   accident - and say out loud that this is the lesson about values and
   references paying off.
2. The three rules of the game as three tiny functions: what moves are
   legal, what a move produces, and who has won.
3. Build an ACTUAL tree of GameNode objects from a near-finished position,
   and print it indented so they can see it. Small enough to read every node.
4. Then count the whole tree from an empty board and print how long it took.
   I want the number and the wall-clock time on screen.
5. Count DISTINCT positions as well as nodes, and use the gap between the two
   numbers to introduce the idea of remembering answers you've already worked
   out.
6. Minimax, explained as one sentence about the tree, then written. Then a
   perfect-vs-perfect game that ends in a draw, printed board by board.
7. Close with why this exact approach cannot work for chess, and what real
   engines do instead.

Rules: single file, only `time` and `functools` imported, runs in a few
seconds, no pygame, no input() - it should play itself so it can run
unattended in class.

================================================================================
"""

import time
from functools import lru_cache


# ======================================================== 1. Representing a board
# Nine cells in reading order:
#
#      0 | 1 | 2
#     ---+---+---
#      3 | 4 | 5
#     ---+---+---
#      6 | 7 | 8
#
# A TUPLE, not a list. Tuples cannot be changed after they're made. Every
# move therefore produces a NEW board and leaves the old one intact - which
# is exactly what a tree of positions needs, since the parent has to survive
# after you look at the child. A list here would let one branch of the search
# quietly corrupt another. This is the variables lesson, doing real work.
EMPTY = (" ",) * 9

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),      # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),      # columns
    (0, 4, 8), (2, 4, 6),                 # diagonals
]


def show(board, indent=""):
    """Print a board as three rows."""
    for row in range(3):
        cells = board[row * 3:row * 3 + 3]
        print(indent + " " + " | ".join(c if c != " " else "." for c in cells))


# ================================================================ 2. The rules
def legal_moves(board):
    """Which squares are still empty."""
    return [i for i, cell in enumerate(board) if cell == " "]


def play(board, square, mark):
    """Return a NEW board with `mark` placed on `square`. Never modifies."""
    return board[:square] + (mark,) + board[square + 1:]


def winner(board):
    """'X', 'O', or None."""
    for a, b, c in LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_over(board):
    return winner(board) is not None or not legal_moves(board)


def other(mark):
    return "O" if mark == "X" else "X"


print("=== 1-2. A position and its legal moves ===")
position = ("X", "O", "X",
            " ", "O", " ",
            " ", " ", " ")
show(position)
print(f"legal moves: {legal_moves(position)}")
print(f"winner so far: {winner(position)}")


# ==================================================== 3. An actual tree, printed
print("\n=== 3. The tree of everything that can happen next ===")


class GameNode:
    """One position, plus every position reachable from it in one move."""

    def __init__(self, board, to_move):
        self.board = board
        self.to_move = to_move
        self.children = []          # filled in by build_tree

    def __repr__(self):
        return f"<GameNode {''.join(self.board)} {self.to_move} to move>"


def build_tree(board, to_move):
    """Build the whole tree below this position. Recursion: a function that
    calls itself on a smaller piece of the same problem. It stops because
    every move fills a square, so every branch runs out."""
    node = GameNode(board, to_move)
    if is_over(board):
        return node                             # a leaf: the game ended here
    for square in legal_moves(board):
        child = build_tree(play(board, square, to_move), other(to_move))
        node.children.append(child)
    return node


def print_tree(node, depth=0):
    indent = "    " * depth
    result = winner(node.board)
    if result:
        label = f"{result} wins"
    elif is_over(node.board):
        label = "draw"
    else:
        label = f"{node.to_move} to move"
    # dots instead of spaces so the empty squares are visible
    flat = "".join(c if c != " " else "." for c in node.board)
    print(f"{indent}{flat}   {label}")
    for child in node.children:
        print_tree(child, depth + 1)


# Start from a position with only three squares left, so the whole tree fits
# on screen. Read it top to bottom: each indent is one move deeper.
nearly_done = ("X", "O", "X",
               "X", "O", "O",
               " ", " ", " ")
print("starting from:")
show(nearly_done)
print("\nthe complete tree below it (indentation = depth):\n")

root = build_tree(nearly_done, "X")
print_tree(root)


def count_nodes(node):
    return 1 + sum(count_nodes(child) for child in node.children)


def count_leaves(node):
    if not node.children:
        return 1
    return sum(count_leaves(child) for child in node.children)


print(f"\nthat tree: {count_nodes(root)} positions, {count_leaves(root)} finished games")


# ============================================== 4. The whole tree, from empty
print("\n=== 4. The same tree, from an empty board ===")


def count_all(board, to_move):
    """Count every position in the tree without keeping any of them."""
    if is_over(board):
        return 1
    return 1 + sum(
        count_all(play(board, square, to_move), other(to_move))
        for square in legal_moves(board)
    )


start = time.time()
total = count_all(EMPTY, "X")
elapsed = time.time() - start
print(f"{total:,} positions, counted in {elapsed:.2f} seconds")

# Where that number comes from: 9 choices, then 8, then 7... 9! = 362,880
# complete games, plus every partial position along the way, minus the
# branches that stop early because somebody already won.


# ================================================== 5. The same position, twice
print("\n=== 5. How many of those are actually DIFFERENT? ===")


@lru_cache(maxsize=None)
def count_distinct_below(board, to_move):
    """Same count, but @lru_cache remembers each board it has already seen.
    A position reached by X-then-O is the same position as O-then-X, and the
    plain count above worked it out twice."""
    if is_over(board):
        return 1
    return 1 + sum(
        count_distinct_below(play(board, square, to_move), other(to_move))
        for square in legal_moves(board)
    )


start = time.time()
count_distinct_below(EMPTY, "X")
cached_time = time.time() - start
distinct = count_distinct_below.cache_info().currsize

print(f"{total:,} positions in the tree")
print(f"{distinct:,} of them are distinct boards")
print(f"the tree revisits the same board about {total / distinct:.0f}x on average")
print(f"and with the cache, the walk took {cached_time:.3f} seconds")

# That trick has a name - memoisation - and it is the difference between a
# program that finishes and one that doesn't. The tree is a picture of what
# COULD happen. The distinct positions are what actually exists. Whenever a
# search feels impossibly large, ask first whether it's re-solving the same
# thing over and over.


# ==================================================================== 6. Minimax
print("\n=== 6. Playing perfectly ===")

# One sentence: a position is worth whatever the best move from it leads to,
# assuming your opponent also plays their best move.
#
# Score from X's point of view: +1 X wins, -1 O wins, 0 draw. X picks the
# child with the highest score; O picks the child with the lowest. So the
# scores bubble UP from the finished games at the bottom of the tree.


@lru_cache(maxsize=None)
def score(board, to_move):
    """What this position is worth to X, with both sides playing perfectly."""
    champion = winner(board)
    if champion == "X":
        return 1
    if champion == "O":
        return -1
    if not legal_moves(board):
        return 0

    outcomes = [
        score(play(board, square, to_move), other(to_move))
        for square in legal_moves(board)
    ]
    return max(outcomes) if to_move == "X" else min(outcomes)


def best_move(board, to_move):
    """The move leading to the best outcome for whoever is to move."""
    choose = max if to_move == "X" else min
    return choose(
        legal_moves(board),
        key=lambda square: score(play(board, square, to_move), other(to_move)),
    )


print("Every opening move, scored (+1 = X wins, 0 = draw, -1 = O wins):")
NAMES = {1: "X wins", 0: "draw", -1: "O wins"}
for square in legal_moves(EMPTY):
    value = score(play(EMPTY, square, "X"), "O")
    print(f"  square {square}: {value:>2}   ({NAMES[value]})")
print("Every first move is a draw. Tic-tac-toe is a solved, boring game -")
print("and now you have proved it rather than been told it.")

print("\nA whole game, both sides perfect:")
board = EMPTY
to_move = "X"
turn = 0
while not is_over(board):
    turn += 1
    square = best_move(board, to_move)
    board = play(board, square, to_move)
    print(f"\nmove {turn}: {to_move} takes square {square}")
    show(board, indent="  ")
    to_move = other(to_move)

result = winner(board)
print(f"\nresult: {result + ' wins' if result else 'draw'}")


# ==============================================================================
# WHY THIS DOESN'T SCALE - AND WHAT REAL ENGINES DO
# ------------------------------------------------------------------------------
# Tic-tac-toe:   ~550,000 positions.        Counted above, in under a second.
# Checkers:      ~10^20 positions.          Solved in 2007, after 18 years.
# Chess:         ~10^45 positions.          More than there are atoms in the
#                                           Earth. Will never be counted.
# Go (19x19):    ~10^170.                   Beyond comment.
#
# Same tree, same minimax. The only thing that changed is the size. So real
# engines do three things this program doesn't:
#   1. Stop early. Look ten moves ahead, not to the end, and GUESS what the
#      position is worth. That guess is the "evaluation function", and it is
#      where all the craft lives.
#   2. Skip branches. Alpha-beta pruning: once you know a branch is worse
#      than one you've already checked, stop reading it. Same answer, a
#      fraction of the work.
#   3. Remember. The @lru_cache above, industrialised.
# AlphaGo's contribution was to learn step 1 from data instead of being told
# it by experts. Everything else in this file it still does.
#
# WHAT TO NOTICE
# ------------------------------------------------------------------------------
# - A "game" is four functions: what's legal, what a move does, who won, and
#   how good is this. Everything else is search. Change those four and this
#   program plays Connect Four or Nim.
# - Recursion is just "the tree, walked". build_tree, count_all and score are
#   the same three-line shape: handle the ending, otherwise ask the children.
# - Tuples made this safe. With lists, one branch could corrupt another and
#   you'd never find out.
#
# CHANGE ONE LINE
# ------------------------------------------------------------------------------
# - Delete @lru_cache from score() and time it. Still fast - the game is
#   small. Now imagine the same deletion in a chess engine.
# - Make O play the FIRST legal move instead of the best one, and watch X
#   start winning. Perfect play only draws against perfect play.
# - Change LINES to require four in a row on a 4x4 board. What else breaks?
#
# ASK THE AI
# ------------------------------------------------------------------------------
# - "Add alpha-beta pruning to score() and count how many positions each
#    version looks at."
# - "Convert this to Nim: three piles, take any number from one pile, whoever
#    takes the last object wins. Keep the same four functions."
# - "My tree of game states is too big to fit in memory. What are my options?"
# ==============================================================================
