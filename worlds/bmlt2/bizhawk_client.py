import logging
import math
from typing import TYPE_CHECKING, Any, Coroutine, Callable

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .client.locations import check_flag_locations
from .client.items import receive_items
from .client.setup import early_setup

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


def register_client():
    """This is just a placeholder function to remind new (and old) world devs to import the client file"""
    pass


class BombermanLandTouch2Client(BizHawkClient):
    game = "Bomberman Land Touch! 2"
    system = "NDS"
    patch_suffix = ".apbmlt2"

    ram_read_write_domain = "Main RAM"
    rom_read_only_domain = "ROM"  # Only works on BizHawk 2.10+

    data_address_address = 0x000024  # says 0x21B310 in vanilla W
    ingame_state_address = 0x000034
    header_address = 0x3ffa80

    items_inventory_address = 0x0AE8E0

    def __init__(self):
        super().__init__()
        self.player_name: str | None = None
        self.save_data_address = 0
        self.current_map = -1
        self.goal_checking_method: Callable[["BombermanLandTouch2Client", "BizHawkClientContext"], Coroutine[Any, Any, bool]] | None = None
        self.logger = logging.getLogger("Client")
        self.debug_halt = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """Should return whether the currently loaded ROM should be handled by this client. You might read the game name
        from the ROM header, for example. This function will only be asked to validate ROMs from the system set by the
        client class, so you do not need to check the system yourself.

        Once this function has determined that the ROM should be handled by this client, it should also modify `ctx`
        as necessary (such as setting `ctx.game = self.game`, modifying `ctx.items_handling`, etc...)."""

        header = await bizhawk.read(
            ctx.bizhawk_ctx, (
                (self.header_address, 0xc0, self.ram_read_write_domain),
            )
        )
        if header[0][:18] != b'TCHBMBMNLND2YB2E18':
            self.logger.warning(f"Invalid header: {header[0][:18]}")
            return False

        self.player_name = header[0][0xa0:].strip(b'\0').decode()
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        """Should set ctx.auth in anticipation of sending a `Connected` packet. You may override this if you store slot
        name in your patched ROM. If ctx.auth is not set after calling, the player will be prompted to enter their
        username."""

        if self.player_name is not None:
            ctx.auth = self.player_name

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        """For handling packages from the server. Called from `BizHawkClientContext.on_package`."""

        if cmd == 'Connected':
            from .data.locations import all_item_locations
            for loc_id in ctx.missing_locations:
                loc_name = ctx.location_names.lookup_in_game(loc_id)
                if loc_name not in all_item_locations:
                    self.logger.warning(f"Missing location \"{loc_name}\" neither flag")
        elif cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        """Runs on a loop with the approximate interval `ctx.watcher_timeout`. The currently loaded ROM is guaranteed
        to have passed your validator when this function is called, and the emulator is very likely to be connected."""

        try:
            if (
                not ctx.server or
                not ctx.server.socket.open or
                ctx.server.socket.closed or
                ctx.slot_data is None or
                self.debug_halt
            ):
                return
            read = await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (self.ingame_state_address, 1, self.ram_read_write_domain),
                )
            )
            if read[0][0] == 0:
                return
            setup_needed = False
            if self.save_data_address == 0:
                await early_setup(self, ctx)
                setup_needed = True

            locations_to_check: list[int] = (
                    await check_flag_locations(self, ctx)
            )
            if len(locations_to_check) != 0:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locations_to_check)}])

            await receive_items(self, ctx)

            if self.flags_cache[0x190 // 8] & 1 != 0:
                self.logger.warning("An error occurred while receiving an item ingame. "
                                    "Please report this and what you just received to the devs.")

            if await self.goal_checking_method(self, ctx):
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except bizhawk.RequestFailedError:
            pass

        except bizhawk.ConnectorError:
            pass

    def get_flag(self, flag: int) -> bool:
        return (self.flags_cache[flag // 8] & (2 ** (flag % 8))) != 0

    async def write_set_flag(self, ctx: "BizHawkClientContext", flag: int) -> None:
        while not await bizhawk.guarded_write(
                ctx.bizhawk_ctx, ((
                                          self.save_data_address + self.flags_offset + (flag // 8),
                                          [self.flags_cache[flag // 8] | (2 ** (flag % 8))],
                                          self.ram_read_write_domain
                                  ),), ((
                                                self.save_data_address + self.flags_offset + (flag // 8),
                                                [self.flags_cache[flag // 8]],
                                                self.ram_read_write_domain
                                        ),)
        ):
            self.flags_cache[flag // 8] = (await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (self.save_data_address + self.flags_offset + (flag // 8), 1, self.ram_read_write_domain),
                )
            ))[0][0]
        self.flags_cache[flag // 8] |= (2 ** (flag % 8))

    async def write_unset_flag(self, ctx: "BizHawkClientContext", flag: int) -> None:
        while not await bizhawk.guarded_write(
                ctx.bizhawk_ctx, ((
                                          self.save_data_address + self.flags_offset + (flag // 8),
                                          [self.flags_cache[flag // 8] & (255 - (2 ** (flag % 8)))],
                                          self.ram_read_write_domain
                                  ),), ((
                                                self.save_data_address + self.flags_offset + (flag // 8),
                                                [self.flags_cache[flag // 8]],
                                                self.ram_read_write_domain
                                        ),)
        ):
            self.flags_cache[flag // 8] = (await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (self.save_data_address + (flag // 8), 1, self.ram_read_write_domain),
                )
            ))[0][0]
        self.flags_cache[flag // 8] &= (255 - (2 ** (flag % 8)))

    async def write_var(self, ctx: "BizHawkClientContext", var: int, value: int, length=2) -> None:
        await bizhawk.write(
            ctx.bizhawk_ctx, ((
                                  self.save_data_address + (2 * var),
                                  value.to_bytes(length, "little"),
                                  self.ram_read_write_domain
                              ),)
        )

    async def read_var(self, ctx: "BizHawkClientContext", var: int, length=2) -> int:
        return int.from_bytes((await bizhawk.read(
            ctx.bizhawk_ctx, (
                (self.save_data_address + (2 * var), length, self.ram_read_write_domain),
            )
        ))[0], "little")
