#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import attrgetter
import datetime as dt


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
                J1 = sorted_player_sup[i]
                J2 = sorted_player_inf[i]
                versus = [J1, J2]
                J1.set_already_met = J2
                J2.set_already_met = J2
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
                    while sorted_player[count] in sorted_player[0].get_already_met_list:
                        try:
                            count += 1
                            versus = [sorted_player[0], sorted_player[count]]
                        except IndexError:
                            count -= 1
                    self.match_list.append((versus, [0, 0]))
                    sorted_player[0].set_already_met = sorted_player[count]
                    sorted_player[count].set_already_met = sorted_player[0]
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
