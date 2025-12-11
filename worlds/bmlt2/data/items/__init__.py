from typing import TYPE_CHECKING
from collections import ChainMap

from . import items
from .items import bombs

if TYPE_CHECKING:
    from .. import ItemData, AnyItemData

all_bombs: ChainMap[str, "ItemData"] = ChainMap(
    items.bombs
)

all_pieces: ChainMap[str, "ItemData"] = ChainMap(
    items.pieces
)

all_fillers: ChainMap[str, "ItemData"] = ChainMap(
    items.fillers
)

all_items_dict_view: ChainMap[str, "ItemData"] = ChainMap(
    items.bombs,
    items.pieces
)
