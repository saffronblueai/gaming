import numpy as np

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

def Get_Score(cards):
    if isinstance(cards,str):
        return card_scores[int(cards[0][1:]) - 1]
    else:
        score = 0
        for card in cards:
            score += card_scores[int(card[1:]) - 1]
        return score

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
    # shoe.shuffle()

    print(shoe.cards)

    for i in range(16):
        first_card = shoe.deal(1)
        real_score = Get_Score(first_card)
        print("card is ", first_card, ",real score is ", real_score)


    cards = shoe.deal(3)
    real_score = Get_Score(cards)
    print("cards is ", cards, ",real score is ", real_score)



