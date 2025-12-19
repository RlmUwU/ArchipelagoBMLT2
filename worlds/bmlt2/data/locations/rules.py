from .. import ExtendedRule, InclusionRule
from ..items import star_piece

# Bombs
has_default_bomb: ExtendedRule = lambda state, world: (
    state.has("default bomb", world.player)
)

# Gates
gate_1_star: ExtendedRule = lambda state, world: (
    state.count_from_list(star_piece, world.player) >= 1
)

can_do_all_temp: ExtendedRule = lambda state, world: (
    has_default_bomb(state, world) and gate_1_star(state, world)
)

extended_rules_list: tuple = (
    has_default_bomb,

    gate_1_star,

    can_do_all_temp
)
