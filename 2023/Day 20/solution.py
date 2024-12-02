from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import re


class PulseType(Enum):
    LOW = 0
    HIGH = 1


@dataclass
class Module:
    label: str
    outputs: list[str]

    def _get_output_pulse_type(
        self, input_: PulseType, origin_module_label: str
    ) -> PulseType:
        ...

    def is_in_original_state(self) -> bool:
        ...

    def get_output_pulses(
        self, input_: PulseType, origin_module_label: str
    ) -> tuple[PulseType, list[str]]:
        pulse_type = self._get_output_pulse_type(input_, origin_module_label)
        if pulse_type is None:
            return None
        return Pulse(pulse_type, self.label, self.outputs)


@dataclass
class BroadcasterModule(Module):
    def _get_output_pulse_type(self, input_: PulseType, _) -> PulseType:
        return input_

    def is_in_original_state(self) -> bool:
        return True


@dataclass
class FlipFlopModule(Module):
    def __init__(self, label: str, outputs: list[str]) -> None:
        super().__init__(label, outputs)
        self.is_on = False

    def _get_output_pulse_type(self, input_: PulseType, _) -> PulseType:
        if input_ == PulseType.HIGH:
            return None
        self.is_on = not self.is_on
        if self.is_on:
            return PulseType.HIGH
        return PulseType.LOW

    def is_in_original_state(self) -> bool:
        return not self.is_on


@dataclass
class Conjunction(Module):
    def __init__(self, label: str, inputs: set[str], outputs: list[str]):
        super().__init__(label, outputs)
        self.inputs = inputs
        self.highs = set()

    def _get_output_pulse_type(
        self, input_: PulseType, origin_module_label: str
    ) -> PulseType:
        if input_ == PulseType.HIGH:
            self.highs.add(origin_module_label)
        else:
            self.highs.discard(origin_module_label)

        if self.inputs == self.highs:
            return PulseType.LOW
        return PulseType.HIGH

    def is_in_original_state(self) -> bool:
        return len(self.highs) == 0


@dataclass
class Pulse:
    pulse_type: PulseType
    origin: str
    destinations: list[str]


def get_modules(raw_text: str) -> dict[str, Module]:
    module_pattern = re.compile(r"([%&]?)(\w+) -> ((?:\w+(?:, )?)+)")
    all_inputs = defaultdict(set)
    conjunction_matches = []
    modules = dict()
    for m in module_pattern.finditer(raw_text):
        outputs = m[3].split(", ")
        label = m[2]
        for o in outputs:
            all_inputs[o].add(label)
        if m[1] == "&":
            conjunction_matches.append(m)
        else:
            module_type = FlipFlopModule if m[1] == "%" else BroadcasterModule
            modules[label] = module_type(label, outputs)

    for m in conjunction_matches:
        modules[m[2]] = Conjunction(m[2], all_inputs[m[2]], m[3].split(", "))
        # print(m[2], all_inputs[m[2]])
    return modules


def main():
    with open(Path(__file__).resolve().parent / "Puzzle input.txt", "r") as data:
        modules = get_modules(data.read())

    pulse_counts = []
    lows_total = 0
    highs_total = 0
    while True:
        low_pulses = 1
        high_pulses = 0
        pulses = deque(
            [modules["broadcaster"].get_output_pulses(PulseType.LOW, "button")]
        )
        while len(pulses) != 0:
            pulse: Pulse = pulses.popleft()
            for dest in pulse.destinations:
                if pulse.pulse_type == PulseType.HIGH:
                    high_pulses += 1
                else:
                    low_pulses += 1

                if dest in modules:
                    output_pulse = modules[dest].get_output_pulses(
                        pulse.pulse_type, pulse.origin
                    )
                    if output_pulse is not None:
                        pulses.append(output_pulse)
        pulse_counts.append((low_pulses, high_pulses))
        lows_total += low_pulses
        highs_total += high_pulses

        if len(pulse_counts) >= 1000:
            break

    loop_length = len(pulse_counts)
    loop_count = 1000 // loop_length
    loop_pos = 1000 % loop_length

    lows_total *= loop_count
    highs_total *= loop_count
    for ix in range(loop_pos):
        low, high = pulse_counts[ix]
        lows_total += low
        highs_total += high

    print(f"Part 1: The product is {lows_total * highs_total}!")


if __name__ == "__main__":
    main()
