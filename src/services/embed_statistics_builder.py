# -*- coding: utf-8 -*-

# Python Modules
from operator import itemgetter

# App Modules
from .embed_builder import EmbedBuilder
from ..models.Statistics import Statistics


class EmbedStatisticsBuilder(EmbedBuilder):
    __statistics: Statistics

    def __init__(self) -> None:
        super().__init__()

    def with_statistics(self, statistics: Statistics) -> EmbedBuilder:
        self.__statistics = statistics
        self.__process_statistics()
        return self

    def __process_statistics(self):
        self.__set_wins()
        self.__set_defeats()
        self.__set_winrate()
        self.__set_matches_played()

    def __set_wins(self):
        wins = self.__statistics.get_wins
        most_wins = max(wins.items(), key=itemgetter(1))[0]  # Retorna con que campeon gano mas
        self.with_field(
            name=f"Gano mas partidas con {most_wins}",
            value=f" {wins[most_wins]} victorias",
        )

    def __set_defeats(self):
        defeats = self.__statistics.get_defeat
        most_defeat = max(defeats.items(), key=itemgetter(1))[0]  # Retorna con que campeon perdio mas
        self.with_field(
            name=f"Perdio mas partidas con {most_defeat}",
            value=f"{defeats[most_defeat]} derrotas",
        )

    def __set_winrate(self):
        win_rate = self.__statistics.get_win_rate
        self.with_field(name=f"Porcentaje de victorias", value=f"{win_rate}")

    def __set_matches_played(self):
        matches = self.__statistics.get_played
        for c, p in matches.items():
            try:
                win_rate = int((self.__statistics.get_wins[c] / p) * 100)
            except:
                win_rate = 0

            self.with_field(
                name=f"{c} disputo {p} partidas", value=f" Winrate: {win_rate} %"
            )
