def part_one(schematic):
    total = 0
    for rowIx in range(len(schematic)):
        adjacent_rows = []
        if rowIx != 0:
            adjacent_rows.append(schematic[rowIx - 1])
        if rowIx + 1 < len(schematic):
            adjacent_rows.append(schematic[rowIx + 1])
        total += get_row_total(schematic[rowIx], adjacent_rows)
    return total


def get_row_total(row: str, adjacent_rows):
    total = 0
    pos = 0
    length = len(row)
    while pos < length:
        if row[pos].isdigit():
            sequence = row[pos]
            for nextIx in range(pos + 1, length):
                if nextIx < length and row[nextIx].isdigit():
                    sequence += row[nextIx]
                else:
                    break
            has_symbol = (pos > 0 and is_symbol(row[pos - 1])) or (pos + len(sequence) < len(row) and is_symbol(row[pos + len(sequence)]))
            if not has_symbol:
                for adj_row in adjacent_rows:
                    has_symbol = has_symbol or has_symbol_in_row_section(adj_row, pos - 1, pos + len(sequence))
            if has_symbol:
                total += int(sequence)
            pos += len(sequence)
        pos += 1
    return total


def has_symbol_in_row_section(row: str, start, end):
    for char in row[max(0, start) : min(len(row), end + 1)]:
        if is_symbol(char):
            return True
    return False


def is_symbol(char: str):
    return not (char.isdigit() or char == ".")


if __name__ == "__main__":
    with open("Puzzle input.txt", "r") as data:
        schematic = data.read().splitlines()
    print(f"Part 1: The total comes out to {part_one(schematic)}!")
