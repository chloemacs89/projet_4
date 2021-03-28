#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Player:
    """Class to make an instance of a chess player. Includes the following
    informations :
    - First Name
    - Last Name
    - Date of Birth
    - Gender
    - Rank
    """
    def __init__(self, l_name, f_name, date_birth, gender, rank, score=0):
        """Class constructor"""
        self.last_name = l_name.capitalize()
        self.first_name = f_name.capitalize()
        self.date_birth = date_birth
        self.gender = gender.upper()
        self.rank = rank
        self.id_player = self.date_birth.replace("/", "")[4:] + "_" \
            + self.last_name[0:3].upper() \
            + self.first_name[0:3].upper()
        self.__score = score
        self.__player_saved_info = {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "date_birth": self.date_birth,
            "gender": self.gender,
            "rank": self.rank,
            "id_player": self.id_player
        }

    @property
    def get_player_saved_info(self):
        return self.__player_saved_info

    def serialize_player_tour_info(self):
        serialized_info = self.__player_saved_info.copy()
        serialized_info["score"] = self.get_player_score
        return serialized_info

    @get_player_saved_info.setter
    def set_player_saved_info(self, key, value):
        self.__player_saved_info[key] = value

    @property
    def get_player_score(self):
        return self.__score

    @get_player_score.setter
    def set_player_score(self, score):
        self.__score = self.__score + score

    def __eq__(self, other):
        return self.rank == other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __str__(self):
        if self.gender == "M":
            print("Description du joueur :")
        elif self.gender == "F":
            print("Description de la joueuse :")

        return f"""
        Nom : {self.last_name}
        Prénom : {self.first_name}
        Date de naissance : {self.date_birth}
        Sexe : {self.gender}
        Rang : {self.rank}
        Score : {self.__score}\n"""


if __name__ == '__main__':
    p1 = Player("Jean", "Michel", "14/08/1956", "M", 2)
    print(p1)
    p1.get_player_score
    p1.set_player_score = 1
    p1.get_player_score
    p1.get_player_saved_info
