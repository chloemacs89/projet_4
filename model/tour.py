#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import attrgetter
from itertools import permutations
from model.player import Player
import datetime as dt

from tinydb import TinyDB, Query


class Tour:
    """Class managiing the creation of the different rounds of a
    tournament. By default, the minimum number of tours is set to 4.
    Ideally, tour's name should be 'Round 1', 'Round 2', and so on.
    """
    def __init__(self, name, player_list, not_first=False):
        """Class constructor : ask for round name et player list from which
        the rounds are made. The not_first argument is needed for every rounds
        but the first"""
        self.name = name
        self.start_date = dt.datetime.today()
        self.player_list = player_list
        self.match_list = []
        self.end_date = None
        self.not_first = not_first

    def make_round(self, prev_round_list=None):
        """Make a round list out of the players list. The matchmaking relies
        on the swiss tournament system :
        - On first round, players are sorted by their rank. The list is then
        divided by half, with a superior list and an inferior list. Sup List's
        player meet Inf list's first player, and so on.
        - On following rounds, players are sorted by score. 1st meets 2nd, 3rd
        meets 4th, and so on. Unless a round already happened between the two
        players.
        """
        if not self.not_first:
            sorted_player = sorted(self.player_list, key=attrgetter("rank"))
            sorted_player_sup = sorted_player[0:int(len(sorted_player) / 2)]
            sorted_player_inf = sorted_player[int(len(sorted_player) /
                                                  2):len(sorted_player)]
            for i in range(len(sorted_player_inf)):
                versus = [sorted_player_sup[i], sorted_player_inf[i]]
                score = [0, 0]
                match = (versus, score)
                self.match_list.append(match)
        else:
            sorted_player = self.player_list[:]
            sorted_player.sort(key=attrgetter("rank"))
            sorted_player = sorted(sorted_player,
                                   key=attrgetter("_Player__score"),
                                   reverse=True)

            for i in range(len(sorted_player)):
                # loop until 'sorted_player' is empty
                if sorted_player:
                    count = 1
                    versus = [sorted_player[0], sorted_player[count]]
                    # Loop to check if players already met each other in all of the
                    # previous rounds played before
                    for rounds in prev_round_list:
                        for prev_round in rounds.match_list:
                            # If players already met, the first player in the list
                            # is paired with the next player.
                            if tuple(versus) in permutations(prev_round[0]):
                                try:
                                    count += 1
                                    versus = [sorted_player[0], sorted_player[count]]
                                except IndexError:
                                    pass
                    self.match_list.append((versus, [0, 0]))
                    # Once paired, players are removed from the list.
                    sorted_player.pop(0)
                    sorted_player.pop(count - 1)
                else:
                    pass

    @property
    def get_match_list(self):
        return self.match_list

    def play_round(self, game, result):
        P1 = game[0][0]
        P2 = game[0][1]
        if result == "J1":
            game[1][0] = 1
            game[1][1] = 0
            P1.set_player_score = game[1][0]
            P2.set_player_score = game[1][1]
        elif result == "J2":
            game[1][0] = 0
            game[1][1] = 1
            P1.set_player_score = game[1][0]
            P2.set_player_score = game[1][1]
        elif result.lower() == "nul":
            game[1][0] = 0.5
            game[1][1] = 0.5
            P1.set_player_score = game[1][0]
            P2.set_player_score = game[1][1]

    def info_from_match(self):
        match_info = {}
        for e, info in enumerate(self.match_list):
            score = info[1]
            match_info[f"game {e+1}"] = score
        match_info["start_date"] = self.start_date.strftime("%d/%m/%Y %H:%M")
        match_info["end_date"] = self.end_date
        return match_info

    def serialize_round(self):
        return {f"{self.name}": self.info_from_match()}


if __name__ == '__main__':
    player_list = [
        Player("POIRIER", "Marine", "14/05/1992", "F", 1),
        Player("VILLEY", "Chloé", "14/08/1989", "F", 2),
        Player("VILLEY", "Karine", "29/09/1985", "F", 28),
        Player("JOURDAN", "Evelyne", "04/10/1960", "F", 12),
        Player("QUESNEY", "Dany", "07/05/1990", "M", 19),
        Player("BRISE", "Vincent", "11/01/1990", "M", 6),
        Player("VILLEY", "Thierry", "06/09/1959", "M", 10),
        Player("SAINT-AUBIN", "Alana", "05/03/2016", "F", 156)
    ]

    prev_round = []

    tr = Tour("Round 1", player_list)
    tr.make_round()
    # tr.describe_match()
    tr.play_round()
    for p in tr.player_list:
        print(p)
    tr.info_from_match()
    dct = tr.serialize_round()

    prev_round.append(tr)

    tr2 = Tour("Round 2", player_list, not_first=True)
    tr2.make_round(prev_round)
    tr2.describe_match()
    tr2.play_round()

    prev_round.append(tr2)

    tr3 = Tour("Round 3", player_list, not_first=True)
    tr3.make_round(prev_round)
    tr3.describe_match()
    tr3.play_round()

    prev_round.append(tr3)

    tr4 = Tour("Round 4", player_list, not_first=True)
    tr4.make_round(prev_round)
    tr4.describe_match()
    tr4.play_round()

    db = TinyDB("roundRB.json")
    rd_list = db.table("game_list")
    t = tr.info_from_match()
    rd_list.insert(t)
    for g in rd_list:
        print(g)
