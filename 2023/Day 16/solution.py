from dataclasses import dataclass
from pathlib import Path


class Tile:
    direction_maps = {
        ".": lambda d: d,
        "|": lambda d: d if d in "UD" else "UD",
        "-": lambda d: d if d in "LR" else "LR",
        "/": lambda d: "UR".replace(d, "") if d in "UR" else "LD".replace(d, ""),
        "\\": lambda d: "UL".replace(d, "") if d in "UL" else "RD".replace(d, ""),
    }

    def __init__(self, character) -> None:
        self.character = character
        self.get_next_directions = Tile.direction_maps[character]
        self.traversed_directions = ""


@dataclass(frozen=True)
class Move:
    x: int
    y: int
    directions: str


cache = dict()


def get_cells_until_forks(move: Move) -> tuple:
    if move in cache:
        return cache[move]

    next_moves = set()
    visited_cells = set()
    for dir_ in move.directions:
        x = move.x
        y = move.y
        next_dirs = dir_
        hit_wall = False
        while len(next_dirs) == 1 and not hit_wall:
            match next_dirs:
                case "U":
                    y -= 1
                case "D":
                    y += 1
                case "L":
                    x -= 1
                case "R":
                    x += 1
            if x < 0 or x >= width or y < 0 or y >= height:
                hit_wall = True
            else:
                visited_cells.add(new_cell := grid[y][x])
                next_dirs = new_cell.get_next_directions(next_dirs)

        if not hit_wall:
            visited_cells.remove(new_cell)
            next_moves.add(Move(x, y, next_dirs))

    cache[move] = (visited_cells, next_moves)
    return cache[move]


def get_energised_cell_count(starting_move: Move) -> int:
    move_stack = set([starting_move])
    visited_cells = set()
    while len(move_stack) != 0:
        move = move_stack.pop()
        if 0 <= move.x < width and 0 <= move.y < height:
            # This condition is True except for the starting cells which are outside the grid.
            if (start_cell := grid[move.y][move.x]) in visited_cells:
                continue
            visited_cells.add(start_cell)

        new_cells, new_moves = get_cells_until_forks(move)
        visited_cells.update(new_cells)
        move_stack.update(new_moves)
    return len(visited_cells)


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt") as data:
        grid = [[Tile(ch) for ch in row] for row in data.read().splitlines()]

    height = len(grid)
    width = len(grid[0])

    part_one_total = get_energised_cell_count(Move(-1, 0, "R"))
    max_total = 0
    for row in range(height):
        max_total = max(max_total, get_energised_cell_count(Move(-1, row, "R")))
        max_total = max(max_total, get_energised_cell_count(Move(width, row, "L")))
    for col in range(width):
        max_total = max(max_total, get_energised_cell_count(Move(col, -1, "D")))
        max_total = max(max_total, get_energised_cell_count(Move(col, height, "U")))

    print(f"Part 1: The number of energised cells is {part_one_total}!")
    print(f"Part 2: The maximum number of energised cells is {max_total}!")
