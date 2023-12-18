from pathlib import Path


class Schematic:
    def __init__(self, raw_text: str) -> None:
        self._grid = [[char for char in row] for row in raw_text.splitlines()]
        self._asterisk_values = {}
        self._numbers = self._get_numbers()

    def _get_numbers(self):
        numbers = []
        for rowIx, row in enumerate(self._grid):
            sequence = ""
            for colIx, char in enumerate(row):
                if char.isdigit():
                    sequence += char
                elif sequence != "":
                    number = Schematic._Number(colIx - len(sequence), rowIx, sequence)
                    if self._check_number_for_symbol(number):
                        numbers.append(number)
                    sequence = ""
            if sequence != "":
                number = Schematic._Number(colIx + 1 - len(sequence), rowIx, sequence)
                if self._check_number_for_symbol(number):
                    numbers.append(number)
        return numbers

    def _check_number_for_symbol(self, number):
        result = False
        for x, y in [
            (x, y)
            for x in range(number.x - 1, number.x + number.length + 1)
            for y in [number.y - 1, number.y + 1]
        ] + [(number.x - 1, number.y), (number.x + number.length, number.y)]:
            char = self._get_character_at_position(x, y)
            if not char.isdigit() and char != ".":
                result = True
                if char == "*":
                    self._handle_asterisk(x, y, number.number)
        return result

    def _get_character_at_position(self, x, y):
        if x < 0 or y < 0 or y >= len(self._grid) or x >= len(self._grid[y]):
            return "."
        return self._grid[y][x]

    def _handle_asterisk(self, x, y, number):
        key = f"{x} {y}"
        if key not in self._asterisk_values:
            self._asterisk_values[key] = []
        self._asterisk_values[key].append(number)

    def get_sum_of_numbers(self):
        return sum([num.number for num in self._numbers])

    def get_gear_sum(self):
        gears = filter(lambda values: len(values) == 2, self._asterisk_values.values())
        return sum([gear[0] * gear[1] for gear in gears])

    class _Number:
        def __init__(self, x, y, number: str) -> None:
            self.x = x
            self.y = y
            self.number = int(number)
            self.length = len(number)


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        schematic = Schematic(data.read())
    print(f"Part 1: The total comes out to {schematic.get_sum_of_numbers()}!")
    print(f"Part 2: The total comes out to {schematic.get_gear_sum()}!")
