from ... import FlagLocationData
from ..rules import *
from ..progress_type import *

table: dict[str, FlagLocationData] = {
    "StarZone - Starbomber Castle - Right Chest": FlagLocationData(0x00004000, always_priority, "Star Zone - Star Bomber Castle", None, None),
    "StarZone - Starbomber Castle - Left Chest": FlagLocationData(0x2, always_default, "Star Zone - Star Bomber Castle", None, None),
    "Testing1": FlagLocationData(3, always_default, "Star Zone - Star Bomber Castle", None, None),
    "Testing2": FlagLocationData(4, always_default, "Star Zone - Star Bomber Castle", None, None),
    "Testing3": FlagLocationData(5, always_default, "Star Zone - Star Bomber Castle", None, None)
}