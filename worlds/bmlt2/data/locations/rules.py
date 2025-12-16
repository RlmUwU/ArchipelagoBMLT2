from .. import ExtendedRule, InclusionRule
from ..items import star_piece

# Bombs
has_default_bomb: ExtendedRule = lambda state, world: (
    state.has("default bomb", world.player)
)

# Gates
can_open_star_castle_gate: ExtendedRule = lambda state, world: (
    state.count_from_list(star_piece, world.player) >= 2
)

extended_rules_list: tuple = (
    has_default_bomb,

    can_open_star_castle_gate
)
