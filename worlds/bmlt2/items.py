from random import Random
from typing import TYPE_CHECKING, Any
from collections import ChainMap

from BaseClasses import Item

if TYPE_CHECKING:
    from . import BombermanLandTouch2World
    from .data import AnyItemData

all_items_view: ChainMap[str, "AnyItemData"] | None = None


class BombermanLandTouch2Item(Item):
    game = 'Bomberman Land Touch! 2'


def generate_item(name: str, world: "BombermanLandTouch2World") -> BombermanLandTouch2Item:
    global all_items_view

    if all_items_view is None:
        from .data.items import all_items_dict_view
        all_items_view = all_items_dict_view

    data = all_items_view[name]
    # Item id from lookup table is used instead of id from data for safety purposes
    return BombermanLandTouch2Item(name, data.classification(world), world.item_name_to_id[name], world.player)


def get_item_lookup_table() -> dict[str, int]:
    from .data.items import all_items_dict_view

    return {name: data.item_id for name, data in all_items_dict_view.items()}


def get_main_item_pool(world: "BombermanLandTouch2World") -> list[BombermanLandTouch2Item]:
    from .generate.items import items

    return items.generate_default(world)


def generate_filler(world: "BombermanLandTouch2World") -> str:
    from .data.items import items

    main_nested = [
        items.bombs,
        items.pieces,
        items.fillers
    ]

    return random_choice_nested(
        world.random, [
            main_nested,
            main_nested,
        ]
    )


def random_choice_nested(random: Random, nested: list[str | list | dict]) -> Any:
    """Helper function for getting a random element from a nested list."""
    current: str | list | dict = nested
    while isinstance(current, list | dict):
        if isinstance(current, list):
            current = random.choice(current)
        else:
            current = random.choice(tuple(current.keys()))
    return current


def populate_starting_inventory(world: "BombermanLandTouch2World", items: list[BombermanLandTouch2Item]) -> None:
    pass


def place_locked_items(world: "BombermanLandTouch2World", items: list[BombermanLandTouch2World]) -> None:
    pass
