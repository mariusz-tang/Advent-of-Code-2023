from pathlib import Path
import re


def counter_clockwise_rotated(grid):
    transposed = [""] * len(grid[0])
    for row in grid:
        for ix, char in enumerate(row):
            transposed[ix] += char
    return reversed(transposed)


def get_load_after_north_tilt(grid):
    total = 0
    height = len(grid)
    grid = counter_clockwise_rotated(grid)
    for column in grid:
        next_load = height
        for pos, char in enumerate(column):
            if char == "#":
                next_load = height - pos - 1
            elif char == "O":
                total += next_load
                next_load -= 1
    return total


def cycled(grid):
    for _ in range(4):
        grid = counter_clockwise_rotated(grid)
        grid = left_tilted(grid)
    return grid


def left_tilted(grid):
    tilted_grid = []
    for row in grid:
        last_pos = -1
        round_rocks = 0
        new_row = ""
        for pos, char in enumerate(row):
            if char == "O":
                round_rocks += 1
            elif char == "#":
                new_row += "O" * round_rocks
                new_row += "." * (pos - 1 - last_pos - round_rocks)
                new_row += "#"
                last_pos = pos
                round_rocks = 0
        new_row += "O" * round_rocks
        new_row += "." * (len(row) - 1 - last_pos - round_rocks)
        tilted_grid.append(new_row)
    return tilted_grid


def get_load(grid):
    total = 0
    height = len(grid)
    for ix, row in enumerate(grid):
        total += (height - ix) * row.count("O")
    return total


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        # Flip the grid horizontally to account for rotating in the wrong direction
        grid = [line[::-1] for line in data.read().splitlines()]

    part_one_total = get_load_after_north_tilt(grid)
    print(f"Part 1: The total load is {part_one_total}!")

    encountered_sequences = []
    while True:
        grid = cycled(grid)
        if (sequence := "".join(grid)) in encountered_sequences:
            break
        encountered_sequences.append(sequence)

    loop_start = encountered_sequences.index(sequence)
    loop_length = len(encountered_sequences) - loop_start
    position_in_loop = (999_999_999 - loop_start) % loop_length
    grid_width = len(grid[0])
    grid = re.findall(
        rf"[.O#]{{{grid_width}}}", encountered_sequences[loop_start + position_in_loop]
    )
    print(f"Part 2: The load after 1,000,000,000 cycles is {get_load(grid)}!")
