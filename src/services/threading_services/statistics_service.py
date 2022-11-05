# -*- coding: utf-8 -*-

from ...models.Statistics import Statistics


class StatisticsService:
    __wins_by_summoners: list[Statistics] = []
    __SUMMONER: str = "summoner"
    __FECHA_LIBRE: str = "Fecha libre"
    __STATISTICS: str = "statistics"
    __CHAMP: str = "champ"
    __WIN: str = "win"

    def __int__(self) -> None:
        pass

    def set_statistics(self, statistics: list):
        if len(statistics) > 0:
            self.__process_statistics(statistics)

    @property
    def wins_by_summoners(self) -> list[Statistics]:
        return self.__wins_by_summoners

    def __process_statistics(self, statistics : list):

        """
        Procesa las estadisticas obtenidas de la api
        """

        for s in statistics:
            if s[self.__SUMMONER] != self.__FECHA_LIBRE:
                stats: Statistics = Statistics()
                wins = {}
                defeat = {}
                played = {}
                win_count = 0
                def_count = 0
                try:
                    for p in s[self.__STATISTICS]:

                        try:
                            played[p[self.__CHAMP]] = played[p[self.__CHAMP]] + 1
                        except:
                            played[p[self.__CHAMP]] = 1

                        if p[self.__WIN]:
                            win_count = win_count + 1
                            try:
                                wins[p[self.__CHAMP]] = wins[p[self.__CHAMP]] + 1
                            except:
                                wins[p[self.__CHAMP]] = 1
                        else:
                            def_count = def_count + 1
                            try:
                                defeat[p[self.__CHAMP]] = defeat[p[self.__CHAMP]] + 1
                            except:
                                defeat[p[self.__CHAMP]] = 1
                except:
                    continue

                stats.set_wins(wins)
                stats.set_played(played)
                stats.set_defeat(defeat)
                stats.set_summoner(s[self.__SUMMONER])

                all_matches: int = len(s[self.__STATISTICS])
                if all_matches == 0:
                    stats.set_winrate(f"{s['summoner']} no jugo en los ultimos 3 dias :(")
                else:
                    stats.set_winrate(str(win_count / all_matches))

                self.__wins_by_summoners.append(stats)
