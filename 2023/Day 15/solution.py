from pathlib import Path
import re


class Instruction:
    def __init__(self, raw_text: str) -> None:
        self.raw_text = raw_text
        match = re.match(r"(\w+)(=\d|-)", raw_text)
        self.label = match[1]
        self.is_remove = match[2] == "-"
        if not self.is_remove:
            self.focal_length = int(match[2][1])
        self.target_box = hashed(self.label)


class Lens:
    def __init__(self, label: str, focal_length: int) -> None:
        self.label = label
        self.focal_length = focal_length


def hashed(string):
    hash = 0
    for char in string:
        hash = (17 * (hash + ord(char))) % 256
    return hash


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        instructions = [Instruction(instr) for instr in data.read().split(",")]

    hash_total = sum(hashed(instr.raw_text) for instr in instructions)
    print(f"Part 1: The total is {hash_total}!")

    boxes = [[] for _ in range(256)]
    for instr in instructions:
        box = boxes[instr.target_box]
        target_lens = next((lens for lens in box if lens.label == instr.label), None)
        if not instr.is_remove:
            if target_lens != None:
                target_lens.focal_length = instr.focal_length
            else:
                box.append(Lens(instr.label, instr.focal_length))
        elif target_lens != None:
            box.remove(target_lens)

    focusing_power = 0
    for box_num, box in enumerate(boxes):
        for slot, lens in enumerate(box):
            focusing_power += (box_num + 1) * (slot + 1) * lens.focal_length
    print(f"Part 2: The focusing power is {focusing_power}!")
