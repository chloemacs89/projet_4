#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime as dt
from operator import attrgetter

import controller.controltour as clt


class Menu:
    """Menu class. Is controlling the view et the whole menu of the chess
    application.
    """
    def __init__(self):
        "Class constructor, make the Tournament list"
        self.__tournament_list = []
        self.__current_tournament = None
        self.__today_date = dt.today().strftime("%d/%m/%Y")
        self.__current_time = dt.today().strftime("%H:%M")

    def start_menu(self):
        print(
            "Bienvenue dans votre application de gestion de tournois d'échec.")
        print(f"Nous somme le {self.__today_date} à {self.__current_time}.\n")

        while True:
            print("Catégories disponibles.")
            print("==============================\n")
            print("Créer un nouveau tournoi (1)")
            print("Accéder au menu du tournoi en cours (2)")
            print("Charger un tournoi depuis la base de données (3)")
            print("Afficher la liste des tournois (4)")
            print("Quitter l'application (q)\n")
            resp = input("Choix : ")
            if resp in ("1", "2", "3", "4", "q"):
                break
            else:
                print("Choix invalide")

        if resp == "1":
            self.create_tournament()
        elif resp == "2":
            if self.__tournament_list:
                pass
            else:
                print(
                    " !! Action impossible, aucun tournoi n'a encore été créé ou chargé. !!\n"
                )
                self.start_menu()
        elif resp == "3":
            pass
        elif resp == "4":
            if self.__tournament_list:
                pass
            else:
                print(
                    " !! Action impossible, aucun tournoi n'a encore été créé ou chargé. !!\n"
                )
                self.start_menu()
        elif resp == "q":
            r = input(
                "Êtes-vous sûr de vouloir quitter l'appplication ? (O/N) ")
            if r.lower() == "o":
                pass
            else:
                self.start_menu()

    def create_tournament(self):
        print("Bienvenue dans la création d'un tournoi.")
        print("==============================\n")

        name = input("Nom du tournoi : ")
        localization = input("Lieu du tournoi : ")

        while True:
            time_control = input(
                "Type de contrôle du temps (Bullet, Blitz ou Coup rapide) : ")
            if time_control.lower() in ("bullet", "blitz", "coup rapide"):
                break
            else:
                print("Type invalide, veuillez choisir à nouveau.")

        description = input("Description du tournoi (optionnel) : ")

        while True:
            beg_date = input("Date de début du tournoi (JJ/MM/AAAA HH:MM): ")
            try:
                dt.strptime(beg_date, "%d/%m/%Y %H:%M")
                break
            except ValueError:
                print(
                    "Format invalide. Veuillez rentrer une date et une heure valide"
                )

        chess_tournament = clt.Tournament(name, localization, time_control,
                                          description, beg_date)
        self.__tournament_list.append(chess_tournament)
        self.__current_tournament = chess_tournament

    @property
    def get_tournament_list(self):
        return self.__tournament_list

    def add_player_to_tournament(self):
        if len(self.__current_tournament.get_player_list
               ) < self.__current_tournament.MAX_ROUND_LIST:
            print(
                "Adding a new player. Please enter the following informations."
            )
            print()
            l_name = input("Last name: ")
            f_name = input("First name: ")

            while True:
                date_birth = input("Date of birth (JJ/MM/AAAA): ")
                # check date validity. Numbers validity and calendar validity
                try:
                    dt.strptime(date_birth, "%d/%m/%Y")
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

            self.__current_tournament.add_new_player(l_name, f_name,
                                                     date_birth, gender, rank)
            print("Création terminée, ", end='')
            print(
                f"{len(self.__current_tournament.get_player_list)}/{self.__current_tournament.MAX_PLAYER_LIMIT}"
            )

        else:
            print("Nombre de joueurs maximum atteint.")

    def add_round(self):
        if len(self.__current_tournament.get_round_list
               ) < self.__current_tournament.MAX_ROUND_LIST:
            if not self.__current_tournament.get_round_list:
                round_nb = 1
                round_name = f"Round {round_nb}"
                print(f"Création du {round_name} en cours...")
                self.__current_tournament.add_round_to_list(round_name)
                print("Création terminée.")
            else:
                round_nb = len(self.__current_tournament.get_round_list) + 1
                round_name = f"Round {round_nb}"
                print(f"Création du {round_name} en cours...")
                self.__current_tournament.add_round_to_list(round_name)
                print("Création terminée.")
        else:
            print("Nombre de round maximum déjà atteint.")
            print("Impossible de créer un nouveau round.\n")

    def describe_round(self, rd):
        for e, i in enumerate(rd.match_list):
            play1 = f"{i[0][0].first_name} {i[0][0].last_name}"
            play2 = f"{i[0][1].first_name} {i[0][1].last_name}"
            score = i[1]
            print(f"Match n°{e+1} :")
            print(f"(J1) {play1} vs {play2} (J2) -- Score : {score}\n")
        if rd.end_date:
            end_format = rd.end_date.strftime("%d/%m/%Y %H:%M")
            print(f"Fin du round : {end_format}\n")
            print("==============================\n")
        else:
            print("Fin du round : round en cours\n")
            print("==============================\n")

    def describe_rounds(self, index=None):
        if index is None:
            for rd in self.__current_tournament.get_round_list:
                print(f"{rd.name}")
                date_format = rd.start_date.strftime("%d/%m/%Y %H:%M")
                print(f"Début du round : {date_format}\n")
                self.describe_round(rd)
        else:
            try:
                rd = self.__current_tournament.get_round_list[index]
                print(f"{rd.name}")
                date_format = rd.start_date.strftime("%d/%m/%Y %H:%M")
                print(f"Début du round : {date_format}\n")
                self.describe_round(rd)
            except IndexError:
                print("Index invalide.")
            except TypeError:
                print("Format de l'index invalide.")

    def play_round(self):
        nb_rd = len(self.__current_tournament.get_round_list) - 1
        rd = self.__current_tournament.get_round_list[nb_rd]
        if not rd.end_date:
            print(f"Résultat pour le {rd.name}.\n")
            print("Entrer 'J1' si J1 gagnant.")
            print("Entrer 'J2' si J2 gagnant.")
            print("Entrer 'Nul' si le match est nul.")
            self.describe_rounds(nb_rd)
            self.__current_tournament.play_round()
        else:
            print("Dernier round déjà joué.")
            print("Créez un nouveau round à jouer.\n")

    def describe_players(self, index=None, by_name=False, by_rank=False):
        players = self.__current_tournament.get_player_list
        if index is None:
            if by_name:
                players = sorted(players,
                                 key=attrgetter("last_name", "first_name"))
            elif by_rank:
                players = sorted(players, key=attrgetter("rank"))
            for player in players:
                print(player)
        else:
            try:
                print(players[index - 1])
            except IndexError:
                print("Indice invalide.\n")
            except TypeError:
                print("Format de l'indice incorrect.\n")

    def tournament_menu(self):
        pass


if __name__ == '__main__':
    m = Menu()

    tr = clt.Tournament("Tournoi", "Caen", "Bullet", "", "25/03/2021 17:00")

    m._Menu__current_tournament = tr

    plyr = [
        clt.Player("POIRIER", "Marine", "14/05/1992", "F", 1),
        clt.Player("VILLEY", "Chloé", "14/08/1989", "F", 2),
        clt.Player("VILLEY", "Karine", "29/09/1985", "F", 16),
        clt.Player("VILLEY", "Thierry", "06/09/1959", "M", 10),
        clt.Player("JOURDAN", "Evelyne", "04/10/1960", "F", 24),
        clt.Player("QUESNEY", "Dany", "07/05/1990", "M", 42),
        clt.Player("BRISE", "Vincent", "11/10/1988", "M", 6),
        clt.Player("SAINT-AUBIN", "Alana", "05/03/2016", "F", 156)
    ]

    for p in plyr:
        m._Menu__current_tournament._Tournament__player_list.append(p)

    m.add_round()
    m.describe_rounds()
    # m.play_Round()
    m.describe_players(by_name=True)
    m.describe_players(by_rank=True)
