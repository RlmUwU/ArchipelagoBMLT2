
def get_item_groups() -> dict[str, set[str]]:
    from .data.items import items

    return {
        "Bombs": set(items.bombs),
        "Pieces": set(items.pieces),
    }


def get_location_groups() -> dict[str, set[str]]:
    from .data.locations.ingame_items import chests_items

    return {
        "Chests": set(chests_items.table),
    }