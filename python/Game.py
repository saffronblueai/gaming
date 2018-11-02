from enum import Enum


class Action(Enum):
    STICK = 0
    TWIST = 1


class Game:

    def __init__(self, player_id):
        self.player_id = player_id
        self.cards = []
        self.first_bet = 0
        self.second_bet = 0
        self.actions = []

    def first_bet(self,bet,cards):
        """
        bet + deal two cards
        """
        self.first_bet = bet
        self.cards=cards

    def next_action(self, action: Action):
        """
        stick or twist
        """
        self.actions.append(action)

    def receive_card(self,card):
        """
        """
        self.cards.append(card)

    def next_bet(self,bet,card):
        self.second_bet = bet
        self.next_action(card)

