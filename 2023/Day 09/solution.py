from pathlib import Path
import re


def get_differences(sequence: list) -> list:
    result = []
    for ix in range(len(sequence) - 1):
        result.append(sequence[ix + 1] - sequence[ix])
    return result


def extrapolate(sequence: list) -> None:
    subsequences = []
    while True:
        subsequences.append(sequence)
        sequence = get_differences(sequence)
        if not any(elem != 0 for elem in sequence):
            subsequences.append(sequence)
            break

    subsequences.reverse()
    for ix in range(len(subsequences) - 1):
        subsequences[ix + 1].append(subsequences[ix + 1][-1] + subsequences[ix][-1])
        subsequences[ix + 1].insert(0, subsequences[ix + 1][0] - subsequences[ix][0])


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        sequences = [
            [int(m[0]) for m in re.finditer(r"-?\d+", line)]
            for line in data.read().splitlines()
        ]

    forwards_total = 0
    backwards_total = 0
    for seq in sequences:
        extrapolate(seq)
        forwards_total += seq[-1]
        backwards_total += seq[0]

    print(f"Part 1: The total comes out to {forwards_total}!")
    print(f"Part 2: The total comes out to {backwards_total}!")
