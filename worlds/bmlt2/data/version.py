
from typing import NamedTuple


class VersionCompatibility(NamedTuple):
    patch_file: tuple[int, int, int]
    patch_accept: tuple[int, int, int]
    rom: tuple[int, int, int]
    ut: tuple[int, int, int]
    ap_minimum: tuple[int, int, int]


# DO NOT put any number higher than 255
version: tuple[int, int, int] = (0, 4, 0)

compatibility: dict[tuple[int, int, int], VersionCompatibility] = {
    (0, 0, 1): VersionCompatibility((0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 0, 1), (0, 6, 4)),
}


def patch_file() -> tuple[int, int, int]:
    return compatibility[version].patch_file


def patch_accept(found: tuple[int, ...]) -> int:
    """0 = accepted, 1 = too new, -1 = too old"""
    if found > compatibility[version].patch_file:
        return 1
    elif found < compatibility[version].patch_accept:
        return -1
    else:
        return 0


def rom() -> tuple[int, int, int]:
    return compatibility[version].rom


def ut() -> tuple[int, int, int]:
    return compatibility[version].ut


def ap_minimum() -> tuple[int, int, int]:
    return compatibility[version].ap_minimum