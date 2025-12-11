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
        **chests_item().lookup(100000),
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


def extend_dexsanity_hints(world: "PokemonBWWorld", hint_data: dict[int, dict[int, str]]) -> None:
    from .data.locations.encounters.region_connections import connection_by_region
    from .data.pokemon.pokedex import by_number
    from .data.pokemon.species import by_name

    if world.options.dexsanity == 0:
        return

    places_for_location: dict[str, set[str]] = {}

    # Wild encounter
    for slot, entry in world.wild_encounter.items():
        catching_place = connection_by_region[slot[:slot.rindex(" ")]]
        pokemon = by_number[entry.species_id[0]]
        location = "Pokédex - " + pokemon
        if location not in places_for_location:
            places_for_location[location] = set()
        places_for_location[location].add(catching_place)

    # Static encounter
    for static_slot, entry in world.static_encounter.items():
        catching_place = static_slot[:static_slot.rfind("Encounter")]
        pokemon = by_number[entry.species_id[0]]
        location = "Pokédex - " + pokemon
        if location not in places_for_location:
            places_for_location[location] = set()
        places_for_location[location].add(catching_place)

    # Trade encounter
    for trade_slot, entry in world.trade_encounter.items():
        catching_place = trade_slot[:trade_slot.rindex("Encounter")]
        pokemon = by_number[entry.species_id[0]]
        location = "Pokédex - " + pokemon
        if location not in places_for_location:
            places_for_location[location] = set()
        places_for_location[location].add(catching_place)

    # Evolutions
    for species, data in by_name.items():
        for evo in data.evolutions:
            location = "Pokédex - " + by_name[evo[2]].dex_name
            if location not in places_for_location:
                places_for_location[location] = set()
            places_for_location[location].add(f"Evolving {data.dex_name}")

    # Create hint strings
    # For every existing Dexsanity location
    for loc in world.get_locations():
        if loc.name in places_for_location:
            hint_data[world.player][loc.address] = ", ".join(places_for_location[loc.name])
    # For every catchable/obtainable encounter
    for location, places in places_for_location.items():
        loc_id = world.location_name_to_id[location]
        hint_data[world.player][loc_id] = ", ".join(places)