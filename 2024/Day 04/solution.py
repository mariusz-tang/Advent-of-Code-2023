from pathlib import Path


class WordSearch:
    def __init__(self, lines):
        self.letters = lines
        self.width = len(lines[0]) - 1  # Do not count the ending newline.
        self.height = len(lines)

    def find_word_count(self, word):
        count = 0
        for x_dir in (-1, 0, 1):
            for y_dir in (-1, 0, 1):
                if x_dir == y_dir == 0:
                    continue

                for x in range(self.width):
                    for y in range(self.height):
                        if self.word_exists_in_place(word, x, y, x_dir, y_dir):
                            count += 1

        return count

    def word_exists_in_place(self, word, x, y, x_dir, y_dir):
        offset = len(word) - 1
        if (
            x + x_dir * offset < 0
            or x + x_dir * offset >= self.width
            or y + y_dir * offset < 0
            or y + y_dir * offset >= self.height
        ):
            return False

        for ix, letter in enumerate(word):
            if self.letters[y + y_dir * ix][x + x_dir * ix] != letter:
                return False

        return True

    def find_x_mas_count(self):
        count = 0
        for x in range(self.width - 2):
            for y in range(self.height - 2):
                if (
                    self.letters[y + 1][x + 1] != "A"
                    or self.letters[y][x] == self.letters[y + 2][x + 2]
                ):
                    continue

                s_count = 0
                m_count = 0
                for x_diff in (0, 2):
                    for y_diff in (0, 2):
                        letter = self.letters[y + y_diff][x + x_diff]
                        if letter == "S":
                            s_count += 1
                        if letter == "M":
                            m_count += 1

                if s_count == m_count == 2:
                    count += 1

        return count


def main():
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        word_search = WordSearch(data.readlines())

    print(f"Part one: {word_search.find_word_count("XMAS")}")
    print(f"Part two: {word_search.find_x_mas_count()}")


if __name__ == "__main__":
    main()
