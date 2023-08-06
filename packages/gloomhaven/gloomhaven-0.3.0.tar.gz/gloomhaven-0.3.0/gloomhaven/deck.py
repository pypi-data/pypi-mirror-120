import random

from .constants import DEFAULT_DECK, MODIFIER_APPLIER, RESET_LIST


class GloomhavenDeck:
    RESET_LIST = RESET_LIST

    def __init__(self, cards=None, name=None):
        self.current_deck = []
        self.name = name
        if cards is None or len(cards) < 1:
            self.card_list = DEFAULT_DECK
        else:
            self.card_list = cards

        if all([card[0] == "c" for card in self.card_list]):
            raise ValueError("Invalid deck: contains all continue cards.")

    def shuffle_deck(self):
        self.empty_deck()
        tmp = random.sample(self.card_list, len(self.card_list))
        for card in tmp:
            self.current_deck.append(card)

    def empty_deck(self):
        self.current_deck = []

    def draw_card(self):
        if not len(self.current_deck):
            self.shuffle_deck()

        card_to_return = self.current_deck.pop()
        if card_to_return in self.RESET_LIST:
            self.shuffle_deck()
        return card_to_return

    def get_attack(self, base_attack):
        drawn_card = self.draw_card()
        attack_dmg = base_attack
        while True:
            if drawn_card[0] == "c":
                attack_dmg = MODIFIER_APPLIER[drawn_card[1:]](attack_dmg)
                drawn_card = self.draw_card()
            else:
                return MODIFIER_APPLIER[drawn_card](attack_dmg)

    def __repr__(self):
        return "\n".join(
            [
                self.name if self.name is not None else "",
                f"Cards: {', '.join(self.card_list)}",
                f"Current Deck: {', '.join(reversed(self.current_deck))}",
            ]
        )

    def __str__(self):
        return self.__repr__()

    def copy(self):
        return GloomhavenDeck(cards=self.card_list)
