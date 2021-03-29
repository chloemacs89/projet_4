#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

from controller.player import Player
from controller.tour import Tour
import model.loadplayer as lpdb
import model.tournamentdb as trdb


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
        self.saved_info = {
            "name": self.name,
            "localization": self.localization,
            "time_control": self.time_control,
            "description": self.description,
            "beg_date": self.beg_date,
            "end_date": self.end_date
        }

    def serialize_tournament_info(self):
        serial_info = {}
        player_info_list = []
        rounds_info_list = []
        serial_info["tournament_info"] = self.saved_info

        if self.__player_list:
            for nb, info in enumerate(self.__player_list):
                player_info = {}
                player_info[f"player{nb}"] = info.get_player_saved_info
                player_info_list.append(player_info)

        if player_info_list:
            serial_info["players_list"] = player_info_list

        if self.__round_list:
            for info in self.__round_list:
                rounds_info_list.append(info.serialize_round())
        else:
            pass

        if rounds_info_list:
            serial_info["rounds_list"] = rounds_info_list
        else:
            pass

        return {"tournament_data": serial_info}

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

    def save_tournament_in_db(self, db_file_name, update=False):
        tourn_info = self.serialize_tournament_info()
        trdb.TournamentDB(db_file_name).save_tournament_in_db(tourn_info, update)

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

    def play_round(self, roundp, game, result):
        if roundp.end_date is None:
            roundp.play_round(game, result)
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

    t1.add_new_player("POIRIER", "Marine", "14/05/1992", "F", 1)
    t1.add_new_player("VILLEY", "Chloé", "14/08/1989", "F", 2)
    t1.add_new_player("VILLEY", "Karine", "29/09/1985", "F", 28)
    t1.add_new_player("JOURDAN", "Evelyne", "04/10/1960", "F", 12)
    t1.add_new_player("QUESNEY", "Dany", "07/05/1990", "M", 19)
    t1.add_new_player("BRISE", "Vincent", "11/01/1990", "M", 6)
    t1.add_new_player("VILLEY", "Thierry", "06/09/1959", "M", 10)
    t1.add_new_player("SAINT-AUBIN", "Alana", "05/03/2016", "F", 156)

    for plr in t1.get_player_list:
        print(plr)

    t1.serialize_tournament_info()

    t1.add_round_to_list("Round 1")
    t1.describe_round()
    t1.play_round()
    t1.describe_round(4)
    t1.end_tournament()

    t1.save_tournament_in_db("tournamentdb.json", update=True)


