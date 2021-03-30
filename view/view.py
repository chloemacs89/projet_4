#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime as dt
from operator import attrgetter

import model.tournament as trn


def show_message(message):
    print(message, "\n")


def show_listed_data(data_list):
    for data in data_list:
        print(data)


def show_done_action(message=None, current_val=None, max_val=None):
    if message and current_val and max_val:
        print(message, f"{current_val}/{max_val}\n")
    else:
        print("Opération terminée.\n")


def show_warning(message):
    print(f"### {message.upper()} ###\n")


def show_start_menu(date, hour):
    print("Bienvenue dans votre application de gestion de tournois d'échec.")
    print(f"Nous somme le {date} à {hour}.\n")

    print("Catégories disponibles.")
    print("==============================\n")
    print("Créer un nouveau tournoi (1)")
    print("Accéder au menu du tournoi en cours (2)")
    print("Charger un tournoi depuis la base de données (3)")
    print("Afficher la liste des tournois (4)")
    print("Changer le tournoi en cours (5)")
    print("Quitter l'application (q)\n")


def show_create_tournament():
    print("========================================")
    print("Bienvenue dans la création d'un tournoi.")
    print("========================================\n")


def show_tournament_menu(name, localization, start_date):
    print("==============================")
    print(f"{name}, ", end='')
    print(f"{localization}, ", end='')
    print(f"{start_date}.")
    print("==============================\n")

    print("Ajouter un joueur au tournoi. (1)")
    print("Ajouter une nouveller ronde au tournoi. (2)")
    print("Accéder au menu des rondes. (3)")
    print("Marquer le tournoi comme terminé. (4)")
    print("Afficher la liste des joueurs (5)")
    print("Accéder au menu des sauvegardes des joueurs. (6)")
    print("Accéder au menu de chargement des joueurs. (7)")
    print("Revenir au menu principal (q)\n")


def show_rounds_report(name, match_list, start_date, end_date):
    print(f"{name}")
    print(f"Début de la ronde : {start_date}\n")
    for e, i in enumerate(match_list):
        play1 = f"{i[0][0].first_name} {i[0][0].last_name}"
        play2 = f"{i[0][1].first_name} {i[0][1].last_name}"
        score = i[1]
        print(f"Match n°{e+1} :")
        print(f"(J1) {play1} vs {play2} (J2) -- Score : {score}\n")
    if end_date:
        print(f"Fin du round : {end_date}\n")
        print("==============================\n")
    else:
        print("Fin du round : round en cours\n")
        print("==============================\n")


def show_players_report():
    print("Afficher la liste des joueurs (à défaut, l'affichage se fait pas ordre d'ajout) :\n")
    print("Par ordre alphabatique (1)")
    print("Par ordre de classement (2)")
    print("Afficher un joueur spécifique (3)")


def show_rounds_menu():
    print("==============================")
    print("Menu des rondes")
    print("==============================\n")
    print("Afficher une ronde spécifique. (1)")
    print("Afficher l'ensemble des rondes du tournoi (2)")
    print("Entrer les résultats de la ronde en cours (3)")
    print("Retour au menu du tournoi. (q)\n")


def show_play_menu(round_name):
    print(f"Résultat pour le {round_name}.\n")
    print("Entrer 'J1' si J1 gagnant.")
    print("Entrer 'J2' si J2 gagnant.")
    print("Entrer 'Nul' si le match est nul.")


def show_save_player_menu():
    print("==============================")
    print("Menu de sauvegarde des joueurs dans la base de données")
    print("==============================\n")

    print("Afficher la liste des fichier de la base de données. (1)")
    print("Sauvegarder les joueurs dans la base de données (2)")
    print("Retourner au menu du tournoi. (q)\n")


def show_load_player_menu():
    print("==============================")
    print("Menu de chargement des joueurs depuis la base de données.")
    print("==============================\n")
    print("Afficher la liste des fichiers de la base de données. (1)")
    print("Afficher la liste des joueurs présents dans un fichier spécifique. (2)")
    print("Ajouter un joueur depuis la base de données. (3)")
    print("Retourner au menu du tournoi. (q)\n")


