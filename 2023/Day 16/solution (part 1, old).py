from pathlib import Path
from collections import deque

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


class Move:
    def __init__(self, x, y, direction) -> None:
        self.x = x
        self.y = y
        self.direction = direction


class Grid:
    def __init__(self, grid: list) -> None:
        self.grid = [[Tile(ch) for ch in row] for row in grid]
        self.width = len(grid[0])
        self.height = len(grid)
        self.traversed_cells = 0

    def get_next_moves(self, move: Move):
        x = move.x
        y = move.y

        if x != -1:
            if move.direction in (tile := self.grid[y][x]).traversed_directions:
                return ()

            if tile.traversed_directions == "":
                self.traversed_cells += 1
            tile.traversed_directions += move.direction

        match move.direction:
            case "U":
                y -= 1
            case "D":
                y += 1
            case "L":
                x -= 1
            case "R":
                x += 1
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return ()

        return (
            Move(x, y, dir)
            for dir in self.grid[y][x].get_next_directions(move.direction)
        )


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        grid = Grid(data.read().splitlines())

    move_stack = deque([Move(-1, 0, "R")])

    while len(move_stack) != 0:
        move = move_stack.pop()
        move_stack.extend(grid.get_next_moves(move))

    print(f"Part 1: The number of energised cells is {grid.traversed_cells}!")
