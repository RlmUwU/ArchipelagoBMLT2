import io
from typing import NamedTuple, TYPE_CHECKING
from zipfile import ZipFile

from ...ndspy.rom import NintendoDSRom
from ...ndspy.narc import NARC
import pkgutil

from .. import otpp

if TYPE_CHECKING:
    from ...rom import BombermanLandTouch2Patch


class PatchProcedure(NamedTuple):
    narc: NARC
    narc_filename: str


def patch(rom: NintendoDSRom, world_package: str, bmlt_patch_instance: "BombermanLandTouch2Patch") -> None:
    from ...data import version

    pad = rom.pad088[:0x15] + bytes(version.rom()) + bmlt_patch_instance.player_name.encode()
    rom.pad088 = pad + bytes(0x38 - len(pad))

    # open patch files zip and create dict of patch procedures
    procedures: dict[str, list[tuple[int, bytes]]] = {}
    # apply patches to each narc
    for narc_filename, proc_list in procedures.items():
        # load correct narc
        source_narc = NARC(rom.getFileByName(narc_filename))
        # apply each patch to corresponding file inside narc
        for proc in proc_list:
            source_narc.files[proc[0]] = otpp.patch(source_narc.files[proc[0]], proc[1])
        # write patched narc to rom
        rom.setFileByName(narc_filename, source_narc.save())