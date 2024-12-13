from pathlib import Path


class Map:
    def __init__(self, lines):
        self.cells = lines
        self.width = len(lines[0])
        self.height = len(lines)

        self.x_dir = 0
        self.y_dir = -1

        for ix, line in enumerate(self.cells):
            if "^" not in line:
                continue
            self.y = ix
            self.x = line.index("^")
            # Mark starting position as visited.
            self.cells[ix] = self.cells[ix].replace("^", "X")
            break

    def _get_cell(self, x, y):
        return self.cells[y][x]
    
    def _get_current_cell(self):
        return self._get_cell(self.x, self.y)

    def _get_next_coords(self):
        return self.x + self.x_dir, self.y + self.y_dir

    def _coords_out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def get_number_of_cells_visited(self):
        # Count the guard's starting position.
        total = 1
        next_coords = self._get_next_coords()

        while not self._coords_out_of_bounds(*next_coords):
            if self._get_cell(*next_coords) == "#":
                # Turn 90 degrees clockwise.
                self.x_dir, self.y_dir = -self.y_dir, self.x_dir
            else:
                self.x, self.y = next_coords
                if self._get_current_cell() != "X":
                        total += 1
                        line = self.cells[self.y]
                        self.cells[self.y] = f"{line[:self.x]}X{line[self.x + 1:]}"
            next_coords = self._get_next_coords()
        
        return total

def main():
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        map = Map(data.readlines())
    
    print(f"Part one: {map.get_number_of_cells_visited()}")


if __name__ == "__main__":
    main()
