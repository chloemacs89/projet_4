#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from model.interactDB import InteractDB
from tinydb import TinyDB, Query
from tinydb.operations import delete


class TournamentDB(InteractDB):
    """Class to write informations from controller into tournament DB file
    and read informations from tournament DB file to be sent to the
    controller.
    """
    def __init__(self, db_file_name):
        """Class constructor, inherit from InteractDB."""
        super(TournamentDB, self).__init__(db_file_name)

    def list_tournaments_in_db(self):
        all_tournaments = self.tournaments.search(self.info["tournament_data"].exists())
        return all_tournaments

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

    def load_tournament_from_db(self, tournament_name):
        """Return a tuple of dict object with saved tournaments data. If there is no players list
        and no rounds list, dict objects are empty dict."""
        global_data = self.tournaments.get(self.info["tournament_data"]["tournament_info"]["name"] == tournament_name)
        if global_data:
            trn_info = global_data["tournament_data"]["tournament_info"]
            try:
                players_info = global_data["tournament_data"]["players_list"]
            except KeyError:
                players_info = None
            try:
                rounds_info = global_data["tournament_data"]["rounds_list"]
            except KeyError:
                rounds_info = None

            return (trn_info, players_info, rounds_info)
        else:
            raise Warning("Tournoi inexistant dans la base de données.")


if __name__ == '__main__':
    db = TinyDB("tournamentdb.json")

    tournaments = db.table("Tournaments")

    for x in tournaments.search(Query()["tournament_data"].exists()):
        print(x["tournament_data"]["tournament_info"])

    ft_inf = tournaments.get(Query()["tournament_data"]["tournament_info"]["name"] == "Tournoi")
    ft_inf["tournament_data"]["tournament_info"]
    ft_inf["tournament_data"]["players_list"]
    ft_inf["tournament_data"]["rounds_list"]

    test = TournamentDB("tournamentdb.json")
    info = test.load_tournament_from_db("Tournoi")
    info[1]
    info[2]
