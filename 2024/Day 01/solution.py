from collections import defaultdict
from pathlib import Path


def main():
    left = list()
    right = list()
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        for line in data.readlines():
            l, r = line.split("   ")
            left.append(int(l))
            right.append(int(r))
        left.sort()
        right.sort()

    total = 0
    for l, r in zip(left, right):
        total += abs(l - r)
    print(f"Part one: {total}")

    total = 0
    right_dict = defaultdict(lambda: 0)
    for r in right:
        right_dict[r] += 1
    for l in left:
        total += l * right_dict[l]
    print(f"Part two: {total}")


if __name__ == "__main__":
    main()
