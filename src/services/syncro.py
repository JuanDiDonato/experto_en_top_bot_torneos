# -*- coding: utf-8 -*-

# Python modules
import threading
import time

# App modules
from ..threadings import Threadings 

class Syncro:

    """
    Esta clase se encarga de manejar la sincronizacion de los datos desde sus diferentes origenes
    """

    # Atributos privados
    __threadings_handler : Threadings = Threadings() 
    __SUMMONERS_THREADING_NAME : str = "get_summoners"
    __TOURNAMENT_THREADING_NAME : str = "sync_tournament"
    __HISTORY_THREADING_NAME : str = "update_history"

    def sync(self):

        """
        Ejecuta las funciones para obtener el torneo activo desde la base de datos y las
        estadisticas desde la api de riot
        Solo hace la sincronizacion si no esta activa
        """

        fuctions_thr = {
            "get_summoners": self.__get_summoners,
            "sync_tournament": self.__sync_tournament,
            "update_history": self.__update_history,
        }

        sync_active = {
            "get_summoners": False,
            "sync_tournament": False,
            "update_history": False,
        }

        for thr in threading.enumerate():
            if (
                thr.name == "get_summoner"
                or thr.name == "sync_tournament"
                or thr.name == "update_history"
            ):
                sync_active[thr.name] = True

        for k, v in sync_active.items():
            if v == False:
                fuctions_thr[k]()
    
    def enable_auto_sync(self):

        """
        Activa y ejecuta la sincronizacion automatica de datos
        """

        auto_sync_thr = threading.Thread(target=self.__auto_sync, name="auto_sync")
        auto_sync_thr.start()


    def __get_summoners(self):

        """
        Threading que ejecuta la busqueda de usuarios
        """

        get_summ = threading.Thread(target=self.__threadings_handler.tr_get_summoners, name=self.__SUMMONERS_THREADING_NAME)
        if not get_summ.is_alive():
            get_summ.start()


    def __sync_tournament(self):

        """
        Threading que ejecuta la busqueda de torneos
        """

        get_tour = threading.Thread(target=self.__threadings_handler.tr_sync_tournament, name=self.__TOURNAMENT_THREADING_NAME)
        if not get_tour.is_alive():
            get_tour.start()


    def __update_history(self):

        """
        Threading que ejecuta la syncro con la api de riot
        """

        get_hist = threading.Thread(target=self.__threadings_handler.tr_update_history, name=self.__HISTORY_THREADING_NAME)
        if not get_hist.is_alive():
            get_hist.start()

    def __auto_sync(self):

        """
        Ejecuta la sincronizacion automatica
        """

        while True:
            self.sync()
            time.sleep(600)  # diez minutos
