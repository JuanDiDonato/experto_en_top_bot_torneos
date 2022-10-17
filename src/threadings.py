# -*- coding: utf-8 -*-

import time

from database.db import Database
from riot_api.riot_api import RiotAPI


class Threadings:

    """
    Posee las funciones que se ejecutaran en los diferentes subprocesos
    """

    __account_data = RiotAPI()
    db = Database()
    stadistics = []
    points = {}
    rounds_saved = []
    players_saved = []
    summoners = {}
    count = 0

    # Constructor
    # def __init__(self):


    def tr_update_history(self):
        try:
            print("Sincronizando historial")
            data = self.__account_data.get_players_data(self.summoners)
            if len(data) > 0:
                self.stadistics.clear()
                self.stadistics.extend(data)
            print("Datos establecidos")
            self.count = 0
        except:
            self.count = self.count + 1
            if self.count < 3:
                time.sleep(5)
                self.tr_update_history()
            else:
                print("Error al obtener estadisticas")
                self.count = 0

    def tr_sync_tournament(self):
        tournament = self.__db.get_tournament()
        if len(tournament) > 0:
            self.points.clear()
            self.rounds_saved.clear()
            self.players_saved.clear()
            print(f"Se encontron {len(tournament)} torneos activos")
            self.points.update(tournament[0]["points"])
            self.rounds_saved.extend(tournament[0]["rounds"])
            self.players_saved.extend(tournament[0]["players"])
            print("Rondas y puntos actualizados")
        else:
            print("No se encontraron nuevos datos")
            self.points.clear()
            self.rounds_saved.clear()
            self.players_saved.clear()
            self.stadistics.clear()

    def tr_get_summoners(self):
        summoners_list = self.__db.get_players()
        for s in summoners_list:
            if self.summoners.get(s["player_ds_id"]) == None:
                self.summoners.update({s["player_ds_id"]: s["player_lol_name"]})
