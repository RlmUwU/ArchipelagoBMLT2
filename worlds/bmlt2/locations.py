from typing import TYPE_CHECKING, Callable

from BaseClasses import Location, Region, CollectionState

if TYPE_CHECKING:
    from . import BombermanLandTouch2World
    from .data import RulesDict, ExtendedRule, AccessRule


class BombermanLandTouch2Location(Location):
    game = "Bomberman Land Touch! 2"


def get_location_lookup_table() -> dict[str, int]:
    from .generate.locations import chests_item

    return {
        **chests_item.lookup(100000),
    }


def get_regions(world: "BombermanLandTouch2World") -> dict[str, Region]:
    from .data.locations import regions

    return {
        name: Region(name, world.player, world.multiworld)
        for name in regions.region_list
    }


def create_rule_dict(world: "BombermanLandTouch2World") -> "RulesDict":
    from .data.locations.rules import extended_rules_list

    def f(r: "ExtendedRule") -> Callable[[CollectionState], bool]:
        return lambda state: r(state, world)

    return {rule: f(rule) for rule in extended_rules_list} | {None: None}


def create_and_place_locations(world: "BombermanLandTouch2World") -> None:
    from .generate.locations import chests_item
    chests_item.create(world)


def connect_regions(world: "BombermanLandTouch2World") -> None:
    from .data.locations import region_connections as gameplay_connections

    # Create gameplay region connections
    for name, data in gameplay_connections.connections.items():
        world.regions[data.exiting_region].connect(
            world.regions[data.entering_region], name, world.rules_dict[data.rule]
        )

    def combine_and(connection_rules: tuple["ExtendedRule", ...]) -> "AccessRule":
        def f(state) -> bool:
            for r in connection_rules:
                if not r(state, world):
                    return False
            return True
        return f


def cleanup_regions(regions: dict[str, Region]) -> None:
    to_remove = []
    for name, region in regions.items():
        if len(region.entrances) == 0 and region.name != "Menu":
            to_remove.append(name)
    for name in to_remove:
        regions.pop(name)


def count_to_be_filled_locations(regions: dict[str, Region]) -> int:
    count = 0
    for region in regions.values():
        for location in region.locations:
            if location.item is None:
                count += 1
    return count
