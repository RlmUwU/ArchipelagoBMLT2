from .. import RegionConnectionData
from .rules import *

connections: dict[str, RegionConnectionData] = {
    "Star Zone - Star Bomber Castle": RegionConnectionData("Star Zone - Test"),
    "Star Zone - Test": RegionConnectionData("Star Zone - Star Bomber Castle")
}