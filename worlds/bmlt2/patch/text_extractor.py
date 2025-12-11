from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ndspy.rom import NintendoDSRom


def extract(rom: "NintendoDSRom", target: str) -> None:
    from ..ndspy.narc import NARC
    from .text import decode
    with open(target+".story.txt", "wt") as story_f, open(target+".system.txt", "wt") as system_f:
        narc_system = NARC(rom.getFileByName("a/0/0/2"))
        narc_story = NARC(rom.getFileByName("a/0/0/3"))
        for i in range(len(narc_system.files)):
            text = decode(narc_system.files[i])
            system_f.write(f"Text file {i}:\n    ('system', {i}): [")
            for block_num in range(len(text)):
                system_f.write("{\n")
                for line_num in range(len(text[block_num])):
                    system_f.write(f"        {line_num}: \"{text[block_num][line_num].line}\"\n")
                system_f.write("    },")
            system_f.write("],\n")
        for i in range(len(narc_story.files)):
            text = decode(narc_story.files[i])
            story_f.write(f"Text file {i}:\n    ('story', {i}): [")
            for block_num in range(len(text)):
                story_f.write("{\n")
                for line_num in range(len(text[block_num])):
                    story_f.write(f"    {line_num}: \"{text[block_num][line_num].line}\"\n")
                story_f.write("    },")
            story_f.write("],\n")