# -*- encoding: utf-8 -*-

import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient


load_dotenv()


class Database:

    # Atributos de la clase
    __URI : str | None = os.getenv("MONGO_URI")
    __DATABASE_MESSAGE : str = "Base de datos conectada"
    __PLAYERS : str = "players"
    __TOURNAMENTS : str = "tournaments"
    __PLAYER_DS_ID_PARAM :str = "player_ds_id"

    def __init__(self):
        self._tournament = None
        self._players = None
        self.db = None

    def connection(self):
        try:
            client = MongoClient(self.__URI)
            print(self.__DATABASE_MESSAGE)
            self.db = client["tournament"]  # Crea una base de datos
        except:
            print("No se pudo conectar a la base de datos")

    """
    Crea las collecciones de la base de datos
    """
    def create_collections(self):
        self._players = self.db[self.__PLAYERS]  # Crea la colleccion players
        self._tournament = self.db[self.__TOURNAMENTS] # Crea la colleccion tournaments

    """
    Verifica si un jugador ya esta en la base de datos
    """
    def exists(self, ds_id):
        players = self._players.find({"player_ds_id": f"{ds_id}"})
        if len(list(players)) > 0:
            return True
        return False

    """
    Agrega un jugador a la db. si ya existe, acutaliza su nombre
    """
    def insert_one_player(self, player):
        if not self.exists(player[self.__PLAYER_DS_ID_PARAM]):
            self._players.insert_one(player)
        else:
            self._players.update_one(
                {"player_ds_id": player[self.__PLAYER_DS_ID_PARAM]},
                {"$set": {"player_lol_name": player["player_lol_name"]}},
            )

    """
    Agrega una lista de jugadores a la base de datos
    """
    def insert_many_players(self, players):
        new_players = []

        for player in players:
            if not self.exists(player["player_ds_id"]):
                new_players.append(player)

        if len(new_players) > 0:
            self._players.insert_many(new_players)

    """
    Obtener jugadores
    """
    def get_players(self):
        return list(self._players.find({}))

    """
    Agrega el torneo en la base de datos
    """
    def insert_tournament(self, tournament):
        if len(self.get_tournament()) == 0:
            self._tournament.insert_one(tournament)
            return True
        else:
            return False

    """
    Obtiene el torneo activo
    """
    def get_tournament(self):
        return list(self._tournament.find({}))

    """
    Actualiza datos del torneo
    """
    def update_tournament(self, points):
        self._tournament.update_one(
            {"name": "Los Pibardos"}, {"$set": {"points": points}}
        )

    """
    Borra un torneo activo
    """
    def delete_tournament(self):
        self._tournament.delete_one({"name": "Los Pibardos"})

    """
    Inicia la base de datos
    """
    def start_db(self):
        self.connection()
        self.create_collections()
