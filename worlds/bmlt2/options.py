import logging
import typing
from copy import deepcopy
from dataclasses import dataclass

import settings
from BaseClasses import PlandoOptions
from Options import (Choice, PerGameCommonOptions, OptionSet, Range, Toggle,
                     PlandoTexts, OptionError, Option, OptionCounter, OptionDict, StartInventoryPool)

if typing.TYPE_CHECKING:
    from worlds.AutoWorld import World


class CasefoldOptionSet(OptionSet):
    valid_keys_casefold = True

    def __init__(self, value: typing.Iterable[str]):
        self.value = set(val.casefold() for val in value)
        super(OptionSet, self).__init__()  # To make it not call super.__init__? Not sure

    def __contains__(self, item: str):
        return item.casefold() in self.value

    def verify_keys(self) -> None:
        if self.valid_keys:
            dataset = set(word.casefold() for word in self.value)
            extra = dataset - set(key.casefold() for key in self._valid_keys)
            if extra:
                raise OptionError(
                    f"Found unexpected key {', '.join(extra)} in {getattr(self, 'display_name', self)}. "
                    f"Allowed keys: {self._valid_keys}."
                )


class ExtendedOptionCounter(OptionCounter):
    individual_min_max: dict[str, tuple[int, int]] = {}

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]):
        if not isinstance(data, dict):
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")
        for key in cls.valid_keys:
            if key not in data:
                if key in cls.default:
                    data[key] = cls.default[key]
                else:
                    data[key] = 0
        return cls(data)

    def verify(self, world: type["World"], player_name: str, plando_options: PlandoOptions) -> None:
        super().verify(world, player_name, plando_options)

        errors = []

        for key in self.value:
            if key in self.individual_min_max:
                _min, _max = self.individual_min_max[key]
                if not _min <= self.value[key] <= _max:
                    errors.append(f"{key}: {self.value[key]} not in range {_min} to {_max}")

        if len(errors) != 0:
            errors = [f"For option {getattr(self, 'display_name', self)} of player {player_name}:"] + errors
            raise OptionError("\n".join(errors))


class Bombs(Choice):
    """
    Select if bombs location are randomized
    """
    display_name: "Bombs"
    default = 0
    option_shuffle = 0
    option_vanilla = 1


@dataclass
class BombermanLandTouch2Options(PerGameCommonOptions):
    # General

    # Items, locations, and progression
    bombs: Bombs
