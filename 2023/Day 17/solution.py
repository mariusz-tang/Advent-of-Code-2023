from bisect import insort
from pathlib import Path


class Tile:
    def __init__(self, digit) -> None:
        self.cost = digit
        self.visits = []


class Grid:
    def __init__(self, raw_string: str) -> None:
        self.grid = [[Tile(int(ch)) for ch in row] for row in raw_string.splitlines()]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def __getitem__(self, index: int) -> list:
        return self.grid[index]


class Traverser:
    opposite_dir = {"U": "D", "R": "L", "D": "U", "L": "R"}

    def __init__(
        self, grid: Grid, x=0, y=0, total_cost=0, path_since_last_turn=""
    ) -> None:
        self.grid = grid
        self.x = x
        self.y = y
        self.total_cost = total_cost
        self.since_turn = path_since_last_turn

    def get_next_directions(self) -> str:
        available_directions = "ULDR"
        if self.since_turn != "":
            if len(self.since_turn) < type(self).min_straight:
                # Keep going straight if required
                return self.since_turn[0]
            # Do not go backwards
            available_directions = available_directions.replace(
                Traverser.opposite_dir[self.since_turn[0]], ""
            )
            if len(self.since_turn) == type(self).max_straight:
                # Do not go further in a straight line than allowed
                available_directions = available_directions.replace(
                    self.since_turn[0], ""
                )
        return available_directions

    def get_next_traversers(self) -> list:
        available_directions = self.get_next_directions()
        next_traversers = []
        for dir_ in available_directions:
            x = self.x
            y = self.y
            match dir_:
                case "U":
                    y -= 1
                case "D":
                    y += 1
                case "L":
                    x -= 1
                case "R":
                    x += 1
            if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
                continue

            tile: Tile = self.grid[y][x]
            if not dir_ in (new_path := self.since_turn):
                new_path = ""
            new_path += dir_

            # Do not revisit a cell if we have already been there in the same state
            if any(visit == new_path for visit in tile.visits):
                continue
            tile.visits.append(new_path)

            next_traversers.append(
                type(self)(self.grid, x, y, self.total_cost + tile.cost, new_path)
            )
        return next_traversers


class RegularCrucible(Traverser):
    min_straight = 0
    max_straight = 3


class UltraCrucible(Traverser):
    min_straight = 4
    max_straight = 10


def get_lowest_heat_loss(grid: Grid, crucible_type: type):
    move_queue = [crucible_type(grid, 0, 0, 0, "")]
    while len(move_queue) != 0:
        move: Traverser = move_queue.pop(0)
        if move.x + 1 == grid.width and move.y + 1 == grid.height:
            if (
                not crucible_type.min_straight
                <= len(move.since_turn)
                <= crucible_type.max_straight
            ):
                continue
            return move.total_cost
        for trav in move.get_next_traversers():
            trav: Traverser
            insort(move_queue, trav, key=lambda t: t.total_cost)
    return None


def main():
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        raw_text = data.read()
    # We need two grids because the Tile objects are modified during calculation
    part_one_minimum = get_lowest_heat_loss(Grid(raw_text), RegularCrucible)
    part_two_minimum = get_lowest_heat_loss(Grid(raw_text), UltraCrucible)
    print(f"Part 1: The least heat loss possible is {part_one_minimum}!")
    print(f"Part 2: The least heat loss possible is {part_two_minimum}!")


if __name__ == "__main__":
    main()
