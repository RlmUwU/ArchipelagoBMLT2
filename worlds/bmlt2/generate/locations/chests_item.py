import collections
import itertools
from typing import TYPE_CHECKING

from ...locations import BombermanLandTouch2Location

if TYPE_CHECKING:
    from ... import BombermanLandTouch2World
    from BaseClasses import Region


def lookup(domain: int) -> dict[str, int]:
    from ...data.locations.ingame_items.items import bombs, pieces, stamps

    return {
        name: data.flag_id + domain for tab in (bombs, pieces, stamps) for name, data in tab.items()
    }


def create(world: "BombermanLandTouch2World") -> None:
    from ...data.locations.ingame_items.items import bombs, pieces, stamps

    for tab in (bombs, pieces, stamps):
        for name, data in tab.items():
            if data.inclusion_rule is None or data.inclusion_rule(world):
                r: "Region" = world.regions[data.region]
                l: BombermanLandTouch2Location = BombermanLandTouch2Location(world.player, name, world.location_name_to_id[name], r)
                l.progress_type = data.progress_type(world)
                if data.rule is not None:
                    l.access_rule = world.rules_dict[data.rule]
                r.locations.append(l)
