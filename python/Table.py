from Gaming.Deck import Shoe
from Gaming.Player import Player
from Gaming.Deck import Get_Score
from Gaming.Utilities import Player_Status
from Gaming.Utilities import Log_Level
from pandas import Timestamp,Timedelta,set_option, DataFrame
import numpy as np

set_option('display.width', 500)
set_option("display.max_columns", 10)
score_chart={12:1,13:2,14:3,15:4,16:5,17:6,18:7,19:8,20:9,21:10}


class Table:

    def __init__(self,id,sex="m",colour="red",max_players=7,min_bet=10,max_bet=50,decks=8,dt=None):
        """
        complete
        """
        # static
        self.id = id
        self.dealer_sex = sex
        self.games = 0
        self.colour = colour
        self.max_players = max_players
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.shoe = Shoe(decks)
        self.log_level = Log_Level.NONE
        self.decks = decks

        # dynamic
        self.time = None
        self.players = []
        self.number_of_player_games = 0
        self.game_count = 0
        self.games_since_last_shoe = 0
        self.score = 0
        self.cards = []
        self.start_time = dt
        self.time = dt
        self.log = []

    def log_output(self, log, show=True):
        log = ("%s [%s]:" % (self.time, self.id)).ljust(30) + "------>" + log
        self.log.append(log)
        if show:
            print(log)

    def set_log_level(self,player_level,dealer_level):
        self.log_level = dealer_level
        for player in self.players:
            player.log_level = player_level

    def play_round(self):

        if len(self.players)==0:
            time_elapsed = self.time - self.start_time
            self.log_output("no more players, individual games=%s, time elapse = %s"
                            %(self.number_of_player_games,time_elapsed),self.log_level>Log_Level.NONE)
            return False
        # deal cards
        self.cards = []

        self.deal_first_cards()
        self.deal_remaining_cards()
        self.complete_round()
        self.payout()

        """
        add for time
        """
        for i in self.players:
            self.time += Timedelta("10s")

        # check for new shoe
        if len(self.shoe.cards)<len(self.players)*5+5:
            show = True if self.log_level >= Log_Level.GAME else False
            self.log_output("new shoe",show)
            self.shoe.new_shoe(self.decks)
            self.games_since_last_shoe = 0
        return True

    def deal_first_cards(self):
        """
        complete - deal first card for house and two cards for each player
        """
        self.cards = []
        self.score = 0
        self.game_count += 1
        self.games_since_last_shoe += 1
        self.number_of_player_games += len(self.players)
        shoe = self.shoe

        """
        take first bets (c)
        """
        for player in self.players:
            player.first_bet(self.min_bet)

        """
        deal dealer card (c)
        """
        card = shoe.deal(1)
        self.cards.extend(card)
        self.score = Get_Score(self.cards)

        show = True if self.log_level >= Log_Level.GAME else False

        self.log_output("dealing dealer card = %s score = %s"%(card,self.score),show)

        """
        deal first player cards (c)
        """
        for player in self.players:
            cards = shoe.deal(2)
            player.receive_cards(cards)

    def deal_remaining_cards(self):
        """
        complete - take possible bets (if bet then deal card)

              then continue until player complete

              ignore splits
        """

        shoe = self.shoe
        for player in self.players:
            """
            take possible bets (c)
            """
            player.next_bet(self.score,self.min_bet)

            if player.status == Player_Status.LAST_CARD:
                player.receive_cards(shoe.deal(1))
                # no more cards
                continue


            """
            player next action
            """
            while player.status is not Player_Status.NO_MORE_ACTION:
                action = player.next_action(self.score)
                if action == "TWIST":
                    player.receive_cards(shoe.deal(1))

    def complete_round(self):
        """
        dev    -  deal final dealer cards
        """
        shoe = self.shoe
        while self.score<=16:
            self.cards.extend(shoe.deal(1))
            self.score = Get_Score(self.cards)

            show = True if self.log_level >= Log_Level.GAME else False

            self.log_output("FINAL: cards = %s score = %s"%(self.cards, self.score),show)

    def payout(self):
        """
        payouts
        """
        for index, player in enumerate(self.players):
            if not player.pay_out(self.score,self.games_since_last_shoe, self.time):
                show = True if self.log_level >= Log_Level.GAME else False
                self.log_output("removing player : %s" % player.id, show)
                self.players.remove(player)

    def add_player(self,player):
        """
        complete
        """
        if len(self.players)==self.max_players:
            self.log_output("table full cannot add player : %s" % player.id, self.log_level>Log_Level.NONE)
            return False
        else:
            self.players.append(player)
            self.log_output("adding player : %s"%player.id,self.log_level>Log_Level.NONE)
            return True

    def remove_player(self,player):
        """
        complete
        """
        del self.players[player]

    def __str__(self):
        str_ = "\n\033[4mdealer\033[0m"
        for item in self.__dict__:
            str_ += "\n"+"%s : %s"%(item,self.__dict__[item])
        return str_
