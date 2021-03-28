#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model.interactDB import InteractDB
from tinydb import TinyDB, Query
from tinydb.operations import delete
import os


class TournamentDB(InteractDB):
    """Class to write informations from controller into tournament DB file
    and read informations from tournament DB file to be sent to the
    controller.
    """
    def __init__(self, db_file_name):
        """Class constructor, inherit from InteractDB."""
        super(TournamentDB, self).__init__(db_file_name)

    def list_tournaments_in_db(self):
        pass

    def save_tournament_in_db(self, serialized_info, update=False):
        tournament_name = serialized_info["tournament_data"]["tournament_info"]["name"]
        if self.tournaments.search(self.info["tournament_data"]["tournament_info"]["name"] == tournament_name):
            if update is True:
                self.tournaments.update(delete("tournament_data"),
                                   self.info["tournament_data"]["tournament_info"]["name"] == tournament_name)
                self.tournaments.insert(serialized_info)
            else:
                raise Warning("Tournoi déjà sauvegardé dans la base de données.")
        else:
            self.tournaments.insert(serialized_info)


if __name__ == '__main__':
    db = TinyDB("tournamentdb.json")

    tournaments = db.table("Tournaments")

    tournaments.all()

    t_inf = tournaments.get(Query()["tournament_info"]["name"] == "Tournoi")
    t_inf["tournament_info"]
    for plrs in t_inf["players_list"]:
        for plr in plrs.values():
            print(plr["last_name"])
    


    tournaments.update(delete("tournament_data"), Query()["tournament_data"]["tournament_info"]["name"] == "Tournoi")


