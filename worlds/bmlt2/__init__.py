import datetime
import logging
import os
from typing import ClassVar, Mapping, Any, List, TextIO

import settings
from BaseClasses import MultiWorld, Tutorial, Item, Location, Region
from Options import Option
from worlds.AutoWorld import World, WebWorld
from . import items, locations, options, bizhawk_client, rom, groups
from .generate import Items
from .data import RulesDict

bizhawk_client.register_client()


class BombermanLandTouch2Settings(settings.Group):

    class BombermanLandTouch2RomFile(settings.UserFilePath):
        """File name of your Bomberman Land Touch! 2 Rom"""
        description = "Bomberman Land Touch! 2 Rom"
        copy_to = "bmlt2.nds"

    class ExtractText(settings.Bool):
        """If enabled, running a patch file for this game will also produce a text file
        containing all ingame text alongside the rom."""

    rom: BombermanLandTouch2RomFile = BombermanLandTouch2RomFile(BombermanLandTouch2RomFile.copy_to)
    extract_text: ExtractText | bool = False


class BombermanLandTouch2Web(WebWorld):
    rich_text_options_doc = True
    theme = ("grassFlowers", "ocean", "dirt", "ice")[(datetime.datetime.now().month - 1) % 4]
    game_info_languages = ["en"]
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Bomberman land Touch! 2 with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["Rimuru"]
    )
    tutorials = [setup_en]


class BombermanLandTouch2World(World):
    game = "Bomberman Land Touch! 2"
    options_dataclass = options.BombermanLandTouch2Options
    options: options.BombermanLandTouch2Options
    topology_present = True
    web = BombermanLandTouch2Web()
    item_name_to_id = items.get_item_lookup_table()
    location_name_to_id = locations.get_location_lookup_table()
    settings_key = "bomberman_land_touch_2_settings"
    settings: ClassVar[BombermanLandTouch2Settings]
    item_name_groups = groups.get_item_groups()
    location_name_groups = groups.get_location_groups()

    glitches_item_name = "Out of logic"
    # tracker_world = {
    #     "map_page_folder": "tracker",
    #     "map_page_maps": "maps/maps.json",
    #     "map_page_locations": {
    #         "locations/locations.json",
    #         "locations/submaps_cities.json",
    #         "locations/submaps_dungeons.json",
    #         "locations/submaps_routes.json",
    #         "locations/old_compat.json",
    #     },
    #     "map_page_index": tracker.map_page_index,
    #     "map_page_setting_key": "pokemon_bw_map_{team}_{player}",
    # }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        from .data.version import ap_minimum
        from Utils import version_tuple
        if version_tuple < ap_minimum():
            raise Exception(f"Archipelago version too old for Bomberman Land Touch 2 "
                            f"(requires minimum {ap_minimum()}, found {version_tuple}")

        self.to_be_filled_locations: int = 0
        self.seed: int = 0
        self.regions: dict[str, Region] | None = None
        self.rules_dict: RulesDict | None = None

        self.location_id_to_alias: dict[int, str] = {}

    def generate_early(self) -> None:

        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                from .data import version

                re_ge_slot_data: dict[str, Any] = self.multiworld.re_gen_passthrough[self.game]
                re_gen_options: dict[str, Any] = re_ge_slot_data["options"]
                # Populate options from UT
                for key, value in re_gen_options.items():
                    opt: Option | None = getattr(self.options, key, None)
                    if opt is not None:
                        setattr(self.options, key, opt.from_any(value))
                self.seed = re_ge_slot_data["seed"]

        self.random.seed(self.seed)

        self.regions = locations.get_regions(self)
        self.rules_dict = locations.create_rule_dict(self)
        locations.connect_regions(self)
        locations.cleanup_regions(self.regions)

    def create_item(self, name: str) -> items.BombermanLandTouch2Item:
        return items.generate_item(name, self)

    def get_filler_item_name(self) -> str:
        return items.generate_filler(self)

    def create_regions(self) -> None:
        locations.create_and_place_locations(self)
        self.to_be_filled_locations = locations.count_to_be_filled_locations(self.regions)
        self.multiworld.regions.extend(self.regions.values())

    def create_items(self) -> None:
        item_pool = items.get_main_item_pool(self)
        items.populate_starting_inventory(self, item_pool)
        if len(item_pool) > self.to_be_filled_locations:
            raise Exception(f"Player {self.player_name} has more guaranteed items ({len(item_pool)}) "
                            f"than to-be-filled locations ({self.to_be_filled_locations})."
                            f"Please report this to the devs and provide the yaml used for generating.")
        for _ in range(self.to_be_filled_locations-len(item_pool)):
            item_pool.append(self.create_item(self.get_filler_item_name()))
        items.place_locked_items(self, item_pool)
        self.multiworld.itempool.extend(item_pool)

    def fill_hook(self,
                  progitempool: List[Item],
                  usefulitempool: List[Item],
                  filleritempool: List[Item],
                  fill_locations: List[Location]) -> None:
        pass

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        hint_data[self.player] = {}

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        pass
        # from .generate.spoiler import write_chests_spoiler
        # write_chests_spoiler(self, spoiler_handle)

    def generate_output(self, output_directory: str) -> None:
        rom.BombermanLandTouch2Patch(
            path=os.path.join(
                output_directory,
                self.multiworld.get_out_file_name_base(self.player) + rom.BombermanLandTouch2Patch.patch_file_ending
            ), world=self, player=self.player, player_name=self.player_name
        ).write()

    def fill_slot_data(self) -> Mapping[str, Any]:
        from .data import version

        # Some options and data are included for UT
        return {
            "options": {
                # "bombs": self.options.bombs
            }
        }

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        """Helper function for Universal Tracker"""
        return slot_data
