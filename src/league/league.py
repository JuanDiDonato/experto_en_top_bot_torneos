# -*- coding: utf-8 -*-

"""
Clase que se encarga de crear la estructura de una Liga
"""


class Tournament:
    def __init__(self, players):
        self.players = players

    """
    Verifica que la cantidad de participantes sea par, sino es asi, agrega una fecha libre
    """

    def Validation(self, players):
        if len(players) % 2:
            players.append(
                "Fecha libre"
            )  # Si el numero es impar, agrega un jugador mas.
        self.rotation = list(players)

    """
    Crea los enfrentamientos de la liga
    """

    def League(self, players):
        league = []
        for i in range(0, len(players) - 1):
            league.append(self.rotation)
            self.rotation = (
                [self.rotation[0]] + [self.rotation[-1]] + self.rotation[1:-1]
            )
        return league

    def Generate(self):
        self.Validation(self.players)
        return self.League(self.players)
