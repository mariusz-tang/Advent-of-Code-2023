from numpy import array as vector


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
        print(self._grid[y][x])
        return PipeGrid._connections[self._grid[y][x]]


def get_path_length(grid: PipeGrid, direction):
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
        length += 1
        if direction is None:
            return None
        if direction == "FINISH":
            return length


if __name__ == "__main__":
    with open("Puzzle input.txt", "r") as data:
        grid = PipeGrid(data.read().splitlines())

    distance = None
    for dir_ in "UDLR":
        if (result := get_path_length(grid, dir_)) is not None:
            distance = result / 2

    print(f"Part 1: The distance is {distance}!")
