from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class PartGroup:
    starts: tuple
    ends: tuple
    instr: str

    def get_total(self):
        total = 1
        for s, e in zip(self.starts, self.ends):
            total *= e - s + 1
        return total


class Part:
    categories_pattern = re.compile(r"([xmas])=(\d+)")

    def __init__(self, raw_text) -> None:
        self.categories = {
            m[1]: int(m[2]) for m in Part.categories_pattern.finditer(raw_text)
        }

    def get_total(self):
        return sum(v for v in self.categories.values())

    def __getitem__(self, index):
        return self.categories[index]


class Instruction:
    operators = {">": lambda x, y: x > y, "<": lambda x, y: x < y}

    def __init__(self, category, operator, limit, output) -> None:
        self.category = category
        self.cat_ix = "xmas".index(self.category)
        self.check_match = Instruction.operators[operator]
        self.limit = int(limit)
        self.output = output

    def evaluate(self, part):
        return self.check_match(part[self.category], self.limit)

    def evaluate_tuple(self, part):
        return self.check_match(part[self.cat_ix], self.limit)


class Workflow:
    instr_pattern = re.compile(r"(\w+)(>|<)(\d+):(\w+)")
    final_pattern = re.compile(r"(\w+)}")

    def __init__(self, raw_text) -> None:
        self.instructions = [
            Instruction(m[1], m[2], m[3], m[4])
            for m in Workflow.instr_pattern.finditer(raw_text)
        ]
        self.end = Workflow.final_pattern.search(raw_text)[1]

    def evaluate(self, part):
        for instr in self.instructions:
            if instr.evaluate(part):
                return instr.output
        return self.end

    def evaluate_group(self, group: PartGroup):
        results = set()
        for instr in self.instructions:
            bottom_in = instr.evaluate_tuple(group.starts)
            top_in = instr.evaluate_tuple(group.ends)
            if bottom_in == top_in:
                if top_in:
                    results.add(PartGroup(group.starts, group.ends, instr.output))
                    return results
            elif bottom_in:
                lower_break = Workflow._replace_tuple_index(
                    group.ends, instr.cat_ix, instr.limit - 1
                )
                upper_break = Workflow._replace_tuple_index(
                    group.starts, instr.cat_ix, instr.limit
                )
                results.add(PartGroup(group.starts, lower_break, instr.output))
                group = PartGroup(upper_break, group.ends, group.instr)
            else:
                lower_break = Workflow._replace_tuple_index(
                    group.ends, instr.cat_ix, instr.limit
                )
                upper_break = Workflow._replace_tuple_index(
                    group.starts, instr.cat_ix, instr.limit + 1
                )
                results.add(PartGroup(upper_break, group.ends, instr.output))
                group = PartGroup(group.starts, lower_break, group.instr)
        results.add(PartGroup(group.starts, group.ends, self.end))
        return results

    @staticmethod
    def _replace_tuple_index(tuple_, replacement_index, new_value):
        new = []
        for ix, existing_value in enumerate(tuple_):
            if ix != replacement_index:
                new.append(existing_value)
            else:
                new.append(new_value)
        return tuple(new)


def should_accept_part(workflows, part, input_):
    result = workflows[input_].evaluate(part)
    if result == "A":
        return True
    if result == "R":
        return False
    return should_accept_part(workflows, part, result)


def main():
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        workflows_raw, parts_raw = data.read().split("\n\n")

    label_pattern = re.compile(r"\w+")
    workflows = {
        label_pattern.match(wf)[0]: Workflow(wf) for wf in workflows_raw.splitlines()
    }

    total = 0
    for p in parts_raw.splitlines():
        part = Part(p)
        if should_accept_part(workflows, part, "in"):
            total += part.get_total()

    print(f"Part 1: The total is {total}!")

    total = 0
    groups = {PartGroup((1, 1, 1, 1), (4000, 4000, 4000, 4000), "in")}
    while len(groups) != 0:
        group = groups.pop()
        if group.instr == "A":
            total += group.get_total()
        elif group.instr != "R":
            groups.update(workflows[group.instr].evaluate_group(group))

    print(f"Part 2: The total is {total}!")


if __name__ == "__main__":
    main()
