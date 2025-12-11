from typing import TYPE_CHECKING
from ...items import BombermanLandTouch2Item

if TYPE_CHECKING:
    from ... import BombermanLandTouch2World


def generate_default(world: "BombermanLandTouch2World") -> list[BombermanLandTouch2Item]:
    from ...data.items.items import bombs, pieces, fillers

    items = [
        BombermanLandTouch2Item(name, data.classification(world), data.item_id, world.player)
        for name, data in bombs.items()
    ] + [
        BombermanLandTouch2Item(name, data.classification(world), data.item_id, world.player)
        for name, data in pieces.items()
    ] + [
        BombermanLandTouch2Item(name, data.classification(world), data.item_id, world.player)
        for name, data in fillers.items()
    ]

    return items
