from .ingame_items import items
from typing import TYPE_CHECKING
from collections import ChainMap

if TYPE_CHECKING:
    from .. import AnyLocationData, FlagLocationData

items_locations: ChainMap[str, "AnyLocationData"] = ChainMap[str, "AnyLocationData"](
    items.bombs,
)

pieces_location: ChainMap[str, "AnyLocationData"] = ChainMap[str, "AnyLocationData"](
    items.pieces
)

stamps_location: ChainMap[str, "AnyLocationData"] = ChainMap[str, "AnyLocationData"](
)
