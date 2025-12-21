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

sunny_piece: ChainMap[str, "ItemData"] = ChainMap(
    {k: v for k, v in items.pieces.items() if "Sunny Piece" in k}
)

earth_piece: ChainMap[str, "ItemData"] = ChainMap(
    {k: v for k, v in items.pieces.items() if "Earth Piece" in k}
)

lightning_piece: ChainMap[str, "ItemData"] = ChainMap(
    {k: v for k, v in items.pieces.items() if "Lightning Piece" in k}
)

rainbow_piece: ChainMap[str, "ItemData"] = ChainMap(
    {k: v for k, v in items.pieces.items() if "Rainbow Piece" in k}
)

heart_piece: ChainMap[str, "ItemData"] = ChainMap(
    {k: v for k, v in items.pieces.items() if "Heart Piece" in k}
)

keys: ChainMap[str, "ItemData"] = ChainMap(
    {k: v for k, v in items.pieces.items() if "Key" in k}
)

all_pieces: ChainMap[str, "ItemData"] = ChainMap(
    star_piece,
    moon_piece,
    sunny_piece,
    earth_piece,
    lightning_piece,
    rainbow_piece,
    heart_piece,
    keys,
)


all_fillers: ChainMap[str, "ItemData"] = ChainMap(
    items.fillers
)

all_stamps: ChainMap[str, "ItemData"] = ChainMap(
    items.stamps
)

all_items_dict_view: ChainMap[str, "ItemData"] = ChainMap(
    items.bombs,
    items.pieces,
    items.fillers,
    items.stamps
)
