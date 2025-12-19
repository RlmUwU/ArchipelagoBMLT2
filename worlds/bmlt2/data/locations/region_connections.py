from .. import RegionConnectionData
from .rules import *

connections: dict[str, RegionConnectionData] = {
    "Starting the game": RegionConnectionData("Menu", "Star Castle - A", None),
    "Star Castle - 1 Star Gate": RegionConnectionData("Star Castle - A", "Star Zone - Test", gate_1_star),
    "Reach End": RegionConnectionData("Star Zone - Test", "Star Zone - End", can_do_all_temp),
}