def show_key_val_data(dict_data):
    for key, val in dict_data.items():
        print(key, ":", val, end=", ")
    print()


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
            print("Changer le tournoi en cours (5)")
            print("Quitter l'application (q)\n")
            resp = input("Choix : ")
            if resp in ("1", "2", "3", "4", "5", "q"):
                break
            else:
                print("Choix invalide")

        if resp == "1":
            self.create_tournament()
            self.tournament_menu()
        elif resp == "2":
            if self.__tournament_list:
                self.tournament_menu()
            else:
                print(
                    " !! Action impossible, aucun tournoi n'a encore été créé ou chargé. !!\n"
                )
                self.start_menu()
        elif resp == "3":
            # TODO: Fonctionnalité à implémenter dans le modèle et le contrôleur.
            pass
        elif resp == "4":
            if self.__tournament_list:
                for tournament in self.__tournament_list:
                    print(tournament)
                self.start_menu()
            else:
                print(
                    " !! Action impossible, aucun tournoi n'a encore été créé ou chargé. !!\n"
                )
                self.start_menu()
        elif resp == "5":
            index = int(input("N° du tournoi à selectionner : "))
            if self.__tournament_list:
                try:
                    self.__current_tournament = self.__tournament_list[index -
                                                                       1]
                    print("Tournoi selectionné : ", end='')
                    print(self.tournament_menu[index - 1])
                    print()
                    self.start_menu()
                except IndexError:
                    print("Tournoi n°{index} inexistant.\n")
                    self.start_menu()
                except ValueError:
                    print("Format de l'index invalide.\n")
                    self.start_menu()
            else:
                print(
                    "Aucun tournoi inscrit dans la liste. Veuillez créer ou charger un tournoi.\n"
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
        print("========================================")
        print("Bienvenue dans la création d'un tournoi.")
        print("========================================\n")

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

        chess_tournament = trn.Tournament(name, localization, time_control,
                                          description, beg_date)
        self.__tournament_list.append(chess_tournament)
        self.__current_tournament = chess_tournament

    @property
    def get_tournament_list(self):
        return self.__tournament_list

    def add_player_to_tournament(self):
        if len(self.__current_tournament.get_player_list
               ) < self.__current_tournament.MAX_PLAYER_LIMIT:
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
                f"({len(self.__current_tournament.get_player_list)}/{self.__current_tournament.MAX_PLAYER_LIMIT})"
            )

        else:
            print("Nombre de joueurs maximum atteint.")

    def add_round(self):
        last_round_nb = len(self.__current_tournament.get_round_list)

        if len(self.__current_tournament.get_player_list
               ) != self.__current_tournament.MAX_PLAYER_LIMIT:
            print("Nombre de joueurs inscrits insuffisant.")
            print("Veuillez ajouter au moins 8 joueurs.\n")

        if len(self.__current_tournament.get_round_list
               ) < self.__current_tournament.MAX_ROUND_LIST:

            if not self.__current_tournament.get_round_list:
                round_nb = 1
                round_name = f"Round {round_nb}"
                print(f"Création du {round_name} en cours...")
                self.__current_tournament.add_round_to_list(round_name)
                print("Création terminée.")

            elif not self.__current_tournament.get_round_list[last_round_nb -
                                                              1].end_date:
                print("La dernière ronde n'a pas encore été jouée.")
                print(
                    "Veuillez entrer les résultats avant de créer une nouvelle ronde.\n"
                )

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
            print(f"Fin du round : {rd.end_date}\n")
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
        try:
            nb_rd = len(self.__current_tournament.get_round_list) - 1
            rd = self.__current_tournament.get_round_list[nb_rd]

            if not rd.end_date:
                print(f"Résultat pour le {rd.name}.\n")
                print("Entrer 'J1' si J1 gagnant.")
                print("Entrer 'J2' si J2 gagnant.")
                print("Entrer 'Nul' si le match est nul.")
                self.describe_rounds(nb_rd)

                for nb, game in enumerate(rd.get_match_list):
                    while True:
                        result = input(
                            f"Résultat match {nb+1} (J1, J2 ou nul) : ")
                        if result.upper() in ("J1", "J2", "NUL"):
                            self.__current_tournament.play_round(game, result)
                            break
                        else:
                            print("Commande invalide !\n")
                while True:
                    date = input(
                        "Date de fin de la ronde (JJ/MM/AAAA HH:MM) : ")
                    try:
                        dt.strptime(date, "%d/%m/%Y %H:%M")
                        rd.end_date = date
                        break
                    except ValueError:
                        print("Format de date invalide.\n")

            else:
                print("Dernier round déjà joué.")
                print("Créez un nouveau round à jouer.\n")
        except IndexError:
            print(
                "Opération impossible. Veuillez créer une ronde au préalable.")
        except Warning:
            print(
                "Opération impossible, la dernière ronde n'est pas terminée.")

    def rounds_menu(self):
        print("==============================")
        print("Menu des rondes")
        print("==============================\n")
        print("Afficher une ronde spécifique. (1)")
        print("Afficher l'ensemble des rondes du tournoi (2)")
        print("Entrer les résultats de la ronde en cours (3)")
        print("Retour au menu du tournoi. (q)\n")

        while True:
            choice = input("Choix : ")
            print()
            if choice == "1":
                try:
                    index = int(
                        input(
                            "Numéro de la ronde à afficher (1, 2, 3 ou 4) : "))
                except ValueError:
                    print("Format de l'index invalide.\n")
                    break
                try:
                    self.describe_rounds(index - 1)
                    break
                except IndexError:
                    print(f"Ronde n°{index} inexistante.\n")
                    break
            elif choice == "2":
                self.describe_rounds()
                break
            elif choice == "3":
                self.play_round()
                break
            elif choice == "q":
                break
            else:
                print("Comment invalide.\n")
        if choice in ("1", "2", "3", "4"):
            self.rounds_menu()

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

    # TU EN ES LA #############################################################

    def get_file_list(self):
        for files in self.__current_tournament.get_file_list():
            print(files)

    def add_player_from_db(self, db_file, player_id):
        try:
            self.__current_tournament.add_player_from_db(db_file, player_id)
        except Exception as err:
            print("Opération impossible :", err)
        except Warning as err:
            print("Opération impossible :", err)

    def get_player_list_from_db(self, db_file):
        for player in self.__current_tournament.get_player_list_from_db(
                db_file):
            for key, val in player.items():
                print(key, ":", val, end=", ")
            print()

    def describe_players_menu(self):
        print(
            "Afficher la liste des joueurs (à défaut, l'affichage se fait pas ordre d'ajout) :\n"
        )
        print("Par ordre alphabatique (1)")
        print("Par ordre de classement (2)")
        print("Afficher un joueur spécifique (3)")

        while True:
            resp = input("Choix : ")
            if resp == "1":
                self.describe_players(by_name=True)
                break
            elif resp == "2":
                self.describe_players(by_rank=True)
                break
            elif resp == "3":
                index = int(
                    input("Joueur à afficher (choisir entre 1 et 8) : "))
                self.describe_players(index=index)
                break
            else:
                self.describe_players()
                break

    def load_player_menu(self):
        print("==============================")
        print("Menu de chargement des joueurs depuis la base de données.")
        print("==============================\n")
        print("Afficher la liste des fichiers de la base de données. (1)")
        print(
            "Afficher la liste des joueurs présents dans un fichier spécifique. (2)"
        )
        print("Ajouter un joueur depuis la base de données. (3)")
        print("Retourner au menu du tournoi. (q)\n")

        while True:
            resp = input("Choix : ")
            if resp == "1":
                self.get_file_list()
                break
            elif resp == "2":
                db_file = input("Nom du fichier : ")
                self.get_player_list_from_db(db_file)
                break
            elif resp == "3":
                db_file = input("Nom du fichier : ")
                player_id = input(
                    "Entrer l'identifiant du joueur à ajouter (1000_AA) : ")
                self.add_player_from_db(db_file, player_id)
                break
            elif resp == "q":
                break
            else:
                print("Commande invalide !\n")

        if resp in ("1", "2", "3", "4"):
            self.load_player_menu()

    def save_player_menu(self):
        print("==============================")
        print("Menu de sauvegarde des joueurs dans la base de données")
        print("==============================\n")

        print("Afficher la liste des fichier de la base de données. (1)")
        print("Sauvegarder les joueurs dans la base de données (2)")
        print("Retourner au menu du tournoi. (q)\n")

        while True:
            resp = input("Choix : ")
            if resp == "1":
                self.get_file_list()
                break
            elif resp == "2":
                db_file = input("Nom du fichier : ")
                self.save_player_into_db(db_file)
                break
            elif resp == "q":
                break

        if resp in ("1", "2"):
            self.save_player_menu()

    def save_player_into_db(self, db_file):
        for player in self.__current_tournament.get_player_list:
            try:
                self.__current_tournament.save_player_into_db(db_file, player)
            except Warning:
                print(
                    f"Joueurs ({player.get_player_saved_info['id_player']}) ",
                    end='')
                print(
                    "déjà présent dans la base de données. N'a pas été sauvegardé.\n"
                )

    def tournament_menu(self):
        print("==============================")
        print(f"{self.__current_tournament.name}, ", end='')
        print(f"{self.__current_tournament.localization}, ", end='')
        print(f"{self.__current_tournament.beg_date}.")
        print("==============================\n")

        print("Ajouter un joueur au tournoi. (1)")
        print("Ajouter une nouveller ronde au tournoi. (2)")
        print("Accéder au menu des rondes. (3)")
        print("Marquer le tournoi comme terminé. (4)")
        print("Afficher la liste des joueurs (5)")
        print("Accéder au menu des sauvegardes des joueurs. (6)")
        print("Accéder au menu de chargement des joueurs. (7)")
        print("Revenir au menu principal (q)\n")

        while True:
            resp = input("Choix : ")
            if resp == "1":
                self.add_player_to_tournament()
                break
            elif resp == "2":
                self.add_round()
                break
            elif resp == "3":
                self.rounds_menu()
                break
            elif resp == "4":
                break
            elif resp == "5":
                self.describe_players_menu()
                break
            elif resp == "6":
                self.save_player_menu()
                break
            elif resp == "7":
                self.load_player_menu()
                break
            elif resp == "q":
                break
            else:
                print("Commande invalide.")

        if resp in ("1", "2", "3", "4", "5", "6", "7"):
            self.tournament_menu()
        elif resp == "q":
            self.start_menu()


if __name__ == '__main__':
    m = Menu()

    tr = clt.Tournament("Tournoi", "Caen", "Bullet", "", "25/03/2021 17:00")

    m._Menu__current_tournament = tr

    m._Menu__tournament_list.append(tr)

    plyr = [
        trn.Player("POIRIER", "Marine", "14/05/1992", "F", 1),
        trn.Player("VILLEY", "Chloé", "14/08/1989", "F", 2),
        trn.Player("VILLEY", "Karine", "29/09/1985", "F", 16),
        trn.Player("VILLEY", "Thierry", "06/09/1959", "M", 10),
        trn.Player("JOURDAN", "Evelyne", "04/10/1960", "F", 24),
        trn.Player("QUESNEY", "Dany", "07/05/1990", "M", 42),
        trn.Player("BRISE", "Vincent", "11/10/1988", "M", 6),
        trn.Player("SAINT-AUBIN", "Alana", "05/03/2016", "F", 156)
    ]

    for p in plyr:
        m._Menu__current_tournament._Tournament__player_list.append(p)

    m.start_menu()

    m.add_round()
    m.describe_rounds()
    # m.play_Round()
    m.describe_players(by_name=True)
    m.describe_players(by_rank=True)
