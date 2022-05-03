# -*- coding: utf-8 -*-

class Tournament:
    def __init__(self,players):
        self.players = players

    def Validation(self,players):
        if len(players) % 2:
            players.append("Fecha libre")  # Si el numero es impar, agrega un jugador mas.
        self.rotation = list(players)

    def League(self,players):
        league = []
        for i in range(0, len(players) -1 ):
            league.append(self.rotation)
            self.rotation = [self.rotation[0]] + [self.rotation[-1]] + self.rotation[1:-1]
        return league

    def Generate(self):
        self.Validation(self.players)
        return self.League(self.players)