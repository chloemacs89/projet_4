#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import os

from tinydb import TinyDB, Query

from controller.player import Player
from controller.tour import Tour


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

    def add_new_player(self):
        """Class to manually add a new player to the tournament. Can be done until 
        MAX_PLAYER_LIMIT is reached. 
        """
        if len(self.__player_list) < self.MAX_PLAYER_LIMIT:
            print("Adding a new player. Please enter the following informations.")
            print()
            l_name = input("Last name: ")
            f_name = input("First name: ")

            while True:
                date_birth = input("Date of birth (JJ/MM/AAAA): ")
                # check date validity. Numbers validity and calendar validity
                try:
                    dt.datetime.strptime(date_birth, "%d/%m/%Y")
                    break
                except ValueError:
                    print("Format ou date invalide, veuillez entrer une date valide")

            while True:
                gender = input("Gender (M/F): ")
                if gender.upper() in ("M", "F"):
                    break
                else:
                    print("Veuillez entre M ou F uniquement.")

            while True:
                try:
                    rank = int(input("Rank (must be a positive integer): "))
                    if rank > 0:
                        break
                    else:
                        print("La valeur doit être strictement positive. Veuillez entrer un nombre valide")
                except ValueError:
                    print("La valeur doit être un nombre strictement positif, Veuillez entrer un nombre valide")

            self.__player_list.append(
                Player(l_name, f_name, date_birth, gender, rank))
            print(f"\nPlayer Added to the tournament ({len(self.__player_list)}/{self.MAX_PLAYER_LIMIT})\n")
        else:
            print("Impossible d'ajouter un nouveau joueur. Nombre maximal atteint")

    def save_player_into_db(self, db_file):
        # TODO: TO WRITE INTO THE MODEL FILES
        file_path = os.path.join("data", db_file)
        db = TinyDB(file_path)
        for player in self.__player_list:
            if db.search(Query().id_player == player.id_player):
                print("Utilisateur déjà présent dans la DB.")
                while True:
                    rep = input("Souhaitez-vous mettre à jour le rang du joueur ? (Oui/Non) ")
                    if rep.lower() == "oui":
                        db.update({"rank": player.rank},
                                  Query().id_player == player.id_player)
                        break
                    elif rep.lower() == "non":
                        break
                    else:
                        print("Réponse invalide.")
            else:
                db.insert(player.get_player_saved_info)

    def get_player_description(self, index=None):
        if index is None:
            for player in self.__player_list:
                print(player)
        elif index in range(self.__player_list):
            print(self.__player_list[index])
        else:
            print("Format de l'index invalide ou joueur inéxistant.\n")

    def add_round_to_list(self):
        """Add a new Tour instance and create the round to be played. Since the first round
        making mechanism is different from the following round, the method check for the
        existence of a first round before making an instance.
        """
        if len(self.__round_list) < self.MAX_ROUND_LIST:
            if not self.__round_list:
                name = input("Nom du round (Round 1, Round 2, etc...) : ")
                rd = Tour(name, self.__player_list)
                rd.make_round()
                self.__round_list.append(rd)
            else:
                name = input("Nom du round (Round 1, Round 2, etc...) : ")
                rd = Tour(name, self.__player_list, not_first=True)
                rd.make_round(self.__round_list)
                self.__round_list.append(rd)
        else:
            print("Nombre de rounds maximum déjà joué.")
            print("Impossible de créer un nouveau round.")
            print("Tournoi terminé !\n")

    def play_round(self):
        for rounds in self.__round_list:
            if rounds.end_date is None:
                rounds.play_round()
            else:
                pass

    def describe_round(self, index=None):
        if index is None:
            for rd in self.__round_list:
                rd.describe_round()
        elif index in range(len(self.__round_list)):
            rd = self.__round_list[index]
            rd.describe_round()
        else:
            print("Format de l'index non valide ou round inéxistance.\n")

    def end_tournament(self):
        """Class to set the tournament's end date. Only works if
        every rounds have been played (last round has an end date).
        """
        every_round_exit = len(self.__round_list) == self.MAX_ROUND_LIST
        round_done = bool(self.__round_list[self.MAX_ROUND_LIST - 1].end_date)
        if every_round_exit and round_done and not self.end_date:
            while True:
                self.end_date = input("Date de fin du tournoi (JJ/MM/AAAA) : ")
                try:
                    dt.datetime.strptime(self.end_date, "%d/%m/%Y")
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
    for x in range(4):
        t1.add_new_player()

    t1.get_player_description()
    t1.add_round_to_list()
    t1.describe_round()
    t1.play_round()
    t1.describe_round()
