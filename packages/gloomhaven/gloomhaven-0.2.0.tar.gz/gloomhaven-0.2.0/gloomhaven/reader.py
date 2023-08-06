import yaml

from .deck import GloomhavenDeck


def read_deck(file_path):
    if file_path is None:
        raise ValueError("Provide valid path")
    with open(file_path) as f:
        deck_dict = yaml.safe_load(f)

    return GloomhavenDeck(**deck_dict)
