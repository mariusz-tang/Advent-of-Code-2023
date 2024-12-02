from enum import Enum
from operator import attrgetter
from pathlib import Path
import re as regex


class Hand:
    class _HandType(Enum):
        FIVE_OF_A_KIND = 1
        FOUR_OF_A_KIND = 2
        FULL_HOUSE = 3
        THREE_OF_A_KIND = 4
        TWO_PAIR = 5
        ONE_PAIR = 6
        HIGH_CARD = 7

    _CARDS = "23456789TJQKA"

    def __init__(self, cards: str, bid) -> None:
        self._ordered_cards = cards
        self._type = Hand._get_hand_type(cards)
        self._type_with_wildcards = Hand._get_hand_type_with_wildcards(cards)
        self.bid = int(bid)
        self.sort_index = Hand._get_sort_index(self._type, self._ordered_cards, False)
        self.wildcard_sort_index = Hand._get_sort_index(
            self._type_with_wildcards, self._ordered_cards, True
        )

    @staticmethod
    def _get_sorted_cards(cards: str) -> list:
        return sorted(
            cards,  # Sort by number of occurences, then by value
            key=lambda c: -(cards.count(c) * len(Hand._CARDS) + Hand._CARDS.index(c)),
        )

    @staticmethod
    def _get_hand_type(cards: str) -> _HandType:
        sorted_cards = Hand._get_sorted_cards(cards)
        h_type = Hand._HandType
        first, second, third, fourth, fifth = sorted_cards
        if first == fifth:
            return h_type.FIVE_OF_A_KIND
        if first == fourth:
            return h_type.FOUR_OF_A_KIND
        if first == third:
            if fourth == fifth:
                return h_type.FULL_HOUSE
            return h_type.THREE_OF_A_KIND
        if first == second:
            if third == fourth:
                return h_type.TWO_PAIR
            return h_type.ONE_PAIR
        return h_type.HIGH_CARD

    @staticmethod
    def _get_sort_index(
        hand_type: _HandType, ordered_cards: str, use_wildcard_rules: bool
    ) -> int:
        card_values = Hand._CARDS if not use_wildcard_rules else "J23456789TQKA"
        base = len(card_values)
        max_ = base**5
        hand_values = [card_values.index(card) for card in ordered_cards]
        values_index = sum(
            ix * base**pos for pos, ix in enumerate(reversed(hand_values))
        )
        return values_index - max_ * hand_type.value

    @staticmethod
    def _get_hand_type_with_wildcards(cards: str) -> _HandType:
        if cards == "JJJJJ":
            return Hand._HandType.FIVE_OF_A_KIND
        most_occurences = 0
        most_common_value = None
        for value in Hand._CARDS:
            if value != "J" and (count := cards.count(value) > most_occurences):
                most_occurences = count
                most_common_value = value
        return Hand._get_hand_type(cards.replace("J", most_common_value))


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        hands = [
            Hand(match[1], match[2])
            for match in regex.finditer(r"([2-9TJQKA]{5}) (\d+)", data.read())
        ]

    hands.sort(key=attrgetter("sort_index"))
    total = sum((ix + 1) * hand.bid for ix, hand in enumerate(hands))
    hands.sort(key=attrgetter("wildcard_sort_index"))
    total_with_wildcards = sum((ix + 1) * hand.bid for ix, hand in enumerate(hands))
    print(f"Part 1: The total winnings are {total}!")
    print(f"Part 2: The total winnings are now {total_with_wildcards}!")
