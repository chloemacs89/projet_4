#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import os
from operator import attrgetter

from tinydb import TinyDB, Query


class Player:
    """Class to make an instance of a chess player. Includes the following
    informations :
    - First Name
    - Last Name
    - Date of Birth
    - Gender
    - Rank
    """
    def __init__(self, l_name, f_name, date_birth, gender, rank):
        """Class constructor"""
        self.last_name = l_name.capitalize()
        self.first_name = f_name.capitalize()
        self.date_birth = date_birth
        self.gender = gender.upper()
        self.rank = rank
        self.id_player = self.date_birth.replace("/", "")[4:] + "_" \
            + self.last_name[0] \
            + self.first_name[0]

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __str__(self):
        if self.gender == "M":
            print("Description du joueur :")
        elif self.gender == "F":
            print("Description de la joueuse :")

        return f"""
        Nom : {self.last_name}
        Prénom : {self.first_name}
        Date de naissance : {self.date_birth}
        Sexe : {self.gender}
        Rang : {self.rank}\n"""


class Tournament:
    """Tournament making class
    """
    def __init__(self, name, localization, time_control, description, beg_date, end_date=None):
        self.name = name
        self.localization = localization
        self.beg_date = beg_date
        self.end_date = end_date
        self.time_control = time_control
        self.description = description
        self.__player_list = []
        self.__round_list = []
        self.MAX_PLAYER_LIMIT = 8

    def add_new_player(self):
        if len(self.__player_list) < self.MAX_PLAYER_LIMIT:
            print("Adding a new player. Please enter the following informations.")
            print()
            l_name = input("Last name: ")
            f_name = input("First name: ")

            while True:
                date_birth = input("Date of birth (JJ/MM/AAAA): ")
                # check date validity. Numbers validity and calendar validity
                try:
                    dt.datetime.strptime(date_birth, "%d/%m/%Y")
                    break
                except ValueError:
                    print(
                        "Format ou date invalide, veuillez entrer une date valide")

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
                        print(
                            "La valeur doit être strictement positive. Veuillez entrer un nombre valide"
                        )
                except ValueError:
                    print(
                        "La valeur doit être un nombre strictement positif, Veuillez entrer un nombre valide"
                    )

            print(f"\nPlayer Added to the tournament ({len(self.__player_list)}/{self.MAX_PLAYER_LIMIT})\n")
            self.__player_list.append(
                Player(l_name, f_name, date_birth, gender, rank))
        
        else:
            print("Impossible d'ajouter un nouveau joueur. Nombre maximal atteint")

    def save_player_into_db(self, db_file):
        file_path = os.path.join("data", db_file)
        db = TinyDB(file_path)
        for player in self.__player_list:
            if db.search(Query().id_player == player.id_player):
                print("Utilisateur déjà présent dans la DB.")
                while True:
                    rep = input(
                        "Souhaitez-vous mettre à jour le rang du joueur ? (Oui/Non) "
                    )
                    if rep.lower() == "oui":
                        db.update({"rank": player.rank},
                                  Query().id_player == player.id_player)
                        break
                    elif rep.lower() == "non":
                        break
                    else:
                        print("Réponse invalide.")
            else:
                db.insert(player.__dict__)

    def get_player_description(self, index=None):
        if index:
            print(self.__player_list[index])
        else:
            for player in self.__player_list:
                print(player)

    def make_round_list(self):
        name = input("Nom du round (Round 1, Round 2, etc...) : ")
        self.__round_list.append(Tour(name, self.__player_list))


class Tour:
    """Class managiing the creation of the different rounds of a
    tournament. By default, the minimum number of tours is set to 4.
    Ideally, tour's name should be 'Round 1', 'Round 2', and so on.
    """
    def __init__(self, name, player_list):
        """Class constructor, only ask for the round name."""
        self.name = name
        self.start_date = dt.datetime.today()
        self.player_list = player_list
        self.match_list = []
        self.end_date = None

    def make_round(self):
        """Make a round list out of the players list. The matchmaking relies
        on the swiss tournament system :
        - On first round, players are sorted by their rank. The list is then
        divided by half, with a superior list and an inferior list. Sup List's
        player meet Inf list's first player, and so on.
        - On following rounds, players are sorted by score. 1st meets 2nd, 3rd
        meets 4th, and so on. Unless a round already happened between the two
        players.
        """
        sorted_player = sorted(self.player_list, key=attrgetter("rank"))
        sorted_player_sup = sorted_player[0:int(len(sorted_player) / 2)]
        sorted_player_inf = sorted_player[int(len(sorted_player) /
                                              2):len(sorted_player)]
        for i in range(len(sorted_player_inf)):
            versus = [sorted_player_sup[i], sorted_player_inf[i]]
            score = [0, 0]
            match = (versus, score)
            self.match_list.append(match)

    def describe_round(self):
        print(f"{self.name}")
        date_format = self.start_date.strftime("%d/%m/%Y %H:%M")
        print(f"Début du round : {date_format}\n")
        for e, i in enumerate(self.match_list):
            play1 = f"{i[0][0].first_name} {i[0][0].last_name}"
            play2 = f"{i[0][1].first_name} {i[0][1].last_name}"
            score = i[1]
            print(f"Match n°{e+1} :")
            print(f"{play1} vs {play2} -- Score : {score}\n")
        if self.end_date:
            end_format = self.end_date.strftime("%d/%m/%Y %H:%M")
            print(f"Fin du round : {end_format}")
        else:
            print("Fin du round : round en cours")


def main():
    t1 = Tournament()
    t1.add_new_player()
    t1.get_player_description()
    t1.add_new_player()
    t1.save_player_into_db("db.json")
    t1.get_player_description()
    t1.make_round_list()


if __name__ == '__main__':
    main()

    L = [
        Player("A", "B", "14/08/1999", "M", 15),
        Player("C", "D", "14/08/1998", "M", 32),
        Player("E", "F", "14/08/1997", "M", 45),
        Player("G", "H", "14/08/1996", "M", 3)
    ]

    r1 = Tour("Round 1", L)
    r1.make_round()
    r1.match_list

    r1.describe_round()
