from pathlib import Path
import re as regex


def get_possibilities_count(time, distance):
    count = 0
    for hold_time in range(time + 1):
        move_time = time - hold_time
        if move_time * hold_time > distance:
            count += 1
    return count


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt") as data:
        times = [int(match[0]) for match in regex.finditer(r"\d+", data.readline())]
        distances = [int(match[0]) for match in regex.finditer(r"\d+", data.readline())]
    
    product = 1
    for time, distance in zip(times, distances):
        product *= get_possibilities_count(time, distance)
    
    print(f"Part 1: The result is {product}!")

# For the second part we need to solve the quadratic inequality in a
#       a(x-a) > y
# for integer a, where a is the time spent holding the button, x is
# the time limit, and y is the distance to beat. The result is
#       |a - x/2| < sqrt((x/2)^2-y)
# If x is even, then the number of possible values for a (our answer)
# is floor(sqrt((x/2)^2-y)) * 2 + 1. Otherwise, it's
# floor(sqrt((x/2)^2-y) + 0.5) * 2.
# Due to the very small number of cases (1) I opted to do this calculation
# on my phone's calculator.

# Note: The above also applies to the first part but the the numbers
# are so small that it is not worth implementing compared to the
# relatively trivial method of trial-and-error.