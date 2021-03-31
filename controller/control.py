#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from operator import attrgetter
from datetime import datetime as dt

import model.tournament as trn
import view.view as view
import model.playerdb as lpdb
import model.tournamentdb as trdb


class Control:
    """Controller classe : take data from model et send it to view.
    """
    def __init__(self):
        """Constructor : no arguments needed"""
        self.today = dt.strftime(dt.today(), "%d/%m/%Y")
        self.current_time = dt.strftime(dt.today(), "%H:%M")
        self.tournament_list = []
        self.current_tournament = None
        self.error_messages = {
            "UNKNOWN_COMMAND": "Commande invalide !",
            "MISSING_FILE": "Fichier inexistant !",
            "NO_TOURNAMENT": "Action impossible : aucun tournoi n'a encore été créé ou chargé !",
            "ADD_PLAYER": "Action impossible : veuillez ajouter suffisamment de joueurs au tournoi",
            "MISSING_INDEX": "Index invalide",
            "INVALIDE_FORMAT": "Format invalide",
            "INVALID_DATE": "Format ou date invalide.",
            "INVALID_INT": "Doit être un entier strictement positif.",
            "MAX_PLAYER": "Action impossible : nombre de joueurs maximum atteint.",
            "MAX_ROUND": "Action impossible : nombre de ronde maximum atteint.",
            "MISSING_ROUND": "Action impossible : aucune ronde n'existe.",
            "ONGOING_ROUND": "Action impossible : veuillez terminer la ronde en cours.",
            "DONE_ROUND": "Action impossible : la dernière ronde a déjà été jouée.",
            "MISSING_TOURNAMENT": "Action impossible : nom de tournoi absent de la base de données.",
            "ONGOING_TOURNAMENT": "Action impossible : toutes les rondes n'ont pas encore été jouées."
        }

    @staticmethod
    def get_file_list():
        """Return a list of files inside data directory. List is then
        displayed by view.
        """
        file_list = os.listdir("data")
        view.show_listed_data(file_list)
        return file_list

    def get_player_list_from_db(self, file_name):
        if file_name in self.get_file_list():
            load = lpdb.LoadPlayer(file_name)
            players = load.list_player_from_db()
            for player in players:
                view.show_key_val_data(player)
        else:
            view.show_warning(self.error_messages["MISSING_FILE"])

    def start_menu(self):
        """Ask the user to choose between the various start menu
        options displayed by view.
        """
        view.show_start_menu(self.today, self.current_time)

        while True:
            resp = input("Choix : ")
            if resp == "1":
                self.create_tournament()
                break
            elif resp == "2":
                if self.tournament_list:
                    self.tournament_menu()
                else:
                    view.show_warning(self.error_messages["NO_TOURNAMENT"])
                    break
            elif resp == "3":
                self.load_tournament_menu()
                break
            elif resp == "4":
                if self.tournament_list:
                    view.show_listed_data(self.tournament_list)
                    break
                else:
                    view.show_warning(self.error_messages["NO_TOURNAMENT"])
                    break
            elif resp == "5":
                index = int(input("N° du tournoi à selectionner : "))
                if self.tournament_list:
                    try:
                        self.current_tournament = self.tournament_list[index - 1]
                        view.show_message(f"Tournoi selectionné : {self.tournament_list[index - 1]}")
                        break
                    except IndexError:
                        view.show_warning(self.error_messages["MISSING_INDEX"])
                        break
                    except ValueError:
                        view.show_warning(self.error_messages["INVALIDE_FORMAT"])
                        break
                else:
                    view.show_warning(self.error_messages["NO_TOURNAMENT"])
                    break
            elif resp == "q":
                break
            else:
                view.show_warning(self.error_messages["UNKNOWN_COMMAND"])

        if resp == "1":
            self.tournament_menu()
        elif resp in ("2", "3", "4", "5"):
            self.start_menu()
        elif resp == "q":
            confirmation = input("êtes-vous sûr de vouloir quitter l'application ? (O/N)")
            if confirmation.lower() == "n":
                self.start_menu()
            elif confirmation.lower() == "o":
                quit()

    def create_tournament(self):
        """Ask the user for the informations needed to make an instance
        of a class Tournament.
        """
        view.show_create_tournament()
        name = input("Nom du tournoi : ")
        localization = input("Lieu du tournoi : ")

        while True:
            time_control = input(
                "Type de contrôle du temps (Bullet, Blitz ou Coup rapide) : ")
            if time_control.lower() in ("bullet", "blitz", "coup rapide"):
                break
            else:
                view.show_warning(self.error_messages["INVALIDE_FORMAT"])

        description = input("Description du tournoi (optionnel) : ")

        while True:
            beg_date = input("Date de début du tournoi (JJ/MM/AAAA HH:MM): ")
            try:
                dt.strptime(beg_date, "%d/%m/%Y %H:%M")
                break
            except ValueError:
                view.show_warning(self.error_messages["INVALID_DATE"])

        chess_tournament = trn.Tournament(name, localization, time_control,
                                          description, beg_date)
        self.tournament_list.append(chess_tournament)
        self.current_tournament = chess_tournament

    def add_player_to_tournament(self):
        """Ask the user for the required arguments needed to make a new Player instance
        and add it to the current tournament.
        """
        if len(self.current_tournament.get_player_list) < self.current_tournament.MAX_PLAYER_LIMIT:
            view.show_message("Adding a new player. Please enter the following informations.")
            l_name = input("Last name: ")
            f_name = input("First name: ")

            while True:
                date_birth = input("Date of birth (JJ/MM/AAAA): ")
                # check date validity. Numbers validity and calendar validity
                try:
                    dt.strptime(date_birth, "%d/%m/%Y")
                    break
                except ValueError:
                    view.show_warning(self.error_messages["INVALID_DATE"])

            while True:
                gender = input("Gender (M/F): ")
                if gender.upper() in ("M", "F"):
                    break
                else:
                    view.show_warning(self.error_messages["INVALIDE_FORMAT"])

            while True:
                try:
                    rank = int(input("Rank (must be a positive integer): "))
                    if isinstance(rank, int) and rank > 0:
                        break
                    else:
                        view.show_warning(self.error_messages["INVALID_INT"])
                except ValueError:
                    view.show_warning(self.error_messages["INVALID_INT"])

            self.current_tournament.add_new_player(l_name, f_name,
                                                   date_birth, gender, rank)
            view.show_done_action("Création terminée",
                                  len(self.current_tournament.get_player_list),
                                  self.current_tournament.MAX_PLAYER_LIMIT)
        else:
            view.show_warning(self.error_messages["MAX_PLAYER"])

    def tournament_menu(self):
        """Ask the user to chooses between the various options availables
        in the tournament_menu, as displayed by view.
        """
        view.show_tournament_menu(self.current_tournament.name,
                                  self.current_tournament.localization,
                                  self.current_tournament.beg_date)
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
            elif resp == "8":
                self.save_tournament_in_db()
                break
            elif resp == "q":
                break
            else:
                view.show_warning(self.error_messages["UNKNOWN_COMMAND"])

        if resp in ("1", "2", "3", "4", "5", "6", "7"):
            self.tournament_menu()
        elif resp == "q":
            self.start_menu()

    def rounds_menu(self):
        """Ask the user to choose between the various options available
        in the rounds menu, as displayed by view.
        """
        view.show_rounds_menu()

        while True:
            choice = input("Choix : ")
            print()
            if choice == "1":
                try:
                    index = int(input("Numéro de la ronde à afficher (1, 2, 3 ou 4) : "))
                except ValueError:
                    view.show_warning(self.error_messages["INVALIDE_FORMAT"])
                    break
                try:
                    self.describe_rounds(index - 1)
                    break
                except IndexError:
                    view.show_warning(self.error_messages["MISSING_INDEX"])
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
                view.show_warning(self.error_messages["UNKNOWN_COMMAND"])
        if choice in ("1", "2", "3", "4"):
            self.rounds_menu()

    def add_round(self):
        """Add a round to the current tournament by calling the add_round_to_list
        method of the current tournament instance. Display a warning if :
        - Not enough players added to the tournament ;
        - Last round hasn't been played yet ;
        - MAX_ROUND_LIST has been reached.
        """
        last_round_nb = len(self.current_tournament.get_round_list)

        if len(self.current_tournament.get_player_list) != self.current_tournament.MAX_PLAYER_LIMIT:
            view.show_warning(self.error_messages["ADD_PLAYER"])

        elif len(self.current_tournament.get_round_list) < self.current_tournament.MAX_ROUND_LIST:

            if not self.current_tournament.get_round_list:
                round_nb = 1
                round_name = f"Round {round_nb}"
                self.current_tournament.add_round_to_list(round_name)
                view.show_done_action(f"Creation : {round_name}",
                                      round_nb,
                                      self.current_tournament.MAX_ROUND_LIST)

            elif not self.current_tournament.get_round_list[last_round_nb - 1].end_date:
                view.show_warning(self.error_messages["ONGOING_ROUND"])

            else:
                round_nb = len(self.current_tournament.get_round_list) + 1
                round_name = f"Round {round_nb}"
                self.current_tournament.add_round_to_list(round_name)
                view.show_done_action(f"Creation : {round_name}",
                                      round_nb,
                                      self.current_tournament.MAX_ROUND_LIST)

        else:
            view.show_warning(self.error_messages["MAX_ROUND"])

    def describe_rounds(self, index=None):
        """Show the rounds report. If index argument is given, a unique round
        is displayed.
        """
        if index is None:
            for rd in self.current_tournament.get_round_list:
                start_date = dt.strftime(rd.start_date, "%d/%m/%Y - %H:%M")
                view.show_rounds_report(rd.name, rd.match_list, start_date, rd.end_date)
        else:
            try:
                rd = self.current_tournament.get_round_list[index]
                start_date = dt.strftime(rd.start_date, "%d/%m/%Y - %H:%M")
                view.show_rounds_report(rd.name, rd.match_list, start_date, rd.end_date)
            except IndexError:
                view.show_warning(self.error_messages["MISSING_INDEX"])
            except TypeError:
                view.show_warning(self.error_messages["INVALIDE_FORMAT"])

    def play_round(self):
        """Play the last round added to the tournament by calling the play_round
        method of the current tournament instance.
        """
        try:
            nb_rd = len(self.current_tournament.get_round_list) - 1
            rd = self.current_tournament.get_round_list[nb_rd]

            if not rd.end_date:
                view.show_play_menu(rd.name)
                self.describe_rounds(nb_rd)

                for nb, game in enumerate(rd.get_match_list):
                    while True:
                        result = input(
                            f"Résultat match {nb+1} (J1, J2 ou nul) : ")
                        if result.upper() in ("J1", "J2", "NUL"):
                            self.current_tournament.play_round(rd, game, result)
                            break
                        else:
                            view.show_warning(self.error_messages["UNKNOWN_COMMAND"])
                while True:
                    date = input(
                        "Date de fin de la ronde (JJ/MM/AAAA HH:MM) : ")
                    try:
                        dt.strptime(date, "%d/%m/%Y %H:%M")
                        rd.end_date = date
                        break
                    except ValueError:
                        view.show_warning(self.error_messages["INVALIDE_FORMAT"])

            else:
                view.show_warning(self.error_messages["DONE_ROUND"])
        except IndexError:
            view.show_warning(self.error_messages["MISSING_ROUND"])
        except Warning:
            view.show_warning(self.error_messages["ONGOING_ROUND"])

    def describe_players_menu(self):
        """Send the information needed by view to display the list of players
        can be displayed by :
        - Alphabetical order ;
        - Rank order ;
        - A unique player if index argument is given.
        """
        view.show_players_report()

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
                view.show_warning(self.error_messages["UNKNOWN_COMMAND"])

    def describe_players(self, index=None, by_name=False, by_rank=False):
        players = self.current_tournament.get_player_list
        if index is None:
            if by_name:
                players = sorted(players,
                                 key=attrgetter("last_name", "first_name"))
                view.show_listed_data(players)
            elif by_rank:
                players = sorted(players, key=attrgetter("rank"))
                view.show_listed_data(players)
        else:
            try:
                print(players[index - 1])
            except IndexError:
                view.show_warning(self.error_messages["MISSING_INDEX"])
            except TypeError:
                view.show_warning(self.error_messages["INVALIDE_FORMAT"])

    def add_player_from_db(self, db_file, player_id):
        try:
            self.current_tournament.add_player_from_db(db_file, player_id)
        except Exception as err:
            print("Opération impossible :", err)
        except Warning as err:
            print("Opération impossible :", err)

    def save_player_menu(self):
        view.show_save_player_menu()

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
        for player in self.current_tournament.get_player_list:
            try:
                self.current_tournament.save_player_into_db(db_file, player)
            except Warning as err:
                view.show_message(err)

    def load_player_menu(self):
        view.show_load_player_menu()

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
                player_id = input("Entrer l'identifiant du joueur à ajouter (1000_ABCDEF) : ")
                self.add_player_from_db(db_file, player_id)
                break
            elif resp == "q":
                break
            else:
                view.show_warning(self.error_messages["UNKNOWN_COMMAND"])

        if resp in ("1", "2", "3", "4"):
            self.load_player_menu()

    def load_tournament_menu(self):
        view.show_load_tournament_menu()
        while True:
            resp = input("Choix : ")
            if resp == "1":
                self.get_file_list()
                break
            elif resp == "2":
                self.list_tournaments_in_db()
                break
            elif resp == "3":
                self.load_tournament_from_db()
                break
            elif resp == "q":
                break
            else:
                view.show_warning(self.error_messages["UNKNOWN_COMMAND"])

        if resp in ("1", "2", "3"):
            self.load_tournament_menu()
        elif resp == "q":
            self.start_menu()

    def set_tournament_end_date(self):
        while True:
            date = input("Choisir une date de fin (JJ/MM/AAAA) : ")
            try:
                self.current_tournament.end_tournament(date)
                break
            except Warning:
                view.show_warning(self.error_messages["INVALID_DATE"])
            except Exception:
                view.show_warning(self.error_messages["ONGOING_TOURNAMENT"])
                break

        self.tournament_menu()

    def load_tournament_from_db(self):
        """Load a saved tournament avalable in the database.
        """
        view.show_message("Fichiers existants : ")
        self.get_file_list()
        file_name = input("Nom du fichier de chargement : ")
        loader = trdb.TournamentDB(file_name)
        name = input("Nom du tournoi à charger : ")
        try:
            tournament_data = loader.load_tournament_from_db(name)
            tournament_info = tournament_data[0]
            players_info = tournament_data[1]
            rounds_info = tournament_data[2]

            loaded_tournament = trn.Tournament(tournament_info["name"],
                                               tournament_info["localization"],
                                               tournament_info["time_control"],
                                               tournament_info["description"],
                                               tournament_info["beg_date"],
                                               tournament_info["end_date"])

            if players_info:
                for e, players in enumerate(players_info):
                    player = players[f"player{e}"]
                    loaded_tournament.add_new_player(player["last_name"],
                                                     player["first_name"],
                                                     player["date_birth"],
                                                     player["gender"],
                                                     player["rank"])

            # Saved rounds data only contains scores. The rounds are build
            # through the application internal logic. Scores are added only
            # if the saved rounds data has an end_date
            if rounds_info:
                for e, rnd in enumerate(rounds_info):
                    if rnd[f"Round {e+1}"]["end_date"] is None:
                        pass
                    else:
                        loaded_tournament.add_round_to_list(f"Round {e+1}")
                        currrent_round = loaded_tournament.get_round_list[e]
                        for nb, game in enumerate(currrent_round.get_match_list):
                            score1 = rnd[f"Round {e+1}"][f"game {nb + 1}"][0]
                            score2 = rnd[f"Round {e+1}"][f"game {nb + 1}"][1]
                            P1 = game[0][0]
                            P2 = game[0][1]
                            game[1][0] = score1
                            game[1][1] = score2
                            P1.set_player_score = score1
                            P2.set_player_score = score2
                            currrent_round.end_date = rnd[f"Round {e+1}"]["end_date"]

            self.tournament_list.append(loaded_tournament)
            self.current_tournament = loaded_tournament

        except Warning:
            view.show_warning(self.error_messages["MISSING_TOURNAMENT"])
            self.start_menu()

    def save_tournament_in_db(self):
        file_name = input("Nom du fichier de sauvegarde : ")
        update = False
        loader = trdb.TournamentDB(file_name)
        all_tournaments = loader.list_tournaments_in_db()
        for tournament in all_tournaments:
            if self.current_tournament.name in tournament["tournament_data"]["tournament_info"].values():
                update = True
            else:
                pass

        if update:
            self.current_tournament.save_tournament_in_db(file_name, update)
        else:
            self.current_tournament.save_tournament_in_db(file_name)

    def list_tournaments_in_db(self):
        """Send the tournaments data of a database file to be displayed
        by view.
        """
        view.show_message("Fichiers disponibles :\n")
        self.get_file_list()
        file_name = input("Nom du fichier : ")
        loader = trdb.TournamentDB(file_name)
        all_tournaments = loader.list_tournaments_in_db()
        for one_tournament in all_tournaments:
            view.show_key_val_data(one_tournament["tournament_data"]["tournament_info"])


if __name__ == '__main__':
    ct = Control()
    tr = trn.Tournament("Tournoi", "Caen", "Bullet", "", "25/03/2021 17:00")

    tr2 = trn.Tournament("Tour du babour", "Honfleur", "Blitz", "", "30/03/2021 10:00")

    ct.list_tournaments_in_db()

    ct.current_tournament = tr2

    ct.tournament_list.append(tr2)

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
        ct.current_tournament._Tournament__player_list.append(p)

    ct.load_tournament_from_db()
    ct.load_tournament_menu()
    ct.save_tournament_in_db()

    ct.start_menu()
    ct.describe_players(by_name=True)
