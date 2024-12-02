"""
Creates template files for Advent of Code in the same directory as this script.

Requires template.py to be in the same directory.
"""
from os import mkdir
from pathlib import Path


def main():
    path = Path(__file__).resolve().parent
    input_ = input(f"Create Advent of Code templates in {path}? (YES to confirm) ")
    if input_ != "YES":
        print(
            "Cancelled. Place this script in your chosen directory before running to change the suggested directory."
        )
        input("Press ENTER to exit.")
        exit()

    try:
        for ix in range(25):
            dir_name = path / f"Day {ix + 1:02d}"
            mkdir(dir_name)
            open(dir_name / "Test input.txt", "x").close()
            open(dir_name / "Puzzle input.txt", "x").close()
            with open(path / "template.py", "r") as template, open(
                dir_name / "solution.py", "x"
            ) as script:
                script.write(template.read())
        print(f"Created 25 directories in {path}.")
    except OSError as e:
        print(f"Failed to create all template files:")
        print(e)

    input("Press ENTER to exit.")


if __name__ == "__main__":
    main()
