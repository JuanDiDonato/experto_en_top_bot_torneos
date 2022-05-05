# -*- coding: utf-8 -*-

import os
import datetime
import threading
from threading import Timer
from datetime import date

import discord
from dotenv import load_dotenv
from discord.ext import commands

from league.league import Tournament
from riot_api.riot_api import RiotAPI
from database.db import Database
from embed import Embed

# Variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Base de datos
db = Database()
db.start_db()

# Gestion de mensajes
msg = Embed()

bot = commands.Bot(command_prefix='.')  # prefix del bot

todays_date = date.today() # Fecha actual
cron_time = datetime.datetime.now()
points = {}  # puntos del torneo
rounds_saved = []
players_saved = []
stadistics = []

"""
Funcion para manejar intevalos
"""
def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()


summoners = {}

@bot.event
async def on_ready(): 
    await bot.change_presence(activity=discord.Game(name=".comandos para mas info!"))
    print("Bot conectado")
    get_summoners()


def get_summoners():
    summoners_list = db.get_players()
    for s in summoners_list:
        if summoners.get(s['player_ds_id']) == None:
            summoners.update({s['player_ds_id'] : s['player_lol_name']})

"""
Obtiene el torneo y los puntos guardados en la db.

Si no obtiene datos, deja vacios los dict donde se almacenarian en el bot
"""
def sync_tournament():
    tournament = db.get_tournament()
    if len(tournament) > 0:
        print(f"Se encontron {len(tournament)} torneos activos")
        points.update(tournament[0]['points'])
        rounds_saved.extend(tournament[0]['rounds'])
        players_saved.extend(tournament[0]['players'])
        print("Rondas y puntos actualizados")
    else:
        print("No se encontraron nuevos datos")
        points.clear()
        rounds_saved.clear()
        players_saved.clear()
        stadistics.clear()

"""
Retorna informacion del servidor
"""
@bot.command()
async def info(ctx):
    await msg.show_server_info(ctx)
    
"""
Muestra los comandos del bot
"""
@bot.command()
async def comandos(ctx):
    await msg.show_commands(ctx)

"""
Guarda el nombre de invocador en la base de datos
"""
@bot.command()
async def guardar(ctx,*args):
    data = [item for item in args]
    if len(data) > 2:
        player = {'player_ds_id':data[0],"player_lol_name": ''.join(e + ' ' for e in data[1:])} # Guarda el nombre con espacios
    else:
        player = {'player_ds_id':data[0],"player_lol_name": data[1]} # Guarda el nombre sin espacios
    db.insert_one_player(player)
    await ctx.send(f"{data[0]} guardado.")

"""
Obtiene los datos de las partidas de los jugadores del torneo desde
la api de Riot games
"""
def update_history():
    print("Sincronizando historial")
    account_data = RiotAPI()
    data = account_data.get_players_data(summoners)
    stadistics.extend(data)
    print("Datos establecidos")


"""
Genera la tabla de puntos
"""
async def puntos(ctx,players):
    list_players = []
    for i in players:
        points[i] = 0
        if summoners.get(i) == None or summoners.get(i) == i:
            await ctx.send(f"🚨 {i} no esta guardado. Usa el comando '.guardar {i} + nombre en lol' 🚨")
            list_players.append({"player_ds_id":i,"player_lol_name":i})
    db.insert_many_players(list_players)
    get_summoners()

"""
Muestra en el canal de ds las estadisticas 
"""
async def display_wins(ctx,data):
    for d in data:
        await msg.show_stats(ctx,d)

"""
Ordena las estadisticas obtenidas desde la api de riot
"""
@bot.command()
async def partidas(ctx):
    wins_by_summoners = []
    if len(stadistics) > 0:
        for s in stadistics:
            if s['summoner'] != "Fecha libre":
                wins = {}
                count = 0
                for p in s['statistics']:
                    if p['win'] == True:
                        count = count + 1
                        try:
                            wins[p['champ']] = wins[p['champ']] + 1
                        except:
                            wins[p['champ']] = 1
                wins['summoner'] = s['summoner']
                wins['wins_p'] = ( count / len(s['statistics']) ) if len(s['statistics']) != 0 else 1
                wins_by_summoners.append(wins)
        await display_wins(ctx,wins_by_summoners)

"""
Crea la liga con una lista de jugadores
"""
@bot.command()
async def liga(ctx,*args):
    if len(rounds_saved) == 0 and len(players_saved) == 0:
        players = [item for item in args]  # Convierte los argumentos a una lista
        league = Tournament(players)
        rounds = league.Generate()
        rounds_saved.extend(rounds)
        players_saved.extend(players)
        await puntos(ctx,players) # Crea una tabla de puntos inicial, con cero puntos para cada participante
        created = db.insert_tournament({"rounds": rounds, "players":players, "points":points, "name":"Los Pibardos"})
        if created == False:
            points.clear()
            players_saved.clear()
            rounds_saved.clear()
            await msg.err_tournament(ctx)
            
        else:
            await ctx.send("Creando liga...")
            await msg.show_rounds(ctx,rounds)
            await tabla(ctx)
            await msg.sync_activate(ctx)
            update_history()
            await msg.sync_end(ctx)
    else:
        await msg.err_tournament(ctx)

"""
Muestra la tabla de puntuacion de cada participante del torneo
"""
@bot.command()
async def tabla(ctx):
    await msg.show_points(ctx,points)

"""
Suma un punto a un jugador
"""
@bot.command()
async def para(ctx,player):
    try:
        if points[player] >= 0:
            points[player] += 1
            await ctx.send(f"Se agrego un punto a {player}")
            await tabla(ctx)
            db.update_tournament(points)
        else:
            await ctx.send(f"{player} no esta en este torneo")
    except:
        await ctx.send(f"{player} no esta en este torneo")

"""
Elimina todos los puntos del torneo
"""
@bot.command()
async def reiniciar(ctx):
    if len(rounds_saved) > 0 and len(players_saved) > 0:
        points.clear()
        for p in players_saved:
            points[p] = 0
        db.update_tournament(points)  # Actualiza la base de datos
        await msg.rest_points_tournament(ctx)
        await tabla(ctx)
    else:
        await msg.err_not_tournament(ctx)

"""
Borra el torneo activo
"""
@bot.command()
async def borrar(ctx):
    if len(rounds_saved) > 0 and len(players_saved) > 0:
        db.delete_tournament()
        await msg.tournament_deleted(ctx)
        sync_tournament()
    else:
        await msg.err_not_tournament(ctx)

"""
Sincronizacion manual

Ejecuta las funciones para obtener el torneo activo desde la base de datos y las
estadisticas desde la api de riot
"""
@bot.command()
async def sync(ctx):
    await msg.sync_activate(ctx)
    get_tour = threading.Thread(target=sync_tournament, name='tour')
    get_hist = threading.Thread(target=update_history, name='history')
    get_summ = threading.Thread(target=get_summoners, name='summoners')
    get_tour.start()
    get_hist.start()
    get_summ.start()
    
    # sync_tournament()
    # update_history()
    # get_summoners()
    await msg.sync_end(ctx)

def sync_check():
    hour = datetime.datetime.now().hour
    if hour == 4 or hour == 5 or hour == 3:
        print("Iniciando sincronizacion programanda")
        sync_tournament()
        update_history()

setInterval(43200,sync_check)

bot.run(TOKEN)



