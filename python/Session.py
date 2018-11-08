from Table import Table
from Player import Player
from pandas import DataFrame
from pandas import Timestamp
import pandas as pd
from Utilities import Log_Level
import numpy as np

# set display right
pd.set_option('display.width', 4000)
pd.set_option('max_colwidth', 4000)
pd.set_option('max_rows', 100)
pd.set_option('max_columns', 200)

"""
Title:     Deck.py
Author:    Wilson Chan / Saffron Blue Ltd
Description:   Class definition for black jack table
Created:       1/1/18
Last Modified: 8/11/18
"""

report = []
table = Table("hellmuth", sex="m", colour="green", max_players=7, min_bet=50, max_bet=300, decks=8, dt=Timestamp("2018.01.01"))
table.shoe.shuffle()

if __name__ == "__main__":

    """
    set up table
    """

    report = []
    table = Table("hellmuth", sex="m", colour="green", max_players=7, min_bet=50, max_bet=300, decks=8, dt=Timestamp("2018.01.01"))
    table.shoe.shuffle()

    """
    set up player profiles
    """

    print("\033[4mcreating player pool\033[0m")

    number_of_sensible = 4
    number_of_risky = 1
    total_number_of_players = number_of_sensible + number_of_risky

    players = []

    # [players.append(Player(id="s%s"%i, type=Player.SENSIBLE, report = report)) for i in range(number_of_sensible)]
    [players.append(Player(id="r%s"%i, type=Player.RISKY, report = report)) for i in range(number_of_risky)]

    print("total number of players:%s"%len(players))
    print("\033[4massembling tables\033[0m")
    table = Table("hellmuth0", sex="m", colour="green", max_players=7, min_bet=50, max_bet=300, decks=8, dt=Timestamp("2018.01.01"))
    table.shoe.shuffle()
    tables = [table]

    while players:
        player = players.pop()
        if not table.add_player(player):
            table = Table("hellmuth%s"%len(tables), sex="m", colour="green", max_players=7, min_bet=50, max_bet=300, decks=8, dt=Timestamp("2018.01.01"))
            table.shoe.shuffle()
            tables.append(table)
            table.add_player(player)

    """
    audit
    """
    [table.set_log_level(player_level=Log_Level.NONE, dealer_level=Log_Level.NONE) for table in tables]

    """
    play
    """
    for table in tables:
        for player in table.players:
            player.start_table(table_id=table.id, table_start=table.time)
        while table.play_round() and table.games<200:
            pass

    df = DataFrame(data=report,columns="table player game_count games_since_last_shoe action player_score table_real_score win_conviction bet bonus bonus_at win_amount table_balance leave".split())
    df = df.replace(np.nan, '', regex=True)

    """
    Player_Opt_Play
    Games_Since_Last_Shoe (done)
    Win (done)
    Conviction
    Bonus (dev)
    Bet (done)
    Winnings
    Balance (done)
    """

    # for player in df["player"].unique():
    #     print(df[df["player"]==player])
    #     exit()

    print(df.head())
