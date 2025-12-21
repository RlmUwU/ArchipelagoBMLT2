import logging
import math
from typing import TYPE_CHECKING, Any, Coroutine, Callable

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .client.locations import check_flag_items, check_flag_pieces, check_flag_stamps
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

    data_address_address = 0x000024
    ingame_state_address = 0x000034
    header_address = 0x3ffa80



    # Pieces Inventory
    piece_inventory_address = 0x0AE7A4
    piece_flag_offset = 0x4
    piece_flag_address = 0x023A6B00 - piece_flag_offset
    piece_flag_amount = 264
    piece_flag_bytes_amount = math.ceil(piece_flag_amount / 8)  # 8
    original_piece_flag_location = 0x06DEE4

    # Stamps Inventory
    stamp_inventory_address = 0x0AE7E8 # Where the stamps are stored
    stamp_flag_offset = 0x20
    stamp_flag_amount = 10 # Number of addresses covered by the inventory
    stamps_flag_bytes_amount = math.ceil(stamp_flag_amount / 8)  # 2
    stamp_flag_address = piece_flag_address + 0x17
    original_stamp_flag_location = 0x06CB24
    stamps_id_offset = 200  # Offset of the IDs in AP

    # Items Inventory
    items_inventory_address = 0x0AE8E0  # Where the item are stored
    items_flag_offset = 0x13c  # Offset present in the original game code
    items_flag_address = stamp_flag_address + 0x20  # Where the data is stored
    items_flag_amount = 32  # Number of addresses covered by the inventory
    items_id_offset = 256  # Offset of the IDs in AP
    items_flag_bytes_amount = math.ceil(items_flag_amount / 8)  # 4
    original_items_flag_location = 0x06E73C  # Where the item location is stored

    # Pennies

    # Goal Flags
    goal_flag_size = 1


    def __init__(self):
        super().__init__()
        self.player_name: str | None = None
        self.save_data_address = 0
        self.current_map = -1
        self.goal_checking_method: Callable[["BombermanLandTouch2Client", "BizHawkClientContext"], Coroutine[
            Any, Any, bool]] | None = None
        self.logger = logging.getLogger("Client")
        self.debug_halt = False

        # Items
        self.items_flags_cache: bytearray = bytearray(self.items_flag_bytes_amount)
        self.missing_flag_item_ids: list[list[int]] = [[] for _ in range(self.items_flag_amount)]
        # Pieces
        self.pieces_flags_cache: bytearray = bytearray(self.piece_flag_bytes_amount)
        self.missing_piece_item_ids: list[list[int]] = [[] for _ in range(self.piece_flag_amount)]
        # Stamps
        self.stamps_flags_cache: bytearray = bytearray(self.stamps_flag_bytes_amount)
        self.missing_stamp_item_ids: list[list[int]] = [[] for _ in range(self.stamp_flag_amount)]
        # Goal
        self.goal_flags_cache: bytearray = bytearray(self.goal_flag_size)

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
        await self.patch_after_launch(ctx)
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
            from .data.locations import items_locations, pieces_location, stamps_location
            for loc_id in ctx.missing_locations:
                loc_name = ctx.location_names.lookup_in_game(loc_id)
                if loc_name in items_locations:
                    self.missing_flag_item_ids[items_locations[loc_name].flag_id - self.items_id_offset].append(loc_id)
                elif loc_name in pieces_location:
                    self.missing_piece_item_ids[pieces_location[loc_name].flag_id].append(loc_id)
                elif loc_name in stamps_location:
                    self.missing_stamp_item_ids[stamps_location[loc_name].flag_id - self.stamps_id_offset].append(loc_id)
                else:
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
                await check_flag_items(self, ctx) +
                await check_flag_pieces(self, ctx) +
                await check_flag_stamps(self, ctx)
            )
            if len(locations_to_check) != 0:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locations_to_check)}])

            await receive_items(self, ctx)

            # if self.flags_cache[0x190 // 8] & 1 != 0:
            #     self.logger.warning("An error occurred while receiving an item ingame. "
            #                         "Please report this and what you just received to the devs.")

            if await self.goal_checking_method(self, ctx):
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except bizhawk.RequestFailedError:
            pass

        except bizhawk.ConnectorError:
            pass

    def get_flag(self, flag: int) -> bool:
        return (self.goal_flags_cache[flag // 8] & (2 ** (flag % 8))) != 0

    # async def write_set_flag(self, ctx: "BizHawkClientContext", flag: int) -> None:
    #     while not await bizhawk.guarded_write(
    #             ctx.bizhawk_ctx, ((
    #                                       self.save_data_address + self.flags_offset + (flag // 8),
    #                                       [self.items_flags_cache[flag // 8] | (2 ** (flag % 8))],
    #                                       self.ram_read_write_domain
    #                               ),), ((
    #                                             self.save_data_address + self.flags_offset + (flag // 8),
    #                                             [self.items_flags_cache[flag // 8]],
    #                                             self.ram_read_write_domain
    #                                     ),)
    #     ):
    #         self.items_flags_cache[flag // 8] = (await bizhawk.read(
    #             ctx.bizhawk_ctx, (
    #                 (self.save_data_address + self.flags_offset + (flag // 8), 1, self.ram_read_write_domain),
    #             )
    #         ))[0][0]
    #     self.items_flags_cache[flag // 8] |= (2 ** (flag % 8))
    #
    # async def write_unset_flag(self, ctx: "BizHawkClientContext", flag: int) -> None:
    #     while not await bizhawk.guarded_write(
    #             ctx.bizhawk_ctx, ((
    #                                       self.save_data_address + self.flags_offset + (flag // 8),
    #                                       [self.items_flags_cache[flag // 8] & (255 - (2 ** (flag % 8)))],
    #                                       self.ram_read_write_domain
    #                               ),), ((
    #                                             self.save_data_address + self.flags_offset + (flag // 8),
    #                                             [self.items_flags_cache[flag // 8]],
    #                                             self.ram_read_write_domain
    #                                     ),)
    #     ):
    #         self.items_flags_cache[flag // 8] = (await bizhawk.read(
    #             ctx.bizhawk_ctx, (
    #                 (self.save_data_address + (flag // 8), 1, self.ram_read_write_domain),
    #             )
    #         ))[0][0]
    #     self.items_flags_cache[flag // 8] &= (255 - (2 ** (flag % 8)))

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

    async def patch_after_launch(self, ctx: "BizHawkClientContext") -> None:
        await bizhawk.write(ctx.bizhawk_ctx, ((self.original_items_flag_location,
                                               (self.items_flag_address - self.items_flag_offset).to_bytes(8, "little"),
                                               self.ram_read_write_domain),))

        await bizhawk.write(ctx.bizhawk_ctx, ((self.original_piece_flag_location,
                                               self.piece_flag_address.to_bytes(8, "little"),
                                               self.ram_read_write_domain),))

        await bizhawk.write(ctx.bizhawk_ctx, ((self.original_stamp_flag_location,
                                               (self.stamp_flag_address - self.stamp_flag_offset).to_bytes(8, "little"),
                                               self.ram_read_write_domain),))
