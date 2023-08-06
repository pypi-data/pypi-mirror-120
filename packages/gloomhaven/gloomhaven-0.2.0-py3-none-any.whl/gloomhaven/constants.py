from .mod_applier import ModDeckApplier, mod_applier_fn

DEFAULT_DECK = [
    "Miss",
    "2x",
    "-2",
    "2",
    *["1"] * 5,
    *["-1"] * 5,
    *["0"] * 6,
]

RESET_LIST = ["Miss", "2x"]

MODIFIER_APPLIER = ModDeckApplier(mod_applier_fn)
MODIFIER_APPLIER["Miss"] = lambda x: 0
MODIFIER_APPLIER["2x"] = lambda x: 2 * x
