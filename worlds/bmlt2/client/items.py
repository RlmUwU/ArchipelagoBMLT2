from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from ..data.items import all_bombs, all_pieces, all_items_dict_view

if TYPE_CHECKING:
    from ..bizhawk_client import BombermanLandTouch2Client
    from worlds._bizhawk.context import BizHawkClientContext


async def receive_items(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> None:
    received_items_count = await client.read_var(ctx, 0x126, 4)

    if received_items_count >= len(ctx.items_received):
        return

    inventory_buffer: bytearray | None = None

    new_received = received_items_count
    for index in range(received_items_count, len(ctx.items_received)):
        network_item = ctx.items_received[index]
        name = ctx.item_names.lookup_in_game(network_item.item)
        internal_id = all_items_dict_view[name].item_id
        match name:
            case x if x in all_bombs:
                if inventory_buffer is None:
                    inventory_buffer = await read_items(client, ctx)
                if not await write_to_items(client, ctx, inventory_buffer, internal_id):
                    client.logger.warning(f"Could not add {name} to main items bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case x if x in all_pieces:
                if inventory_buffer is None:
                    inventory_buffer = await read_pieces(client, ctx)
                if not await write_to_pieces(client, ctx, inventory_buffer, internal_id):
                    client.logger.warning(f"Could not add {name} to main items bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            # case x if x in all_pieces:
            #     if inventory_buffer is None:
            #         inventory_buffer = await read_piece(client, ctx, client.key_items_bag_offset, client.key_items_bag_size)
            #     if not await write_to_pieces(client, ctx, inventory_buffer, client.key_items_bag_offset,
            #                                  client.key_items_bag_size, internal_id, False):
            #         client.logger.warning(f"Could not add {name} to key items bag, no space left. "
            #                               f"Please report this to the developers.")
            #         break
            case _:
                client.logger.warning(f"Bad item name: {name}")
        new_received += 1

    # if new_received > received_items_count:
    #     await client.write_var(ctx, 0x126, new_received, 4)


async def read_items(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> bytearray:
    return bytearray((await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.items_inventory_address, client.items_flag_bytes_amount, client.ram_read_write_domain),
        )
    ))[0])


async def write_to_items(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext", buffer: bytearray, internal_id: int) -> bool:
    old_bytes = bytes(buffer)
    new_bytes = bytearray(buffer)
    byte_index = (internal_id-100) // 8
    bit_in_byte = (internal_id-100) % 8
    new_bytes[byte_index] |= (1 << bit_in_byte)

    if await bizhawk.guarded_write(
            ctx.bizhawk_ctx, ((client.items_inventory_address, new_bytes, client.ram_read_write_domain),),
            ((client.items_inventory_address, old_bytes, client.ram_read_write_domain),)
    ):
        return True
    else:
        return await write_to_items(client, ctx, buffer, internal_id)


async def read_pieces(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext") -> bytearray:
    return bytearray((await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.piece_inventory_address + client.piece_flag_offset, client.piece_flag_bytes_amount, client.ram_read_write_domain),
        )
    ))[0])


async def write_to_pieces(client: "BombermanLandTouch2Client", ctx: "BizHawkClientContext", buffer: bytearray, internal_id: int) -> bool:
    old_bytes = bytes(buffer)
    new_bytes = bytearray(buffer)
    byte_index = internal_id // 8
    bit_in_byte = internal_id % 8
    new_bytes[byte_index] |= (1 << bit_in_byte)

    if await bizhawk.guarded_write(
            ctx.bizhawk_ctx, ((client.piece_inventory_address + client.piece_flag_offset, new_bytes, client.ram_read_write_domain),),
            ((client.piece_inventory_address + client.piece_flag_offset, old_bytes, client.ram_read_write_domain),)
    ):
        return True
    else:
        return await write_to_pieces(client, ctx, buffer, internal_id)
