from pathlib import Path
import re


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
        self.operator = Instruction.operators[operator]
        self.limit = int(limit)
        self.output = output

    def evaluate(self, part):
        return self.operator(part[self.category], self.limit)


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

if __name__ == "__main__":
    main()
