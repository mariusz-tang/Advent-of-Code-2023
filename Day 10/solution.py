from numpy import array as vector
from pathlib import Path


class PipeGrid:
    units = {
        "U": vector([-1, 0]),
        "D": vector([1, 0]),
        "L": vector([0, -1]),
        "R": vector([0, 1]),
    }
    _connections = {
        "J": "UL",
        "F": "DR",
        "L": "UR",
        "7": "DL",
        "|": "UD",
        "-": "LR",
        ".": "",
        "S": "FINISH",
    }

    @staticmethod
    def get_opposite_direction(direction: str) -> str:
        if direction in "UD":
            return "UD".replace(direction, "")
        return "LR".replace(direction, "")

    def __init__(self, grid: list) -> None:
        self._grid = grid
        self.start = self._get_start_position()

    def _get_start_position(self) -> vector:
        for y in range(len(self._grid)):
            if "S" in self._grid[y]:
                x = self._grid[y].index("S")
                return vector([y, x])

    def get_connections_at(self, position: vector) -> str:
        y, x = position
        if y < 0 or y >= len(self._grid) or x < 0 or x >= len(self._grid[y]):
            return PipeGrid._connections["."]
        return PipeGrid._connections[self._grid[y][x]]

    def clean(self, path):
        """Remove all special cells which are not part of the path from the grid"""
        for y in range(len(self._grid)):
            row = ""
            for x in range(len(self._grid[y])):
                if (y, x) in path:
                    row += self._grid[y][x]
                else:
                    row += "."
            self._grid[y] = row
        self._start_character = self._get_start_character()

    def get_inner_cell_count(self):
        """Return the number of cells inside the path with a 'ray tracing'-like method"""
        count = 0
        for y in range(len(self._grid)):
            self._grid[y] = self._grid[y].replace("S", self._start_character)
            inside = False
            wall_start = None
            for x in range(len(self._grid[y])):
                if (char := self._grid[y][x]) == "." and inside:
                    count += 1
                elif char in "FL":
                    wall_start = char
                elif (
                    char == "|"
                    or (char == "J" and wall_start == "F")
                    or (char == "7" and wall_start == "L")
                ):
                    inside = not inside
        return count

    def _get_start_character(self):
        up = "D" in self.get_connections_at(self.start + vector([-1, 0]))
        down = "U" in self.get_connections_at(self.start + vector([1, 0]))
        right = "L" in self.get_connections_at(self.start + vector([0, 1]))
        if up:
            if right:
                return "L"
            if down:
                return "|"
            return "J"
        if right:
            if down:
                return "F"
            return "-"
        return "7"


def get_path_length(grid: PipeGrid, direction, path):
    def next_direction() -> str:
        connections = grid.get_connections_at(position)
        if connections == "FINISH":
            return "FINISH"

        from_dir = PipeGrid.get_opposite_direction(direction)
        if from_dir in connections:
            return connections.replace(from_dir, "")
        return None

    position = grid.start
    length = 0
    while True:
        position = position + PipeGrid.units[direction]
        direction = next_direction()
        path.append((position.item(0), position.item(1)))
        length += 1
        if direction is None:
            return None
        if direction == "FINISH":
            return length


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        grid = PipeGrid(data.read().splitlines())

    path = []
    distance = None
    for dir_ in "UDLR":
        path = []
        if (result := get_path_length(grid, dir_, path)) is not None:
            distance = int(result / 2)
            break

    grid.clean(path)
    inner_cells = grid.get_inner_cell_count()

    print(f"Part 1: The distance is {distance}!")
    print(f"Part 2: The number of inner cells is {inner_cells}!")
