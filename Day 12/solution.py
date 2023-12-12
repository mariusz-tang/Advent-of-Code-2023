import re


class Nonorow:
    def __init__(self, springs, groups):
        self.springs = springs
        self.groups = list(map(int, groups))
        self.index_limits = self._get_index_limits()
    
    def __len__(self):
        return len(self.springs)
    
    def __getitem__(self, index):
        return self.springs[index]
    
    def _get_index_limits(self):
        limits = []
        current_limit = len(self)
        for grp_size in reversed(self.groups):
            limits.append(current_limit - grp_size)
            current_limit -= grp_size + 1
            
        return list(reversed(limits))
    
    def has_room_for_group(self, size, position):
        if len(self) < size + position:
            return False
        if position > 0 and self[position - 1] == "#":
            return False
        if (end_ix := position + size) != len(self) and self[end_ix] == "#":
            return False
        for ix in range(position, size + position):
            if self[ix] == ".":
                return False
        return True


def get_total_arrangements(row: Nonorow) -> int:
    total = 0
    def check_possible(group_ix, position):
        if not row.has_room_for_group(row.groups[group_ix], position):
            return
        if group_ix + 1 == len(row.groups):
            if not "#" in row.springs[position + row.groups[group_ix] + 1:]:
                # There must not be any springs left after the final group
                nonlocal total
                total += 1
            return
        
        next_starting_position = position + row.groups[group_ix] + 1
        next_limit = row.index_limits[group_ix + 1]
        if next_limit < next_starting_position:
            return
        
        for ix in range(next_starting_position, next_limit + 1):
            check_possible(group_ix + 1, ix)
            if row[ix] == "#":
                # We must not skip over any broken springs
                return
        return
    
    for ix in range(0, row.index_limits[0] + 1):
        check_possible(0, ix)
    return total


if __name__ == "__main__":
    with open("Puzzleinput.txt", "r") as data:
        rows = [Nonorow(m[1], m[2].split(",")) for m in re.finditer(r"([#?.]+) ((?:\d+,)*\d)", data.read())]

    totals = [get_total_arrangements(row) for row in rows]
    total_arrangements = sum(totals)
    for ix, total in enumerate(totals):
        print(rows[ix].springs, rows[ix].groups, total)
    print(f"Part 1: The total number of arrangements is {total_arrangements}!")
