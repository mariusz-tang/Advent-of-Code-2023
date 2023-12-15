from pathlib import Path


# Taken from my solution to Day 13
def transpose(grid):
    transposed = [""] * len(grid[0])
    for row in grid:
        for ix, char in enumerate(row):
            transposed[ix] += char
    return transposed


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        grid = data.read().splitlines()

    total = 0
    height = len(grid)
    grid = transpose(grid)
    for column in grid:
        next_load = height
        for pos, char in enumerate(column):
            if char == "#":
                next_load = height - pos - 1
            elif char == "O":
                total += next_load
                next_load -= 1

    print(f"Part 1: The total load is {total}!")
