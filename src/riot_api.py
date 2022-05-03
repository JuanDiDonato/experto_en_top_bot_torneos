
import os
import requests

from dotenv import load_dotenv

# Variables del entorno
load_dotenv()
KEY = os.getenv("API_RIOT_TOKEN")

summoners = {
    "<@411704033225605130>":"D1D0",
    "<@602993773940572220>": "KARTTA",
    "<@748722234931282020>":"P4rfecto",
    "<@258683657038856193>":"Neza",
    "<@583500343426547712>":"elioelmufa",
    "<@544348597991243786>":"MaitoChoy",
    "<@712826508229476382>":"Behamoth",
    "<@515334245166743574>":"BALANCE iRELIA",
}

"""
Consume la API de Riot Games para obtener datos de las cuentas de Lol
"""
class RiotAPI:

    def get_players_data(self,players):
        account_data_list = []
        for player in players:
            try:
                account_data_list.append(self.get_account_data(summoners[player]))
            except:
                continue
        return account_data_list

    def get_account_data(self,summoner):
        account_info = {}
        url = f"https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner}"
        params = {"api_key":KEY}
        try:
            results = requests.get(url,params).json()
            print(self.get_matches(results['puuid']))
            account_info[summoner] = (results['puuid'],results['accountId'])
        except:
            pass
        return account_info
    
    def get_matches(self,puuid):
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {"api_key":KEY}
        try:
            return requests.get(url,params).json()
        except:
            return




