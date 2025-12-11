from typing import NamedTuple, Callable, Literal, TYPE_CHECKING, TypeVar, Any, Union
from BaseClasses import ItemClassification, LocationProgressType, CollectionState

if not TYPE_CHECKING:
    AccessRule: type = Any
    ExtendedRule: type = Any
    ClassificationMethod: type = Any
    ProgressTypeMethod: type = Any
    InclusionRule: type = Any
    RulesDict: type = Any
else:
    from .. import BombermanLandTouch2World
    AccessRule: type = Callable[[CollectionState], bool]
    ExtendedRule: type = Callable[[CollectionState, BombermanLandTouch2World], bool]
    ClassificationMethod: type = Callable[[BombermanLandTouch2World], ItemClassification]
    ProgressTypeMethod: type = Callable[[BombermanLandTouch2World], LocationProgressType]
    InclusionRule: type = Callable[[BombermanLandTouch2World], bool]
    RulesDict: type = dict[ExtendedRule | tuple[ExtendedRule, ...], AccessRule]

T = TypeVar("T")
U = TypeVar("U")


class ItemData(NamedTuple):
    item_id: int
    classification: ClassificationMethod


class FlagLocationData(NamedTuple):
    # flags begin at 0x23bf28 (B) or 0x23bf48 (W)
    flag_id: int
    progress_type: ProgressTypeMethod
    region: str
    inclusion_rule: InclusionRule | None
    rule: ExtendedRule | None


class TextData(NamedTuple):
    credit: str
    section: Literal["story", "system"]
    file: int
    block: int
    entry: int
    text: str


class RegionConnectionData(NamedTuple):
    exiting_region: str
    entering_region: str
    rule: ExtendedRule | None


AnyItemData: type = Union[ItemData]
AnyLocationData: type = Union[FlagLocationData]
