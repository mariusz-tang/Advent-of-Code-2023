from os import mkdir
from pathlib import Path


def main():
    path = Path(__file__).resolve().parent
    input_ = input(f"Create Advent of Code templates in {path}? (YES to confirm) ")
    if input_ != "YES":
        print(
            "Cancelled. Place this script from your chosen directory before running to change the suggested directory."
        )
        input("Press ENTER to exit.")
        exit()

    try:
        for ix in range(25):
            dir_name = path / f"Day {ix + 1}"
            mkdir(dir_name)
            with open(dir_name / "Test input.txt", "x"):
                pass
            with open(dir_name / "Puzzle input.txt", "x"):
                pass
            with open(dir_name / "solution.py", "x") as script:
                script.write(
                    """from pathlib import Path


def main():
    with open(Path(__file__).resolve().parent / "Test input.txt", "r") as data:
        pass  # Parse the data here
    # Solve the problem here


if __name__ == "__main__":
    main()
"""
                )
        with open(path / ".gitignore", "x") as gitignore:
            gitignore.write("*input.txt")
        print(f"Created 25 directories and .gitignore in {path}.")
    except OSError as e:
        print(f"Failed to create templates:")
        print(e)

    input("Press ENTER to exit.")


if __name__ == "__main__":
    main()
