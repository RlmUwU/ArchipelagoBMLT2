from typing import TYPE_CHECKING

from ...locations import BombermanLandTouch2Location
from BaseClasses import ItemClassification
from ...items import BombermanLandTouch2Item

if TYPE_CHECKING:
    from ... import BombermanLandTouch2World


def create(world: "BombermanLandTouch2World") -> None:

    location: BombermanLandTouch2Location
    regions = world.regions
    location = BombermanLandTouch2Location(world.player, "Finish", None, regions["Star Zone - End"])
    regions["Star Zone - End"].locations.append(location)
    item: BombermanLandTouch2Item = BombermanLandTouch2Item("Goal", ItemClassification.progression, None, world.player)
    location.place_locked_item(item)
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Goal", world.player)
