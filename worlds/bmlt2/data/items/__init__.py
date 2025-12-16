from typing import TYPE_CHECKING
from collections import ChainMap

from . import items
from .items import bombs

if TYPE_CHECKING:
    from .. import ItemData, AnyItemData

all_bombs: ChainMap[str, "ItemData"] = ChainMap(
    items.bombs
)

# Pieces
star_piece: ChainMap[str, "ItemData"] = ChainMap(
    {k: v for k, v in items.pieces.items() if "Star Piece" in k}
)

moon_piece: ChainMap[str, "ItemData"] = ChainMap(
    {k: v for k, v in items.pieces.items() if "Moon Piece" in k}
)

all_pieces: ChainMap[str, "ItemData"] = ChainMap(
    star_piece,
    moon_piece
)


all_fillers: ChainMap[str, "ItemData"] = ChainMap(
    items.fillers
)

all_items_dict_view: ChainMap[str, "ItemData"] = ChainMap(
    items.bombs,
    items.pieces,
    items.fillers,
)
