def get_calibration_value(sequence: str):
    first = None
    last = None
    for char in sequence:
        if char.isdigit():
            if first == None:
                first = char
            last = char
    return int(f"{first}{last}")


def get_calibration_value_advanced(sequence):
    first = get_first_digit_advanced(sequence, reverse=False)
    last = get_first_digit_advanced(sequence, reverse=True)
    return int(f"{first}{last}")


digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_first_digit_advanced(sequence: str, reverse):
    characters_so_far = ""
    sequence_range = (
        range(len(sequence)) if not reverse else range(len(sequence) - 1, -1, -1)
    )
    for ix in sequence_range:
        char = sequence[ix]
        characters_so_far = (
            characters_so_far + char if not reverse else char + characters_so_far
        )
        if char.isdigit():
            return char
        else:
            for key in digits.keys():
                if key in characters_so_far:
                    return digits[key]


if __name__ == "__main__":
    with open("Puzzle input.txt", "r") as data:
        sequences = data.read().splitlines()
    total = 0
    total_advanced = 0
    for sequence in sequences:
        total += get_calibration_value(sequence)
        total_advanced += get_calibration_value_advanced(sequence)
    print(f"Part 1: The total comes out to {total}!")
    print(f"Part 2: The total comes out to {total_advanced}!")
