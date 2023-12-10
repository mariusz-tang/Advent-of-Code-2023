import re as regex

limits = {"red": 12, "green": 13, "blue": 14}


def possible(groups):
    return not any(int(count) > limits[colour] for count, colour in groups)


def get_power(groups):
    minima = {colour: 0 for colour in limits.keys()}
    for count, colour in groups:
        if minima[colour] < int(count):
            minima[colour] = int(count)
    power = 1
    for minimum in minima.values():
        power *= minimum
    return power


if __name__ == "__main__":
    with open("Puzzle input.txt", "r") as data:
        games_groups = [[match.groups() for match in regex.finditer(r"(\d+) (red|green|blue)", game)] for game in data.read().splitlines()]
    possible_games_total = sum([ix + 1 for ix, _ in filter(lambda pair : possible(pair[1]), enumerate(games_groups))])
    powers_total = sum([get_power(groups) for groups in games_groups])
    print(f"Part 1: The total comes out to {possible_games_total}!")
    print(f"Part 2: The total comes out to {powers_total}!")