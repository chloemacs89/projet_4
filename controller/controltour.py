#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

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
    def __init__(self):
        self.__player_list = []

    def add_new_player(self):
        print("Adding a new player. Please enter the following informations.")
        print()
        l_name = input("Last name: ")
        f_name = input("First name: ")

        while True:
            date_birth = input("Date of birth (JJ/MM/AAAA): ")
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

        print("\nPlayer Added to the tournament\n")
        self.__player_list.append(
            Player(l_name, f_name, date_birth, gender, rank))

    def save_player_into_db(self, db_file):
        db = TinyDB(db_file)
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


def main():
    t1 = Tournament()
    t1.add_new_player()
    t1.get_player_description()
    t1.add_new_player()
    t1.save_player_into_db("db.json")
    t1.get_player_description()
    t1.get_player_description(1)
    t1.save_player_into_db("db.json")


if __name__ == '__main__':
    main()
