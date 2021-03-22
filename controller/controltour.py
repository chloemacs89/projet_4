#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import os
from operator import attrgetter
from itertools import permutations

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
        self.__score = 0
        self.__player_saved_info = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_birth": self.date_birth,
            "gender": self.gender,
            "rank": self.rank,
            "id_player": self.id_player
        }

    @property
    def get_player_saved_info(self):
        return self.__player_saved_info

    @get_player_saved_info.setter
    def set_player_saved_info(self, key, value):
        self.__player_saved_info[key] = value

    @property
    def get_player_score(self):
        return self.__score

    @get_player_score.setter
    def set_player_score(self, score):
        self.__score = self.__score + score

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
        Rang : {self.rank}
        Score : {self.__score}\n"""


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
        if len(self.__player_list) < self.MAX_PLAYER_LIMIT:
            print(
                "Adding a new player. Please enter the following informations."
            )
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
                        "Format ou date invalide, veuillez entrer une date valide"
                    )

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

            self.__player_list.append(
                Player(l_name, f_name, date_birth, gender, rank))
            print(
                f"\nPlayer Added to the tournament ({len(self.__player_list)}/{self.MAX_PLAYER_LIMIT})\n"
            )

        else:
            print(
                "Impossible d'ajouter un nouveau joueur. Nombre maximal atteint"
            )

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
                db.insert(player.get_player_saved_info)

    def get_player_description(self, index=None):
        if index:
            print(self.__player_list[index])
        else:
            for player in self.__player_list:
                print(player)

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
        else:
            rd = self.__round_list[index]
            rd.describe_round()


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
            sorted_player = sorted(sorted_player, key=attrgetter("_Player__score"), reverse=True)

            for i in range(len(sorted_player)):
                # loop until 'sorted_player' is empty
                if sorted_player:
                    count = 1
                    versus = [sorted_player[0], sorted_player[count]]
                    # Loop to check if players already met each other in all of the
                    # previous rounds played before
                    for rounds in prev_round_list:
                        for prev_round in rounds.match_list:
                            # If players already met, the first player in the list
                            # is paired with the next player. 
                            if versus in permutations(prev_round[0]):
                                count += 1
                                versus = [sorted_player, sorted_player[count]]
                    self.match_list.append((versus, [0, 0]))
                    # Once paired, players are removed from the list. 
                    sorted_player.pop(0)
                    sorted_player.pop(count-1)
                else:
                    pass

    def describe_round(self):
        print(f"{self.name}")
        date_format = self.start_date.strftime("%d/%m/%Y %H:%M")
        print(f"Début du round : {date_format}\n")
        self.describe_match()
        if self.end_date:
            end_format = self.end_date.strftime("%d/%m/%Y %H:%M")
            print(f"Fin du round : {end_format}\n")
        else:
            print("Fin du round : round en cours\n")

    def describe_match(self):
        for e, i in enumerate(self.match_list):
            play1 = f"{i[0][0].first_name} {i[0][0].last_name}"
            play2 = f"{i[0][1].first_name} {i[0][1].last_name}"
            score = i[1]
            print(f"Match n°{e+1} :")
            print(f"(J1) {play1} vs {play2} (J2) -- Score : {score}\n")

    def play_round(self):
        print(f"Résultat pour le {self.name}.\n")
        print("Entrer 'J1' si J1 gagnant.")
        print("Entrer 'J2' si J2 gagnant.")
        print("Entrer 'Nul' si le match est nul.")
        self.describe_match()
        for e, i in enumerate(self.match_list):
            P1 = i[0][0]
            P2 = i[0][1]
            while True:
                result = input(f"Resultat Match n°{e+1} : ")
                if result == "J1":
                    i[1][0] = 1
                    i[1][1] = 0
                    P1.set_player_score = i[1][0]
                    P2.set_player_score = i[1][1]
                    break
                elif result == "J2":
                    i[1][0] = 0
                    i[1][1] = 1
                    P1.set_player_score = i[1][0]
                    P2.set_player_score = i[1][1]
                    break
                elif result.lower() == "nul":
                    i[1][0] = 0.5
                    i[1][1] = 0.5
                    P1.set_player_score = i[1][0]
                    P2.set_player_score = i[1][1]
                    break
                else:
                    print(" !! Commande invalide !!\n")
        self.end_date = dt.datetime.today()


def main():
    t1 = Tournament("Tournoi", "Caen", "Blitz", "", "22/03/2021 14:25")
    t1.add_new_player()
    t1.get_player_description()
    t1.add_new_player()
    t1.save_player_into_db("db.json")
    t1.get_player_description()
    t1.add_round_to_list()
    t1.describe_round()
    t1.play_round()
    t1.describe_round()


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
    r1.play_round()

    r1.describe_round()

    t1 = Tournament("Tournoi", "Caen", "Blitz", "", "22/03/2021 14:25")
    for x in range(4):
        t1.add_new_player()
    t1.get_player_description()
    t1.save_player_into_db("db.json")
    t1.get_player_description()
    t1.add_round_to_list()
    t1.describe_round()
    t1.play_round()
    t1.describe_round(1)
    
    a = [
        {"score": 5, "rang":1},
        {"score": 5, "rang":23},
        {"score": 4, "rang":6},
        {"score": 4, "rang":2}
    ]

    l = []
    for x in a:
        t = (x["score"], x["rang"])
        l.append(t)
    l
    l.sort(key=lambda c: c[1])
    sorted(l, key=lambda c: c[0], reverse=True)
