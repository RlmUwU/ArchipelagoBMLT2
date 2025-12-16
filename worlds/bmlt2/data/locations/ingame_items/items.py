from ... import FlagLocationData
from ..rules import *
from ..progress_type import *

bombs: dict[str, FlagLocationData] = {
    "StarZone - Starbomber Castle - Right Chest": FlagLocationData(106, always_priority,
                                                                   "Star Zone - Star Bomber Castle", None, None),
    "StarZone - Starbomber Castle - Left Chest": FlagLocationData(101, always_default, "Star Zone - Star Bomber Castle",
                                                                  None, None),
}

pieces: dict[str, FlagLocationData] = {
    "Star Piece 1 Location": FlagLocationData(0, always_default, "Star Zone - Test", None, None),
    "Star Piece 2 Location": FlagLocationData(1, always_default, "Star Zone - Test", None, None),
    "Star Piece 3 Location": FlagLocationData(2, always_default, "Star Zone - Test", None, None),
    "Star Piece 4 Location": FlagLocationData(3, always_default, "Star Zone - Test", None, None),
    "Star Piece 5 Location": FlagLocationData(4, always_default, "Star Zone - Test", None, None),
    "Star Piece 6 Location": FlagLocationData(5, always_default, "Star Zone - Test", None, None),
    "Star Piece 7 Location": FlagLocationData(6, always_default, "Star Zone - Test", None, None),
    "Spoon Bender Reward 1": FlagLocationData(7, always_default, "Star Zone - Star Bomber Castle", None, None),
    "Star Piece 9 Location": FlagLocationData(8, always_default, "Star Zone - Test", None, None),
    "Star Piece 10 Location": FlagLocationData(9, always_default, "Star Zone - Test", None, None),
    "Star Piece 11 Location": FlagLocationData(10, always_default, "Star Zone - Test", None, None),
    "Star Piece 12 Location": FlagLocationData(11, always_default, "Star Zone - Test", None, None),
    "Star Piece 13 Location": FlagLocationData(12, always_default, "Star Zone - Test", None, None),
    "Star Piece 14 Location": FlagLocationData(13, always_default, "Star Zone - Test", None, None),
    "Star Piece 15 Location": FlagLocationData(14, always_default, "Star Zone - Test", None, None),
    "Star Piece 16 Location": FlagLocationData(15, always_default, "Star Zone - Test", None, None),
    "Star Piece 17 Location": FlagLocationData(16, always_default, "Star Zone - Test", None, None),
    "Star Piece 18 Location": FlagLocationData(17, always_default, "Star Zone - Test", None, None),
    "Star Piece 19 Location": FlagLocationData(18, always_default, "Star Zone - Test", None, None),
    "Star Piece 20 Location": FlagLocationData(19, always_default, "Star Zone - Test", None, None),

    "Moon Piece 1 Location": FlagLocationData(32, always_default, "Star Zone - Test", None, None),
    "Moon Piece 2 Location": FlagLocationData(33, always_default, "Star Zone - Test", None, None),
    "Moon Piece 3 Location": FlagLocationData(34, always_default, "Star Zone - Test", None, None),
    "Moon Piece 4 Location": FlagLocationData(35, always_default, "Star Zone - Test", None, None),
    "Moon Piece 5 Location": FlagLocationData(36, always_default, "Star Zone - Test", None, None),
    "Moon Piece 6 Location": FlagLocationData(37, always_default, "Star Zone - Test", None, None),
    "Moon Piece 7 Location": FlagLocationData(38, always_default, "Star Zone - Test", None, None),
    "Moon Piece 8 Location": FlagLocationData(39, always_default, "Star Zone - Test", None, None),
    "Moon Piece 9 Location": FlagLocationData(40, always_default, "Star Zone - Test", None, None),
    "Moon Piece 10 Location": FlagLocationData(41, always_default, "Star Zone - Test", None, None),
    "Moon Piece 11 Location": FlagLocationData(42, always_default, "Star Zone - Test", None, None),
    "Moon Piece 12 Location": FlagLocationData(43, always_default, "Star Zone - Test", None, None),
    "Moon Piece 13 Location": FlagLocationData(44, always_default, "Star Zone - Test", None, None),
    "Moon Piece 14 Location": FlagLocationData(45, always_default, "Star Zone - Test", None, None),
    "Moon Piece 15 Location": FlagLocationData(46, always_default, "Star Zone - Test", None, None),
    "Moon Piece 16 Location": FlagLocationData(47, always_default, "Star Zone - Test", None, None),
    "Moon Piece 17 Location": FlagLocationData(48, always_default, "Star Zone - Test", None, None),
    "Moon Piece 18 Location": FlagLocationData(49, always_default, "Star Zone - Test", None, None),
    "Moon Piece 19 Location": FlagLocationData(50, always_default, "Star Zone - Test", None, None),
    "Moon Piece 20 Location": FlagLocationData(51, always_default, "Star Zone - Test", None, None),
}

stamps: dict[str, tuple[int, int]] = {

}
