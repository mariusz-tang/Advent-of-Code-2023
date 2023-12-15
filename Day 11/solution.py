from pathlib import Path


def get_transformed_galaxies(initial_image, expansion_rate):
    galaxies = []
    rows = len(initial_image)
    columns = len(initial_image[0])
    empty_rows = []

    non_empty_columns = set()
    for y in range(rows):
        row_is_empty = True
        for x in range(columns):
            if initial_image[y][x] == "#":
                galaxies.append([y, x])
                row_is_empty = False
                non_empty_columns.add(x)

        if row_is_empty:
            empty_rows.append(y)
    empty_columns = [col for col in range(columns) if not col in non_empty_columns]

    expanded_rows = get_expanded_dimension(rows, empty_rows, expansion_rate)
    expanded_columns = get_expanded_dimension(columns, empty_columns, expansion_rate)
    return [[expanded_rows[y], expanded_columns[x]] for y, x in galaxies]


def get_expanded_dimension(initial_count, empties, expansion_rate):
    expanded_dimension = []
    expansion = 0
    for ix in range(initial_count):
        expanded_dimension.append(ix + expansion)
        if ix in empties:
            expansion += expansion_rate
    return expanded_dimension


def get_manhattan_distance(lhs, rhs):
    return abs(lhs[0] - rhs[0]) + abs(lhs[1] - rhs[1])


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        image = data.read().splitlines()

    galaxies = get_transformed_galaxies(image, 1)
    galaxies_part_two = get_transformed_galaxies(image, 999_999)

    part_one_total = 0
    part_two_total = 0
    for l_ix in range(len(galaxies) - 1):
        for r_ix in range(l_ix, len(galaxies)):
            part_one_total += get_manhattan_distance(galaxies[l_ix], galaxies[r_ix])
            part_two_total += get_manhattan_distance(
                galaxies_part_two[l_ix], galaxies_part_two[r_ix]
            )

    print(f"Part 1: The total distance is {part_one_total}!")
    print(f"Part 2: The total distance is {part_two_total}!")
