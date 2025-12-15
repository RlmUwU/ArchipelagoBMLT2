from typing import TYPE_CHECKING, Coroutine, Any, Callable

from worlds.bmlt2.bizhawk_client import BombermanLandTouch2Client

if TYPE_CHECKING:
    from ..bizhawk_client import BombermanLandTouch2Client
    from worlds._bizhawk.context import BizHawkClientContext


def get_method(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> Callable[
    ["BombermanLandTouch2Client", "BizHawkClientContext"], Coroutine[Any, Any, bool]]:
    return finish
    # match ctx.slot_data["options"]["goal"]:
    #     case "finish":
    #         return finish
    #     case _:
    #         client.logger.warning("Bad goal in slot data: "+ctx.slot_data["options"]["goal"])
    #         return error


async def finish(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> bool:
    return client.get_flag(0x1)


async def error(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> bool:
    return False
