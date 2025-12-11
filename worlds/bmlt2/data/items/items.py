from .. import ItemData
from .classification import *

bombs: dict[str, ItemData] = {
    "Default Bomb": ItemData(0x00004000, always_progression),
    "Soccer Bomb": ItemData(0x00004000, always_progression),
    "Basketbomb": ItemData(0x00010000, always_progression)
}

pieces: dict[str, ItemData] = {
    "Star Piece 1": ItemData(0x1, always_progression),
}

fillers: dict[str, ItemData] = {
    "Penny": ItemData(0x1, always_filler),
}