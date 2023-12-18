from pathlib import Path
import re as regex


class Interval:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"[{self.start}, {self.end})"


class MapInterval(Interval):
    def __init__(self, start, end, offset) -> None:
        super().__init__(start, end)
        self.offset = offset


def get_map(raw_string: str):
    intervals = [line.split() for line in raw_string.splitlines()]

    def map_(num: int) -> int:
        for interval in intervals:
            dest_start, src_start, src_range = map(lambda n: int(n), interval)
            if num >= src_start and num - src_start < src_range:
                return num - src_start + dest_start
        return num

    return map_


def get_map_intervals(raw_string: str):
    raw_intervals = [line.split() for line in raw_string.splitlines()]
    map_intervals = []
    for interval in raw_intervals:
        dest_start, src_start, src_range = map(lambda n: int(n), interval)
        map_intervals.append(
            MapInterval(
                start=src_start,
                end=src_start + src_range,
                offset=dest_start - src_start,
            )
        )
    map_intervals.sort(key=lambda interval: interval.start)
    return map_intervals


def get_transformed_intervals(src_intervals, map_intervals):
    result_intervals = []
    for src in src_intervals:
        start = src.start
        need_to_add_end = True
        for map_ in map_intervals:
            if map_.start <= src.start and map_.end >= src.end:
                result_intervals.append(
                    Interval(src.start + map_.offset, src.end + map_.offset)
                )
                need_to_add_end = False
                break
            elif map_.end >= src.end:
                if map_.start > src.end:
                    break
                result_intervals.append((Interval(start, map_.start)))
                result_intervals.append(
                    (Interval(map_.start + map_.offset, src.end + map_.offset))
                )
                need_to_add_end = False
                break
            elif map_.end > start:
                if map_.start > start:
                    result_intervals.append((Interval(start, map_.start)))
                    result_intervals.append(
                        (Interval(map_.start + map_.offset, map_.end + map_.offset))
                    )
                else:
                    result_intervals.append(
                        (Interval(start + map_.offset, map_.end + map_.offset))
                    )
                start = map_.end
        if need_to_add_end:
            result_intervals.append(Interval(start, src.end))
    return result_intervals


def get_minimum_seed_location(seeds, maps):
    min_location = None
    for seed in seeds:
        location = get_seed_location(seed, maps)
        if min_location is None or location < min_location:
            min_location = location
    return min_location


def get_seed_location(seed, maps):
    for map_ in maps:
        seed = map_(seed)
    return seed


if __name__ == "__main__":
    with open(Path(__file__).resolve().parent / "Puzzle input.txt") as data:
        raw_splits = regex.split(r"\n\n.+map:\n", data.read())

    seeds_part_one = list(
        map(
            lambda seed: int(seed),
            regex.search(r"(?:\d+\s?)+", raw_splits[0]).group(0).split(),
        )
    )

    intervals_part_two = list(
        map(
            lambda x: Interval(int(x.group(1)), int(x.group(1)) + int(x.group(2))),
            regex.finditer(r"(\d+) (\d+)", raw_splits[0]),
        )
    )

    maps = []
    map_interval_sets = []
    for map_string in raw_splits[1:]:
        maps.append(get_map(map_string))
        map_interval_sets.append(get_map_intervals(map_string))

    min_location_part_one = get_minimum_seed_location(seeds_part_one, maps)

    for interval_set in map_interval_sets:
        intervals_part_two = get_transformed_intervals(intervals_part_two, interval_set)
    min_location_part_two = min([interval.start for interval in intervals_part_two])

    print(f"Part 1: The lowest location number is {min_location_part_one}!")
    print(f"Part 2: The lowest location number is now {min_location_part_two}!")
