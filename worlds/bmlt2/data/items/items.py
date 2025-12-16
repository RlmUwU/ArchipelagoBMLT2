from .. import ItemData
from .classification import *

bombs: dict[str, ItemData] = {
    "Default Bomb": ItemData(114, always_progression),
    "Soccer Bomb": ItemData(115, always_progression),
    # "Basketbomb": ItemData(0x00010000, always_progression)
}

pieces: dict[str, ItemData] = {
    "Star Piece 1": ItemData(1, always_progression),
    "Star Piece 2": ItemData(2, always_progression),
    "Star Piece 3": ItemData(3, always_progression),
    "Star Piece 4": ItemData(4, always_progression),
    "Star Piece 5": ItemData(5, always_progression),
    "Star Piece 6": ItemData(6, always_progression),
    "Star Piece 7": ItemData(7, always_progression),
    "Star Piece 8": ItemData(8, always_progression),
    "Star Piece 9": ItemData(9, always_progression),
    "Star Piece 10": ItemData(10, always_progression),
    "Star Piece 11": ItemData(11, always_progression),
    "Star Piece 12": ItemData(12, always_progression),
    "Star Piece 13": ItemData(13, always_progression),
    "Star Piece 14": ItemData(14, always_progression),
    "Star Piece 15": ItemData(15, always_progression),
    "Star Piece 16": ItemData(16, always_progression),
    "Star Piece 17": ItemData(17, always_progression),
    "Star Piece 18": ItemData(18, always_progression),
    "Star Piece 19": ItemData(19, always_progression),
    "Star Piece 20": ItemData(20, always_progression),

    "Moon Piece 1": ItemData(33, always_progression),
    "Moon Piece 2": ItemData(34, always_progression),
    "Moon Piece 3": ItemData(35, always_progression),
    "Moon Piece 4": ItemData(36, always_progression),
    "Moon Piece 5": ItemData(37, always_progression),
    "Moon Piece 6": ItemData(38, always_progression),
    "Moon Piece 7": ItemData(39, always_progression),
    "Moon Piece 8": ItemData(40, always_progression),
    "Moon Piece 9": ItemData(41, always_progression),
    "Moon Piece 10": ItemData(42, always_progression),
    "Moon Piece 11": ItemData(43, always_progression),
    "Moon Piece 12": ItemData(44, always_progression),
    "Moon Piece 13": ItemData(45, always_progression),
    "Moon Piece 14": ItemData(46, always_progression),
    "Moon Piece 15": ItemData(47, always_progression),
    "Moon Piece 16": ItemData(48, always_progression),
    "Moon Piece 17": ItemData(49, always_progression),
    "Moon Piece 18": ItemData(50, always_progression),
    "Moon Piece 19": ItemData(51, always_progression),
    "Moon Piece 20": ItemData(52, always_progression),
}

stamps: dict[str, ItemData] = {

}

fillers: dict[str, ItemData] = {
    # "Penny": ItemData(0x2, always_filler),
    # "Penny1": ItemData(0x3, always_filler),
    # "Penny2": ItemData(0x4, always_filler),
    # "Penny3": ItemData(0x5, always_filler),
    # "Penny4": ItemData(0x6, always_filler),
}