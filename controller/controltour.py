#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

from tinydb import TinyDB, Query

from controller.player import Player
from controller.tour import Tour
import model.loadplayer as lpdb


class Tournament:
    """Tournament making class
    """
    def __init__(self,
                 name,
                 localization,
                 time_control,
                 description,
                 beg_date,
                 end_date=None):
        self.name = name
        self.localization = localization
        self.beg_date = beg_date
        self.end_date = end_date
        self.time_control = time_control
        self.description = description
        self.__player_list = []
        self.__round_list = []
        self.MAX_PLAYER_LIMIT = 8
        self.MAX_ROUND_LIST = 4

    @staticmethod
    def get_file_list():
        return lpdb.file_list_from_dir()

    @property
    def get_player_list(self):
        return self.__player_list

    @get_player_list.deleter
    def del_player_from_list(self, index):
        try:
            del self.__player_list[index]
        except IndexError:
            return False

    @property
    def get_round_list(self):
        return self.__round_list

    def add_new_player(self, l_name, f_name, date_birth, gender, rank):
        """Class to manually add a new player to the tournament. Can be done until
        MAX_PLAYER_LIMIT is reached.
        """
        player = Player(l_name, f_name, date_birth, gender, rank)
        self.__player_list.append(player)

    @staticmethod
    def save_player_into_db(db_file, player):
        save = lpdb.SavePlayer(db_file)
        save.save_player_into_db(player)

    def add_player_from_db(self, db_file, player_id):
        load = lpdb.LoadPlayer(db_file)
        if len(self.__player_list) != self.MAX_PLAYER_LIMIT:
            self.__player_list.append(load.load_player_from_db(player_id))
        else:
            raise Exception("Limite maximale de joueurs atteinte.")

    def get_player_list_from_db(self, db_file):
        load = lpdb.LoadPlayer(db_file)
        return load.list_player_from_db()

    def add_round_to_list(self, round_name):
        """Add a new Tour instance and create the round to be played. Since the first round
        making mechanism is different from the following round, the method check for the
        existence of a first round before making an instance.
        """
        if not self.__round_list:
            rd = Tour(round_name, self.__player_list)
            rd.make_round()
            self.__round_list.append(rd)
        else:
            rd = Tour(round_name, self.__player_list, not_first=True)
            rd.make_round(self.__round_list)
            self.__round_list.append(rd)

    def play_round(self):
        for rounds in self.__round_list:
            if rounds.end_date is None:
                rounds.play_round()
            else:
                raise Warning

    def end_tournament(self):
        """Class to set the tournament's end date. Only works if
        every rounds have been played (last round has an end date).
        """
        every_round_exit = len(self.__round_list) == self.MAX_ROUND_LIST
        round_done = bool(self.__round_list[len(self.__round_list) -
                                            1].end_date)
        if every_round_exit and round_done and not self.end_date:
            while True:
                self.end_date = input("Date de fin du tournoi (JJ/MM/AAAA) : ")
                try:
                    dt.datetime.strptime(self.end_date, "%d/%m/%Y")
                    break
                except ValueError:
                    print("Format invalide, veuillez recommencer.\n")
        else:
            print("Le tournoi n'est pas terminé.")
            print("Impossible de fixer une date de fin.\n")

    def __str__(self):
        end_date_info = self.end_date if self.end_date else "En cours"
        return f"""
        Nom : {self.name}
        Lieu : {self.localization}
        Contrôle du temps : {self.time_control}
        Date de début : {self.beg_date}
        Date de fin :  {end_date_info}
        Description : {self.description}
        """


if __name__ == '__main__':
    t1 = Tournament("Tournoi", "Caen", "Blitz", "", "22/03/2021 14:25")
    for x in range(8):
        t1.add_new_player()

    t1.get_player_description()
    t1.add_round_to_list()
    t1.describe_round()
    t1.play_round()
    t1.describe_round(4)
    t1.end_tournament()

    shallow = t1._Tournament__player_list[:]
    shallow.sort(key=attrgetter("rank"))
    shallow = sorted(shallow, key=attrgetter("_Player__score"), reverse=True)
    for p in shallow:
        print(p.first_name, "Score :", p._Player__score, "Rang :", p.rank)
