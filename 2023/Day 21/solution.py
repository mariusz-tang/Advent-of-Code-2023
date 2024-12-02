from pathlib import Path


def add_tuple(x: tuple, y: tuple) -> tuple:
    return (x[0] + y[0], x[1] + y[1])


def find_starting_position(grid: list[str]) -> tuple[int]:
    for ix, row in enumerate(grid):
        if "S" in row:
            return (ix, row.index("S"))


def get_bounds_checker(width, height):
    return lambda pos: 0 <= pos[1] < width and 0 <= pos[0] < height


def main():
    with open(Path(__file__).resolve().parent / "Test input.txt", "r") as data:
        grid = data.read().splitlines()

    width = len(grid[0])
    height = len(grid)
    within_bounds = get_bounds_checker(width, height)

    start = find_starting_position(grid)
    unit_directions = frozenset(((0, 1), (0, -1), (1, 0), (-1, 0)))
    visited_cells = set((start,))
    last_visited_cells = set((start,))
    even_visit_count = 1

    for i in range(64):
        new_cells = set()
        for cell in last_visited_cells:
            for dir_ in unit_directions:
                if (
                    within_bounds(new_cell := add_tuple(dir_, cell))
                    and grid[new_cell[0]][new_cell[1]] != "#"
                ):
                    new_cells.add(new_cell)
        if i % 2 == 1:
            even_visit_count += len(new_cells.difference(visited_cells))
        last_visited_cells = new_cells
        visited_cells.update(new_cells)

    print(f"Part 1: The total is {even_visit_count}!")

    visited_cells = set((start,))
    last_visited_cells = set((start,))
    even_visit_count = 1

    for i in range(500):
        new_cells = set()
        for cell in last_visited_cells:
            for dir_ in unit_directions:
                new_cell = add_tuple(dir_, cell)
                if grid[new_cell[0] % width][new_cell[1] % height] != "#":
                    new_cells.add(new_cell)
        if i % 2 == 1:
            even_visit_count += len(new_cells.difference(visited_cells))
        last_visited_cells = new_cells
        visited_cells.update(new_cells)

    print(f"Part 2: The total is {even_visit_count}!")

if __name__ == "__main__":
    main()
