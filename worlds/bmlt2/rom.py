import os
import pathlib
import zipfile

import Utils
from settings import get_settings
from worlds.Files import APAutoPatchInterface
from typing import TYPE_CHECKING, Any, Dict, Callable

if TYPE_CHECKING:
    from . import BombermanLandTouch2World


class BombermanLandTouch2Patch(APAutoPatchInterface):
    game = "Bomberman Land Touch! 2"
    patch_file_ending = ".apbmlt2"
    result_file_ending = ".nds"

    def __init__(self, path: str, player=None, player_name="", world=None):
        self.world: "BombermanLandTouch2World" = world
        self.files: dict[str, bytes] = {}
        super().__init__(path, player, player_name, "")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        PatchMethods.write_contents(self, opened_zipfile)

    def get_manifest(self) -> Dict[str, Any]:
        return PatchMethods.get_manifest(self, super().get_manifest())

    def patch(self, target: str) -> None:
        PatchMethods.patch(self, target)

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> Dict[str, Any]:
        return PatchMethods.read_contents(self, opened_zipfile, super().read_contents(opened_zipfile))

    def get_file(self, file: str) -> bytes:
        return PatchMethods.get_file(self, file)


class PatchMethods:

    @staticmethod
    def write_contents(patch: BombermanLandTouch2Patch, opened_zipfile: zipfile.ZipFile) -> None:
        from .patch.procedures import base_patch

        procedures: list[str] = ["base_patch"]

        opened_zipfile.writestr("procedures.txt", "\n".join(procedures))

    @staticmethod
    def get_manifest(patch: BombermanLandTouch2Patch, manifest: dict[str, Any]) -> Dict[str, Any]:
        from .data import version

        manifest["bmlt2_patch_format"] = version.patch_file()
        return manifest

    @staticmethod
    def patch(patch: BombermanLandTouch2Patch, target: str) -> None:
        from .data import version

        patch.read()

        if pathlib.Path(target).exists():
            with open(target, "rb") as f:
                header_part = f.read(0xA0)
                found_rom_version = tuple(header_part[0x9D:0xA0])
                if version.rom() != found_rom_version:
                    return

        from .ndspy.rom import NintendoDSRom
        from .patch.procedures import (base_patch)

        patch_procedures: dict[str, Callable[[NintendoDSRom, str, BombermanLandTouch2Patch], None]] = {
            "base_patch": base_patch.patch
        }

        base_data = get_base_rom_bytes()
        rom = NintendoDSRom(base_data)
        procedures: list[str] = str(patch.get_file("procedures.txt"), "utf-8").splitlines()
        for prod in procedures:
            patch_procedures[prod](rom, __name__, patch)
        if get_settings()["bomberman_land_touch_2_settings"]["extract_text"]:
            from .patch import text_extractor
            text_extractor.extract(rom, target)
        with open(target, 'wb') as f:
            f.write(rom.save(updateDeviceCapacity=True))

    @staticmethod
    def read_contents(patch: BombermanLandTouch2Patch, opened_zipfile: zipfile.ZipFile,
                      manifest: Dict[str, Any]) -> Dict[str, Any]:
        from .data import version

        for file in opened_zipfile.namelist():
            if file not in ["archipelago.json"]:
                patch.files[file] = opened_zipfile.read(file)

        found_version: tuple[int, ...] = tuple(manifest["bmlt2_patch_format"])
        accept = version.patch_accept(found_version)

        if accept == 1:
            raise Exception(f"File (bmlt2 patch version: {'.'.join(str(i) for i in manifest['bmlt2_patch_format'])}) too new "
                            f"for this handler (bmlt2 patch version: {version.patch_file()}). "
                            f"Please update your apworld.")
        elif accept == -1:
            raise Exception(f"File (bmlt2 patch version: {'.'.join(str(i) for i in manifest['bmlt2_patch_format'])}) too old "
                            f"for this handler (bmlt2 patch version: {version.patch_file()}). "
                            f"Either re-generate your world or downgrade to an older apworld version.")

        return manifest

    @staticmethod
    def get_file(patch: BombermanLandTouch2Patch, file: str) -> bytes:
        if file not in patch.files:
            patch.read()
        return patch.files[file]


def get_base_rom_bytes(file_name: str = "") -> bytes:
    if not file_name:
        file_name = get_base_rom_path(file_name)
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())
    if base_rom_bytes[:18] != b'TCHBMBMNLND2YB2E18':
        raise Exception(f"Supplied Base Rom appears to not be an english copy of Bomberman Land Touch! 2: "
                        f"{base_rom_bytes[:18]}")
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        file_name = get_settings()["bomberman_land_touch_2_settings"]["rom"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
