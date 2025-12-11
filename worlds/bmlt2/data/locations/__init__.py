from .ingame_items import chests_items
from typing import TYPE_CHECKING
from collections import ChainMap

if TYPE_CHECKING:
    from .. import AnyLocationData

all_item_locations: ChainMap[str, "AnyLocationData"] = ChainMap[str, "AnyLocationData"](
    chests_items.table
)