#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from tinydb import TinyDB, Query


class LoadPlayer:
    """Class to load a player from player's database and
    send the data to the controller to make a Player instance.
    """
    def __init__(self, db_file_name):
        """Class constructor, takes players db file name
        and set the db's directory path."""
        self.db_file_name = db_file_name
        self.db_dir_path = os.path.join("data", db_file_name)
