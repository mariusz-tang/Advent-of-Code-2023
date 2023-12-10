import re as regex


def get_match_count(card):
    match = regex.search(r"^Card +\d+: +((?: *\d+)+) \| +((?: *\d+)+)$", card)
    winning_numbers = regex.split(r" {1,2}", match.groups()[0])
    my_numbers = regex.split(r" {1,2}", match.groups()[1])
    matching_numbers = 0

    for num in my_numbers:
        if num in winning_numbers:
            matching_numbers += 1
    return matching_numbers


def part_one(cards):
    total = 0
    for card in cards:
        match_count = get_match_count(card)
        if match_count != 0:
            total += 2 ** (match_count - 1)
    return total


def part_two(cards):
    card_matches = []
    for card in cards:
        card_matches.append(get_match_count(card))
    
    copies = [1] * len(card_matches)
    for ix in range(len(card_matches)):
        current_count = copies[ix]
        current_matches = get_match_count(cards[ix])
        while current_matches > 0:
            if len(copies) > ix + current_matches:
                copies[ix + current_matches] += current_count
            current_matches -= 1
    return sum(copies)


if __name__ == "__main__":
    with open("Puzzle input.txt", "r") as data:
        cards = data.read().splitlines()
    print(f"Part 1: we have {part_one(cards)} points! :)")
    print(f"Part 2: we end up with {part_two(cards)} cards! :)")
