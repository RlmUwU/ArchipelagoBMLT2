from BaseClasses import LocationProgressType
from .. import ProgressTypeMethod


always_priority: ProgressTypeMethod = lambda world: LocationProgressType.PRIORITY

always_default: ProgressTypeMethod = lambda world: LocationProgressType.DEFAULT

always_excluded: ProgressTypeMethod = lambda world: LocationProgressType.EXCLUDED

key_item_location: ProgressTypeMethod = lambda world: (
    LocationProgressType.PRIORITY
    if "Prioritize key item locations" in world.options.modify_logic
    else LocationProgressType.DEFAULT
)