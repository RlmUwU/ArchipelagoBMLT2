from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    from ..bizhawk_client import BombermanLandTouch2Client
    from worlds._bizhawk.context import BizHawkClientContext


async def check_flag_items(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> list[int]:

    locations_to_check: list[int] = []
    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.items_flag_adress + client.items_flag_offset - 0x02000000, client.items_flag_amount, client.ram_read_write_domain),
        )
    )
    flags_buffer = read[0]
    print(f"buffer:{flags_buffer}, at:{hex(client.items_flag_adress + client.items_flag_offset)}, cache:{client.items_flags_cache}")
    for bytes in range(client.items_flag_amount):
        print(f"cache:{client.items_flags_cache[bytes]} - buffer:{flags_buffer[bytes]}")
        if client.items_flags_cache[bytes] != flags_buffer[bytes]:
            merge = client.items_flags_cache[bytes] | flags_buffer[bytes]
            print(f"merge: {merge}")
            if client.items_flags_cache[bytes] != merge:
                for bit in range(8):
                    print(f"bit:{bit}, value:{merge & (2 ** bit)}")
                    if merge & (2 ** bit) != 0:
                        for loc_id in client.missing_flag_item_ids[bytes * 8 + bit]:
                            locations_to_check.append(loc_id)
            client.items_flags_cache[bytes] = merge
    return locations_to_check
