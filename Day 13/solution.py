from pathlib import Path
import re


class ReflectedGrid:
    def __init__(self, rows) -> None:
        self._rows = rows
        self._columns = self._transpose(rows)
        self.height = len(self._rows)
        self.width = len(self._columns)

    def _transpose(self, grid):
        transposed = [""] * len(grid[0])
        for row in grid:
            for ix, char in enumerate(row):
                transposed[ix] += char
        return transposed

    def _has_reflection(self, index, lines):
        top = index
        bottom = index + 1
        height = len(lines)
        while top >= 0 and bottom < height:
            if lines[top] != lines[bottom]:
                return False
            top -= 1
            bottom += 1
        return True

    def has_horizontal_reflection(self, index):
        return self._has_reflection(index, self._rows)

    def has_vertical_reflection(self, index):
        return self._has_reflection(index, self._columns)

    def _has_smudged_reflection(self, index, lines):
        top = index
        bottom = index + 1
        height = len(lines)
        found_smudged_line = False
        while top >= 0 and bottom < height:
            if lines[top] != lines[bottom]:
                if found_smudged_line:
                    return False
                if not self._could_be_smudge(lines[top], lines[bottom]):
                    return False
                found_smudged_line = True
            top -= 1
            bottom += 1
        return found_smudged_line

    def has_smudged_horizontal_reflection(self, index):
        return self._has_smudged_reflection(index, self._rows)

    def has_smudged_vertical_reflection(self, index):
        return self._has_smudged_reflection(index, self._columns)

    @staticmethod
    def _could_be_smudge(line, reflection):
        found_smudge = False
        for char, ref in zip(line, reflection):
            if char != ref:
                if found_smudge:
                    return False
                found_smudge = True
        return found_smudge


def get_score(grid: ReflectedGrid) -> int:
    for ix in range(grid.height - 1):
        if grid.has_horizontal_reflection(ix):
            return 100 * (ix + 1)
    for ix in range(grid.width - 1):
        if grid.has_vertical_reflection(ix):
            return ix + 1


# This code repetition is bad but it's a bit awkward to combine this.
def get_smudged_score(grid: ReflectedGrid) -> int:
    for ix in range(grid.height - 1):
        if grid.has_smudged_horizontal_reflection(ix):
            return 100 * (ix + 1)
    for ix in range(grid.width - 1):
        if grid.has_smudged_vertical_reflection(ix):
            return ix + 1


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        grids = [
            ReflectedGrid(m[0].splitlines())
            for m in re.finditer(r"(?:[#.]+\n)+[#.]+", data.read())
        ]

    total = sum(get_score(grid) for grid in grids)
    smudged_total = sum(get_smudged_score(grid) for grid in grids)
    print(f"Part 1: The total is {total}!")
    print(f"Part 2: The total is {smudged_total}!")
