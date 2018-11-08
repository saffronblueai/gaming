from Deck import get_score
from Deck import get_real_score
from Utilities import Player_Status
from Utilities import Log_Level
from Utilities import convert_card
"""
Title:     Player.py
Author:    Wilson Chan / Saffron Blue Ltd
Description:   Class definition for BlackJack Player
Created:       1/1/18
Last Modified: 8/11/18
"""
score_chart={12:1,13:2,14:3,15:4,16:5,17:6,18:7,19:8,20:9,21:10}


class Player:

    SENSIBLE =0
    RISKY =1

    def __init__(self, id, type, report):
        self.id = id
        self.report = report
        """
        PARAMS
        """
        # default details
        self.spots = 2
        self.table_roll_of_account = 0
        self.bet_as_percent_table_roll = 0
        self.max_table_count = 0
        self.churn_after_x_consec_games = 5
        self.leaves_if_table_balance_hits_zero = True
        self.leave_table_if_loses_x_times = 0
        self.balance = 0
        self.tables = {}
        self.log = []
        self.log.append("creating player %s" % id)

        # last action
        self.table_count = 0
        self.starting_table_balance = 0
        self.table_start = None
        self.table_balance = 0
        self.table_id = None
        self.status = Player_Status.NO_STATE
        self.bonus_at = None
        self.bet = 0
        self.bonus = 0
        self.cards = []
        self.win = 0
        self.wins = []
        self.score = 0
        self.real_score = 0
        self.log_level = Log_Level.NONE

        self.action = ""  # "TWIST" / "STICK"
        """
        PROFILE
        """
        self.spots = 0
        self.churn_after_x_consec_games = 0
        self.leaves_if_table_balance_hits_zero = 0
        self.balance = 0

        if type == self.SENSIBLE:
            self.set_profile(table_roll_of_account=0.2, bet_as_percent_table_roll=0.05, spots=2, churn_after_x_consec_games=5, leaves_if_table_balance_hits_zero=True, leave_table_if_loses_x_times=12, balance=2000,
                                 max_table_count=100)
        else:
            self.set_profile(table_roll_of_account=0.2, bet_as_percent_table_roll=0.1, spots=2, churn_after_x_consec_games=5,
                    leaves_if_table_balance_hits_zero=True,leave_table_if_loses_x_times=10, balance=3000,max_table_count=200)

        log = "creating profile for player [%s]: table_roll_of_account=%s, bet_as_percent_table_roll=%s, spots=%s,churn_after_x_consec_games=%s,leaves_if_table_balance_hits_zero=%s,balance=%s" % (
        self.id, self.table_roll_of_account, self.bet_as_percent_table_roll, self.spots, self.churn_after_x_consec_games, self.leaves_if_table_balance_hits_zero, self.balance)
        self.log.append(log)
        # print(log)

    def set_profile(self,table_roll_of_account, bet_as_percent_table_roll, spots = 2, churn_after_x_consec_games=5,
                 leaves_if_table_balance_hits_zero=True, leave_table_if_loses_x_times = 10, balance=0, max_table_count=100):
        """
        PARAMS
        """
        self.table_roll_of_account = table_roll_of_account
        self.bet_as_percent_table_roll = bet_as_percent_table_roll
        self.max_table_count = max_table_count
        self.churn_after_x_consec_games = churn_after_x_consec_games
        self.leaves_if_table_balance_hits_zero = True
        self.leave_table_if_loses_x_times = leave_table_if_loses_x_times
        self.spots = spots
        self.leaves_if_table_balance_hits_zero = leaves_if_table_balance_hits_zero
        self.balance = balance

    def log_output(self, log, show=True):
        log = ("[%s]:" % self.id).ljust(30) + "------>" + log
        self.log.append(log)
        if show:
            print(log)

    def start_table(self,table_id, table_start):
        """
        complete
        """
        self.table_start = table_start
        self.table_count = 0
        table_balance = round(self.table_roll_of_account* self.balance)
        self.table_balance = table_balance
        self.starting_table_balance = self.table_balance
        self.consecutive_losses = self.consecutive_wins = 0

        show = True if self.log_level >= Log_Level.SESSION else False

        if self.balance > table_balance:
            self.table_id = table_id
            self.balance += -table_balance
            self.log_output("starting table: %s, table_balance = %s, new balance = %s" % (table_id,table_balance,self.balance),show)
        else:
            self.log_output("cannot open table %s"%table_id,show)

    def leave_table(self, table_time, reason_for_leaving):
        """
        complete
        """
        session_length = table_time - self.table_start
        profit = self.table_balance - self.starting_table_balance
        self.balance += self.table_balance
        self.table_id = None

        show = True if self.log_level >= Log_Level.SESSION else False
        self.log_output("leaving table: %s, profit = %s, new balance = %s, session time = %s, table count = %s (reason for leaving = %s)"
                        % (self.table_id, profit,self.balance, session_length, self.table_count, reason_for_leaving), show)

    def first_bet(self,table_min_bet):
        """
        bet (c)
        """

        normal_bet = round(self.bet_as_percent_table_roll*self.starting_table_balance)

        if normal_bet > self.table_balance:
            normal_bet = self.table_balance

        self.bet = max(table_min_bet,normal_bet)
        self.bonus_at = None
        self.bonus = 0
        self.status=Player_Status.FIRST_BET
        self.score = 0
        self.cards = []
        self.table_count += 1

        show = True if self.log_level >= Log_Level.GAME else False

        self.log_output("INITIAL BETTING of %s on table=%s"%(self.bet,self.table_id),show)

    def receive_cards(self, cards):
        """
        receive card (c)
        """
        self.cards.extend(cards)
        self.status = Player_Status.RECEIVE_FIRST_CARD
        self.score = get_score(self.cards)
        self.real_score = get_real_score(self.cards)
        show = True if self.log_level >= Log_Level.GAME else False

        self.log_output("RECEIVE cards %s score %s" % (str([convert_card(card) for card in self.cards]), self.score),show)

        if self.score>=22:
            self.status = Player_Status.BUST

    def next_bet(self, table_score, table_min_bet):
        """
        next bet
        """
        if 2<=table_score<=6 and 7<= self.score <= 11:
            self.bonus = self.bet
            self.status = Player_Status.LAST_CARD
            self.action = "TWIST"
            self.bonus_at = self.score
        else:
            self.bonus = 0

    def next_action(self, table_score):
        """
        stick or twist
        """
        if self.score<=16:
            self.action = "TWIST"
        else:
            self.action = "STICK"
            self.status = Player_Status.NO_MORE_ACTION

        show = True if self.log_level >= Log_Level.GAME else False
        self.log_output("ACTION :  %s" % self.action.lower(),show)
        return self.action

    def pay_out(self, table_score, table_real_score, game_count, table_time, games_since_last_shoe):

        def last(a, win):
            count = 0
            for w in a[::-1]:
                if w == win:
                    count += 1
                else:
                    break
            return count

        if self.score == table_score:
            win = 0
        elif self.score>21:
            win = -1
        elif table_score > 21:
            win = 1
        elif self.score>table_score:
            win = 1
        else:
            win = -1

        win_amount = win*(self.bet+self.bonus)
        self.table_balance += win_amount

        self.wins.append(win)

        show = True if self.log_level >= Log_Level.RESULT else False

        self.log_output("[table:%s(%s)], score = %s, table_score = %s, bet = %s, bonus = %s @ %s, win_amount = %s, table_balance = %s"
                        % (self.table_id, game_count, self.score, table_score, self.bet, self.bonus, self.bonus_at, win_amount, self.table_balance), show)

        self.report.append({"table":self.table_id,"player":self.id,"game_count":game_count,"games_since_last_shoe":games_since_last_shoe,"table_score":table_score,
                            "bet":self.bet,"bonus":self.bonus,"bonus_at":self.bonus_at,"win_amount":win_amount/self.bet,
                            "table_balance":self.table_balance,"action:":self.action,"player_score":self.real_score,"table_real_score":table_real_score,"win_conviction":self.real_score-table_real_score})
        """
        leave model
        """
        stay = True
        str_ = ""
        losses= last(self.wins,-1)
        if self.table_balance == 0 :
            stay = False
            str_ = "balance = 0"
        elif self.table_count >= self.max_table_count:
            stay = False
            str_ = "tired"
        elif losses>=self.leave_table_if_loses_x_times:
            stay = False
            str_ = "too many losses"

        if not stay:
            self.report[-1]["leave"] = True
            self.leave_table(table_time,str_)

        return stay

    def __str__(self):
        str_ = "\n\033[4mplayer\033[0m"
        for item in self.__dict__:
            str_ += "\n"+"%s : %s"%(item,self.__dict__[item])
        return str_

if __name__ == "__main__":


    print(Player(id="wilson",type=Player.SENSIBLE))