from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    from ..bizhawk_client import BombermanLandTouch2Client
    from worlds._bizhawk.context import BizHawkClientContext


async def check_flag_items(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> list[int]:
    locations_to_check: list[int] = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.items_flag_address + client.items_flag_offset - 0x02000000 + 0x1, client.items_flag_bytes_amount, client.ram_read_write_domain),
        )
    )
    flags_buffer = read[0]
    for bytes in range(client.items_flag_bytes_amount):
        if client.items_flags_cache[bytes] - client.items_id_offset != flags_buffer[bytes]:
            merge = client.items_flags_cache[bytes] | flags_buffer[bytes]
            if client.items_flags_cache[bytes] - client.items_id_offset != merge:
                for bit in range(8):
                    if merge & (2 ** bit) != 0:
                        for loc_id in client.missing_flag_item_ids[bytes * 8 + bit]:
                            locations_to_check.append(loc_id)
            client.items_flags_cache[bytes] = merge
    return locations_to_check


async def check_flag_pieces(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> list[int]:
    locations_to_check: list[int] = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.piece_flag_address + client.piece_flag_offset - 0x02000000, client.piece_flag_bytes_amount, client.ram_read_write_domain),
        )
    )
    flags_buffer = read[0]
    for bytes in range(client.piece_flag_bytes_amount):
        if client.pieces_flags_cache[bytes] != flags_buffer[bytes]:
            merge = client.pieces_flags_cache[bytes] | flags_buffer[bytes]
            if client.pieces_flags_cache[bytes] != merge:
                for bit in range(8):
                    if merge & (2 ** bit) != 0:
                        for loc_id in client.missing_piece_item_ids[bytes * 8 + bit]:
                            locations_to_check.append(loc_id)
            client.pieces_flags_cache[bytes] = merge
    return locations_to_check

async def check_flag_stamps(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> list[int]:
    locations_to_check: list[int] = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.stamp_flag_address - 0x02000000, client.stamps_flag_bytes_amount, client.ram_read_write_domain),
        )
    )
    flags_buffer = read[0]
    for bytes in range(client.stamps_flag_bytes_amount):
        if client.stamps_flags_cache[bytes] != flags_buffer[bytes]:
            merge = client.stamps_flags_cache[bytes] | flags_buffer[bytes]
            if client.stamps_flags_cache[bytes] != merge:
                for bit in range(8):
                    if merge & (2 ** bit) != 0:
                        for loc_id in client.missing_stamp_item_ids[bytes * 8 + bit]:
                            locations_to_check.append(loc_id)
            client.stamps_flags_cache[bytes] = merge
    return locations_to_check
