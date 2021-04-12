#!/usr/bin/env python
# -*- coding: utf-8 -*-

def show_message(message):
    print(message, "\n")


def show_listed_data(data_list):
    print("------------------------------")
    for data in data_list:
        print(data)
    print("------------------------------\n")


def show_done_action(message=None, current_val=None, max_val=None):
    if message and current_val and max_val:
        print(message, "-", f"({current_val}/{max_val})\n")
    else:
        print("Opération terminée.\n")


def show_warning(message):
    print(f"### {message.upper()} ###\n")


def show_start_menu(date, hour):
    print("\nBienvenue dans votre application de gestion de tournois d'échec.")
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
    print("\n========================================")
    print("Bienvenue dans la création d'un tournoi.")
    print("========================================\n")


def show_tournament_menu(name, localization, start_date):
    print("\n============================================================")
    print(f"{name}, ", end='')
    print(f"{localization}, ", end='')
    print(f"{start_date}.")
    print("============================================================\n")

    print("Ajouter un joueur au tournoi. (1)")
    print("Ajouter une nouvelle ronde au tournoi. (2)")
    print("Accéder au menu des rondes. (3)")
    print("Marquer le tournoi comme terminé. (4)")
    print("Afficher la liste des joueurs (5)")
    print("Accéder au menu des sauvegardes des joueurs. (6)")
    print("Accéder au menu de chargement des joueurs. (7)")
    print("Sauvgarder le tournoi. (8)")
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
    print("\nAfficher la liste des joueurs (à défaut, l'affichage se fait pas ordre d'ajout) :\n")
    print("Par ordre alphabatique (1)")
    print("Par ordre de classement (2)")
    print("Afficher un joueur spécifique (3)")
    print("Modifier le rang d'un joueur (4)\n")


def show_load_tournament_menu():
    print("\n==============================")
    print("Menu du chargement des tournois.")
    print("==============================\n")
    print("Afficher la liste des fichers de la base de données. (1)")
    print("Affiche les tournois sauvegardés dans un fichier spécifique. (2)")
    print("Charger un tournoi à partir d'un fichier. (3)")
    print("Retour au menu principal. (q)\n")


def show_rounds_menu():
    print("\n==============================")
    print("Menu des rondes")
    print("==============================\n")
    print("Afficher une ronde spécifique. (1)")
    print("Afficher l'ensemble des rondes du tournoi (2)")
    print("Entrer les résultats de la ronde en cours (3)")
    print("Retour au menu du tournoi. (q)\n")


def show_play_menu(round_name):
    print(f"\nRésultat pour le {round_name}.\n")
    print("Entrer 'J1' si J1 gagnant.")
    print("Entrer 'J2' si J2 gagnant.")
    print("Entrer 'Nul' si le match est nul.\n")


def show_save_player_menu():
    print("\n====================================================")
    print("Menu de sauvegarde des joueurs dans la base de données")
    print("======================================================\n")

    print("Afficher la liste des fichier de la base de données. (1)")
    print("Sauvegarder les joueurs dans la base de données (2)")
    print("Retourner au menu du tournoi. (q)\n")


def show_load_player_menu():
    print("\n=======================================================")
    print("Menu de chargement des joueurs depuis la base de données.")
    print("=========================================================\n")
    print("Afficher la liste des fichiers de la base de données. (1)")
    print("Afficher la liste des joueurs présents dans un fichier spécifique. (2)")
    print("Ajouter un joueur depuis la base de données. (3)")
    print("Retourner au menu du tournoi. (q)\n")


def show_key_val_data(dict_data):
    for key, val in dict_data.items():
        print(key, ":", val, end=", ")
    print()


def ask_user_input(message):
    choice = input(f"{message}")
    print()
    return choice
