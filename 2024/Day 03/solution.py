from pathlib import Path
import re


def main():
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        line = data.readline().rstrip()

    part_one_total = 0
    part_two_total = 0
    do = True
    for m in re.findall(r"(do\(\))|(don't\(\))|mul\((\d+),(\d+)\)", line):
        if m[0]:
            do = True
        elif m[1]:
            do = False
        else:
            part_one_total += int(m[2]) * int(m[3])
            if do:
                part_two_total += int(m[2]) * int(m[3])

    print(f"Part one: {part_one_total}")
    print(f"Part two: {part_two_total}")


if __name__ == "__main__":
    main()
