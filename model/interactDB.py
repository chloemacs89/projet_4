#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from tinydb import TinyDB, Query


class InteractDB:
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
        self.players = self.database.table("Players")
        self.tournaments = self.database.table("Tournaments")
        self.rounds = self.database.table("rounds")
        self.match = self.database.table("match")
        self.info = Query()
