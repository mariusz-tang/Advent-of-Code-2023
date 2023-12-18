from math import lcm
from pathlib import Path
import re as regex

# In hindsight, this should not work AT ALL if there is more than one start node
# I must have gotten extremely lucky with my map...
# EDIT: Turns out all of the puzzle inputs were made to loop such that LCM works
def find_step_count(node_map: dict, start_nodes: list, instructions: str, goal_condition) -> int:
    length = len(instructions)
    counts = []
    for node in start_nodes:
        ix = 0
        count = 0
        while not goal_condition(node):
            node = node_map[node][instructions[ix]]
            ix = (ix + 1) % length
            count += 1
        counts.append(count)
    return lcm(*counts)


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        instructions = regex.match(r"[RL]+", data.readline())[0]
        node_map = {
            m[1]: {"L": m[2], "R": m[3]}
            for m in regex.finditer(
                r"([\dA-Z]{3}) = \(([\dA-Z]{3}), ([\dA-Z]{3})\)", data.read()
            )
        }

    part_one_total = find_step_count(
        node_map, ["AAA"], instructions, lambda node: node == "ZZZ"
    )
    part_two_start_nodes = [node for node in node_map if node.endswith("A")]
    part_two_total = find_step_count(
        node_map, part_two_start_nodes, instructions, lambda node: node.endswith("Z")
    )

    print(f"Part 1: We reach the goal in {part_one_total} steps!")
    print(f"Part 2: We finish in {part_two_total} steps!")
