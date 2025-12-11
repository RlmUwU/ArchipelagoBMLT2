from .. import ExtendedRule, InclusionRule

# Bombs
has_default_bomb: ExtendedRule = lambda state, world: (
    state.has("default bomb", world.player)
)

# Gates
can_open_star_castle_gate: ExtendedRule = lambda state, world: (
    state.has("open star castle gate", world.player)
)

extended_rules_list: tuple = (
    has_default_bomb, can_open_star_castle_gate
)
