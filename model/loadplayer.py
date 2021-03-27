#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from controller.player import Player

from tinydb import TinyDB, Query


def file_list_from_dir():
    """Return list of files from 'data' directory
    """
    return os.listdir("data")


class PlayerDB:
    """Parent class for players class to interact with players
    database.
    """
    def __init__(self, db_file_name):
        """Class constructor, takes players db file name
        and set the db's directory path."""
        self.db_file_name = db_file_name

        if os.path.exists("data"):
            self.db_dir_path = os.path.join("data", db_file_name)
        else:
            os.mkdir("data")
            self.db_dir_path = os.path.join("data", db_file_name)

        self.database = TinyDB(self.db_dir_path)
        self.Players = self.database.table("Players")
        self.info = Query()



class SavePlayer(PlayerDB):
    """Class to save a player into player's database and from
    existing players in a tournament.
    """
    def __init__(self, db_file_name):
        "Class constructor, inherit from PlayerDB class constructor"
        super(SavePlayer, self).__init__(db_file_name)

    def save_player_into_db(self, player):
        """Saves player's infos into DB.
        """
        player_data = player.get_player_saved_info
        id_player = player_data["id_player"]
        id_from_db = self.Players.get(self.info["id_player"] == id_player)
        if not id_from_db:
            self.Players.insert(player_data)
        else:
            raise Warning(
                f"Joueur ({id_player}) déjà présent dans la base de données.")


class LoadPlayer(PlayerDB):
    """Class to load a player from player's database and
    send the data to the controller to make a Player instance.
    """
    def __init__(self, db_file_name):
        """Class constructor, inherit from SavePlayer init method"""
        super(LoadPlayer, self).__init__(db_file_name)

    def list_player_from_db(self):
        "Print players data from the database."
        players_info = self.Players.search(self.info["last_name"].exists())
        return players_info

    def load_player_from_db(self, player_id):
        "Get a player's informations from db to return a Player instance"
        player_exists = self.Players.get(self.info["id_player"] == player_id)
        if player_exists:
            return Player(l_name=player_exists["last_name"],
                          f_name=player_exists["first_name"],
                          date_birth=player_exists["date_birth"],
                          gender=player_exists["gender"],
                          rank=player_exists["rank"])
        else:
            raise Warning(
                f"Joueur ({player_id}) absent de la base de données. Rappel du format: '1000_AA'"
            )


if __name__ == '__main__':

    player_list = [
        Player("POIRIER", "Marine", "14/05/1992", "F", 1),
        Player("VILLEY", "Chloé", "14/08/1989", "F", 2),
        Player("VILLEY", "Karine", "29/09/1985", "F", 28),
        Player("JOURDAN", "Evelyne", "04/10/1960", "F", 12),
        Player("QUESNEY", "Dany", "07/05/1990", "M", 19),
        Player("BRISE", "Vincent", "11/01/1990", "M", 6),
        Player("VILLEY", "Thierry", "06/09/1959", "M", 10),
        Player("SAINT-AUBIN", "Alana", "05/03/2016", "F", 156)
    ]

    f = LoadPlayer("dbplayer.json")
    fs = SavePlayer("dbplayer.json")

    fs.save_player_into_db(player_list[0])

    t = f.list_player_from_db()
    player = f.load_player_from_db("1959_VT")
    player2 = f.load_player_from_db("1959_CT")
