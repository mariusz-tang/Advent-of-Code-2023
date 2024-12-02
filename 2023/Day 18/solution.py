from pathlib import Path
import re


class Move:
    directions = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}

    def __init__(self, x, y, direction, distance) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.distance = distance

    def __repr__(self) -> str:
        return f"[x={self.x}, y={self.y}, direction={self.direction}, distance={self.distance}]"

    def get_destination_from(self, x, y):
        direction = Move.directions[self.direction]
        x += direction[0] * self.distance
        y += direction[1] * self.distance
        return (x, y)


def get_moves(raw_text: str) -> tuple:
    moves1 = []
    moves2 = []
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    for m in re.finditer(r"([UDLR]) (\d+) \(#([a-z0-9]{6})\)", raw_text):
        moves1.append(move1 := Move(x1, y1, m[1], int(m[2])))
        x1, y1 = move1.get_destination_from(x1, y1)
        moves2.append(move2 := Move(x2, y2, "RDLU"[int(m[3][5])], int(m[3][0:5], 16)))
        x2, y2 = move2.get_destination_from(x2, y2)

    return (moves1, moves2)


def get_area(moves):
    area = 0
    move_count = len(moves)
    for ix, move in enumerate(moves):
        move: Move
        if not move.direction in "LR":
            continue
        width = move.distance - 1
        height = move.y

        if move.direction == "L":
            height += 1
            if moves[ix - 1].direction == "D":
                width += 1
            if moves[(ix + 1) % move_count].direction == "U":
                width += 1
        else:
            if moves[ix - 1].direction == "U":
                width += 1
            if moves[(ix + 1) % move_count].direction == "D":
                width += 1

        multiplier = 1 if move.direction == "L" else -1
        area += multiplier * height * width
    return area


def main():
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        moves1, moves2 = get_moves(data.read())

    print(f"Part 1: The area is {get_area(moves1)}!")
    print(f"Part 2: The area is {get_area(moves2)}!")


if __name__ == "__main__":
    main()
