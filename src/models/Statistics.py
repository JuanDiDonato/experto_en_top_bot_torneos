# -*- coding: utf-8 -*-

class Statistics:

    def __init__(self) -> None:
        self.__wins: object = None
        self.__defeat: object = None
        self.__played: object = None
        self.__summoner: str = ""
        self.__win_rate: str = ""

    @property
    def get_wins(self) -> object:
        return self.__wins

    @get_wins.setter
    def set_wins(self, wins: object):
        self.__wins = wins

    @property
    def get_defeat(self) -> object:
        return self.__defeat

    @get_defeat.setter
    def set_defeat(self, defeat: object):
        self.__defeat = defeat

    @property
    def get_played(self) -> object:
        return self.__played

    @get_played.setter
    def set_played(self, played: object):
        self.__played = played

    @property
    def get_summoner(self) -> str:
        return self.__summoner

    @get_summoner.setter
    def set_summoner(self, summoner: str):
        self.__summoner = summoner

    @property
    def get_win_rate(self):
        return self.__win_rate

    @get_winrate.setter
    def set_win_rate(self, win_rate: str):
        self.__win_rate = win_rate
