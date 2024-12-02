from pathlib import Path
import re


class Nonorow:
    def __init__(self, springs, groups):
        self.springs = springs
        self.length = len(self.springs)
        self.groups = list(map(int, groups))
        self.index_limits = self._get_index_limits()

    def _get_index_limits(self):
        limits = []
        current_limit = self.length
        for grp_size in reversed(self.groups):
            limits.append(current_limit - grp_size)
            current_limit -= grp_size + 1

        return list(reversed(limits))

    def has_room_for_group(self, size, position):
        if self.length < (end_ix := position + size):
            return False
        if end_ix != self.length and self.springs[end_ix] == "#":
            return False
        if position > 0 and self.springs[position - 1] == "#":
            return False
        for ix in range(position, end_ix):
            if self.springs[ix] == ".":
                return False
        return True


def get_total_arrangements(row: Nonorow) -> int:
    cache = dict()

    def get_total_possibilities(group_ix, position):
        if not row.has_room_for_group(row.groups[group_ix], position):
            return 0
        if group_ix + 1 == len(row.groups):
            if not "#" in row.springs[position + row.groups[group_ix] + 1 :]:
                # There must not be any springs left after the final group
                return 1
            return 0

        next_starting_position = position + row.groups[group_ix] + 1
        next_limit = row.index_limits[group_ix + 1]
        if next_limit < next_starting_position:
            return 0

        total = 0
        for ix in range(next_starting_position, next_limit + 1):
            total += get_total_possibilities_cached(group_ix + 1, ix)
            if row.springs[ix] == "#":
                # We must not skip over any broken springs
                break
        return total

    def get_total_possibilities_cached(group_ix, position):
        key = (group_ix, position)
        if not key in cache:
            cache[key] = get_total_possibilities(group_ix, position)
        return cache[key]

    total_arrangements = 0
    for ix in range(0, row.index_limits[0] + 1):
        total_arrangements += get_total_possibilities_cached(0, ix)
        if row.springs[ix] == "#":
            # We must not skip over any broken springs
            break
    return total_arrangements


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        matches = re.finditer(r"([#?.]+) ((?:\d+,)*\d+)", data.read())

    rows = []
    part_two_rows = []
    for m in matches:
        springs = m[1]
        groups = m[2].split(",")
        rows.append(Nonorow(springs, groups))

        springs = "?".join(([springs] * 5))
        groups = groups * 5
        part_two_rows.append(Nonorow(springs, groups))

    total_arrangements = sum(get_total_arrangements(row) for row in rows)
    part_two_total_arrangements = sum(
        get_total_arrangements(row) for row in part_two_rows
    )

    print(f"Part 1: The total number of arrangements is {total_arrangements}!")
    print(f"Part 2: The total number of arrangements is {part_two_total_arrangements}!")
