class ModDeckApplier(dict):
    def __init__(self, default_fn):
        self.default_fn = default_fn

    def __missing__(self, k):
        return self.default_fn(k)


def mod_applier_fn(k):
    def apply_mod(x):
        return x + int(k) if (x + int(k)) >= 0 else 0

    return apply_mod
