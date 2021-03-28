#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model.interactDB import InteractDB


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
