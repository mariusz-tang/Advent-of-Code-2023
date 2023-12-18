"""The strategy here will absolutely not work for part two"""

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Move:
    x: int
    y: int
    direction: str
    distance: int

    def get_connector(self) -> list:
        next_coord = [self.x, self.y]
        dim = 1 if self.direction in "UD" else 0
        dir = 1 if self.direction in "DR" else -1
        connector = []
        for _ in range(1, self.distance):
            next_coord[dim] += dir
            connector.append(list(next_coord))
        return connector

    def get_next_coordinate(self) -> list:
        next_coord = [self.x, self.y]
        dim = 1 if self.direction in "UD" else 0
        dir = 1 if self.direction in "DR" else -1
        next_coord[dim] += dir * self.distance
        return next_coord


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self._grid = [[" " for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

    def __getitem__(self, index: int) -> list:
        return self._grid[index]

    def __iter__(self):
        return iter(self._grid)


def main():
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        matches = re.finditer(r"([UDLR]) (\d+) \(#([a-z0-9]{6})\)", data.read())

    x = 0
    y = 0
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    moves = []
    for m in matches:
        moves.append(move := Move(x, y, m[1], int(m[2])))
        x, y = move.get_next_coordinate()
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    width = max_x - min_x + 1
    height = max_y - min_y + 1
    grid = Grid(width, height)

    for move in moves:
        move: Move
        grid[move.y - min_y][move.x - min_x] += move.direction
        for x, y in move.get_connector():
            grid[y - min_y][x - min_x] = "#"
        x, y = move.get_next_coordinate()
        grid[y - min_y][x - min_x] = move.direction + grid[y - min_y][x - min_x]

    count = 0
    for row in grid:
        inside = False
        last_corner = None
        for cell in row:
            if cell != " ":
                count += 1
                if cell == "#" and last_corner is None:
                    inside = not inside
                elif len(cell) == 3:
                    if last_corner is None:
                        last_corner = cell
                    else:
                        if not ("D" in (combined := cell + last_corner) and "U" in combined):
                            inside = not inside
                        last_corner = None
                        
            elif inside:
                count += 1

    print(f"Part 1: The total lava capacity is {count}!")

if __name__ == "__main__":
    main()
