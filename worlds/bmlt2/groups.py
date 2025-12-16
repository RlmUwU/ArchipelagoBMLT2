def get_item_groups() -> dict[str, set[str]]:
    from .data.items import items

    return {
        "Bombs": set(items.bombs),
        "Pieces": set(items.pieces),
        "Stamps": set(items.stamps),
    }


def get_location_groups() -> dict[str, set[str]]:
    from .data.locations.ingame_items import items

    return {
        "Bombs": set(items.bombs),
        "Pieces": set(items.pieces),
        "Stamps": set(items.stamps),
    }
