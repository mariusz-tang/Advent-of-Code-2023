from collections import Counter, defaultdict
from pathlib import Path


class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __hash__(self):
        return hash((self.left, self.right))


def main():

    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        numbered_rules = defaultdict(set)

        while (line := data.readline()) != "\n":
            l, r = line.rstrip().split("|")
            rule = Rule(l, r)
            numbered_rules[l].add(rule)
            numbered_rules[r].add(rule)

        part_one_total = 0
        part_two_total = 0
        while (line := data.readline().rstrip()) != "":
            relevant_rules = set()
            entry_indices = dict()
            entries = line.split(",")
            middle_entry = ""
            for index, entry in enumerate(entries):
                entry_indices[entry] = index
                relevant_rules |= numbered_rules[entry]
                if (index * 2) + 1 == len(entries):
                    middle_entry = entry

            relevant_rules = {
                rule
                for rule in relevant_rules
                if rule.left in entries and rule.right in entries
            }
            rule_broken = False
            for rule in relevant_rules:
                if entry_indices[rule.left] > entry_indices[rule.right]:
                    rule_broken = True
                    break

            if not rule_broken:
                part_one_total += int(middle_entry)
            else:
                # This works because every number is ordered against every other
                # number in the data.
                target = int((len(entries) - 1) / 2)
                encounters = Counter()
                firsts = Counter()
                total_encounters = len(entries) - 1
                for rule in relevant_rules:
                    encounters.update((rule.left, rule.right))
                    firsts[rule.left] += 1

                    if (
                        encounters[rule.left] == total_encounters
                        and firsts[rule.left] == target
                    ):
                        part_two_total += int(rule.left)
                        break
                    if (
                        encounters[rule.right] == total_encounters
                        and firsts[rule.right] == target
                    ):
                        part_two_total += int(rule.right)
                        break

        print(f"Part one: {part_one_total}")
        print(f"Part two: {part_two_total}")


if __name__ == "__main__":
    main()
