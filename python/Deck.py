import numpy as np
"""
Title:     Deck.py
Author:    Wilson Chan / Saffron Blue Ltd
Description:   Class definition for card deck
Created:       1/1/18
Last Modified: 8/11/18
"""

# visual card
suits = "H D C S".split()
numbers = [i+1 for i in range(13)]

# real scores
card_scores=[i for i in numbers]
card_scores[0]=11
card_scores[10]=10
card_scores[11]=10
card_scores[12]=10

score_chart={12:1,13:2,14:3,15:4,16:5,17:6,18:7,19:8,20:9,21:10}


def get_score(cards):
    if isinstance(cards,str):
        return card_scores[int(cards[0][1:]) - 1]
    else:
        score = 0
        for card in cards:
            score += card_scores[int(card[1:]) - 1]
        return score


def get_real_score(cards):
    if isinstance(cards,str):
        number = int(cards[0][1:]) - 1
        if number not in score_chart.keys():
            return 0
        else:
            return score_chart[number]/10
    else:
        score = 0
        for card in cards:
            score += card_scores[int(card[1:]) - 1]
        if score not in score_chart.keys():
            return 0
        else:
            return score_chart[score]/10


class Deck:
    def __init__(self):
        self.cards = ["%s%s"%(suit,number) for suit in suits for number in numbers]


class Shoe:
    def __init__(self, number_of_shoes):
        self.cards = []
        for i in range(number_of_shoes):
            deck = Deck()
            self.cards.extend(deck.cards)

    def new_shoe(self, number_of_decks):
        for i in range(number_of_decks):
            deck = Deck()
            self.cards.extend(deck.cards)

    def shuffle(self):
        index = [i for i in range(len(self.cards))]
        np.random.shuffle(index)
        self.cards = [self.cards[i] for i in index]

    def deal(self,number):
        cards = []
        if self.cards:
            for i in range(number):
                cards.append(self.cards.pop())
            return cards


if __name__ == "__main__":
    shoe = Shoe(1)
    shoe.shuffle()

    print(shoe.cards)

    for i in range(16):
        my_cards = shoe.deal(3)
        score = get_score(my_cards)
        real_score = get_real_score(my_cards)
        print("cards is ", my_cards, ",score is ", score, ", real score = ", real_score)



