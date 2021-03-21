#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime as dt

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
