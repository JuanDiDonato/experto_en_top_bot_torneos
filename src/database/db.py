# -*- encoding: utf-8 -*-

import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.URI = os.getenv("MONGO_URI")

    def conection(self):
        try:
            client = MongoClient(str(self.URI))
            print("Base de datos conectada")
            self.db = client["tournament"]  # Crea una base de datos
        except:
            print("No se pudo conectar a la base de datos")

    """
    Crea las collecciones
    """

    def create_collections(self):
        self.players = self.db["players"]  # Crea una colleccion players
        self.tournament = self.db["tournaments"]

    """
    Verifica si un jugador ya esta en la base de datos
    """

    def exists(self, ds_id):
        players = self.players.find({"player_ds_id": f"{ds_id}"})
        if len(list(players)) > 0:
            return True
        return False

    """
    Agrega un jugador a la db. si ya existe, acutaliza su nombre
    """

    def insert_one_player(self, player):
        if self.exists(player["player_ds_id"]) == False:
            self.players.insert_one(player)
        else:
            self.players.update_one(
                {"player_ds_id": player["player_ds_id"]},
                {"$set": {"player_lol_name": player["player_lol_name"]}},
            )

    """
    Agrega una lista de jugadores a la base de datos
    """

    def insert_many_players(self, players):
        new_players = []

        for player in players:
            if self.exists(player["player_ds_id"]) == False:
                new_players.append(player)

        if len(new_players) > 0:
            self.players.insert_many(new_players)

    """
    Obtener jugadores
    """

    def get_players(self):
        return list(self.players.find({}))

    """
    Agrega el torneo en la base de datos
    """

    def insert_tournament(self, tournament):
        if len(self.get_tournament()) == 0:
            self.tournament.insert_one(tournament)
            return True
        else:
            return False

    """
    Obtiene el torneo activo
    """

    def get_tournament(self):
        return list(self.tournament.find({}))

    """
    Actualiza datos del torneo
    """

    def update_tournament(self, points):
        self.tournament.update_one(
            {"name": "Los Pibardos"}, {"$set": {"points": points}}
        )

    """
    Borra un torneo activo
    """

    def delete_tournament(self):
        self.tournament.delete_one({"name": "Los Pibardos"})

    """
    Inicia la base de datos
    """

    def start_db(self):
        self.conection()
        self.create_collections()
