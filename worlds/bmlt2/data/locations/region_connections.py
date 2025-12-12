from .. import RegionConnectionData
from .rules import *

connections: dict[str, RegionConnectionData] = {
    "Starting the game": RegionConnectionData("Menu", "Star Zone - Star Bomber Castle", None),
    "Star Zone - Star Bomber Castle": RegionConnectionData("Star Zone - Star Bomber Castle", "Star Zone - Test", can_open_star_castle_gate),
    "Star Zone - Test": RegionConnectionData("Star Zone - Test", "Star Zone - Star Bomber Castle", can_open_star_castle_gate)
}