from enum import Enum

class Player_Status(Enum):
    NO_STATE = 0
    RECEIVE_FIRST_CARD = 1
    FIRST_BET = 2
    FIRST_ACTION = 3
    SECOND_BET = 4
    LAST_CARD = 6
    NO_MORE_ACTION = 7
    BUST = 8
    GAME_COMPLETE = 9


class Log_Level:
    NONE = 0
    SESSION = 1
    RESULT = 2
    GAME = 3

def last(a,win):
    count = 0
    for w in a[::-1]:
        if w==win:
            count += 1
        else:
            break
    return count



def convert_card(card):
    suit = card[:1]
    value = card[1:]

    dict_one = {1:"Ace",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",
             10:"Ten",11:"Jack",12:"Queen",13:"King"}
    dict_two = {"H":"Heart","D":"Diamond","C":"Club","S":"Spade"}
    return "%s %s"%(dict_two[suit],dict_one[int(value)])


if __name__ == "__main__":

    card = "C13"  # "king hearts"
    print(card)
    print(convert_card(card))



