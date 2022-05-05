
import os
import time
import requests

from dotenv import load_dotenv

# Variables del entorno
load_dotenv()
KEY = os.getenv("API_RIOT_TOKEN")

summoners = {
    "<@411704033225605130>":"D1D0",
    "<@602993773940572220>": "KARTTA",
    "<@748722234931282020>":"P4rfecto",
    "<@258683657038856193>":"Nezah",
    "<@583500343426547712>":"elioelmufa",
    "<@544348597991243786>":"MaitoChoy",
    "<@712826508229476382>":"Behamoth",
    "<@515334245166743574>":"BALANCE iRELIA",
}

"""
Consume la API de Riot Games para obtener datos de las cuentas de Lol
"""
class RiotAPI:

    """
    Obtiene el puuid y el account id de cada jugador
    """
    def get_players_data(self,players):
        account_data_list = []
        for k,v in players.items():
            try:
                account_data_list.append(self.get_account_data(v))
            except:
                continue
        print(account_data_list)
        if len(account_data_list) > 0:
            for acc in account_data_list:
                history = self.get_matches(acc['puuid'])
                acc['statistics']  = self.get_match_results_by_summoner(history,acc['puuid'])
            return account_data_list
        else:
            print("Ocurrio un error al obtener los datos")

    """
    Obtiene desde la API los datos de un usuario del juego
    """
    def get_account_data(self,summoner):
        account_info = {}
        url = f"https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}"
        params = {"api_key":KEY}
        try:
            results = requests.get(url,params).json()
            account_info['summoner'] = summoner
            account_info['puuid'] = results['puuid']
            account_info['account_id'] = results['accountId']
        except:
            pass
        return account_info
    
    """
    Obtiene el historial de partidas de cada jugador
    """
    def get_matches(self,puuid):
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?startTime={int((time.time() - 259200))}"
        params = {"api_key":KEY}
        try:
            return requests.get(url,params).json()
        except:
            return

    """
    Obtiene los detalles de cada partida enviandole el id de la partida
    """
    def get_match_results_by_summoner(self,summoner_matches,puuid):
        last_statistics = []
        for m in summoner_matches:
            url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{m}"
            params = {"api_key":KEY}
            try:
                results = requests.get(url,params).json()
                if len(results['metadata']['participants']) <= 3:
                    # Validacion para saber si era una partida de torneo o no
                    pass
                else:
                    for i in results['info']['participants']:
                        if i['puuid'] == puuid:
                            last_statistics.append({"champ":i['championName'], "win":i['win']})
            except:
                continue
        return last_statistics
                
    




