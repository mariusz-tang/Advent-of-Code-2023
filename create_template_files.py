import os


current_dir = os.getcwd()
input_ = input(f"Create Advent of Code templates in directory {current_dir}? (YES to confirm) ")
if input_ != "YES":
    print("Cancelled. Run this script from your chosen directory to change the suggested directory.")
    input("Press ENTER to exit.")
    exit()

try:
    for ix in range(25):
        dir_name = f"Day {ix + 1}"
        os.mkdir(dir_name)
        with open(f"{dir_name}/Test input.txt", "x"): pass
        with open(f"{dir_name}/Puzzle input.txt", "x"): pass
        with open(f"{dir_name}/solution.py", "x") as script:
            script.write("""if __name__ == "__main__":
    with open("Test input.txt", "r") as data:
        pass  # Parse the data here
    # Solve the problem here
""")
    with open(".gitignore", "x") as gitignore:
        gitignore.write("*input.txt")
    print(f"Created 25 directories and .gitignore in {current_dir}.")
except OSError as e:
    print(f"Failed to create templates:")
    print(e)

input("Press ENTER to exit.")