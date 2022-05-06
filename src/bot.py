# -*- coding: utf-8 -*-

import os
import datetime
import threading
from threading import Timer
from datetime import date
from unicodedata import name

import discord
from dotenv import load_dotenv
from discord.ext import commands

from league.league import Tournament
from threadings import Threadings
from embed import Embed

# Variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Gestion de mensajes
msg = Embed()

# Threading
th = Threadings()

bot = commands.Bot(command_prefix='.')  # prefix del bot

cron_time = datetime.datetime.now() # fecha actual

"""
Funcion para manejar intevalos
"""
def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()
    
"""
Evento de inicio del bot
"""
@bot.event
async def on_ready(): 
    await bot.change_presence(activity=discord.Game(name=".comandos para mas info!"))
    print("Bot conectado")
    get_summoners()
    sync_tournament()
    update_history()
    

"""
Threading que ejecuta la busqueda de usuarios
"""
def get_summoners():
    get_summ = threading.Thread(target=th.tr_get_summoners, name='get_summoners')
    if not get_summ.is_alive():
        get_summ.start()

"""
Threading que ejecuta la busqueda de torneos
"""
def sync_tournament():
    get_tour = threading.Thread(target=th.tr_sync_tournament, name='sync_tournament')
    if not get_tour.is_alive():
        get_tour.start()

"""
Threading que ejecuta la syncro con la api de riot
"""
def update_history():
    get_hist = threading.Thread(target=th.tr_update_history, name='update_history')
    if not get_hist.is_alive():
        get_hist.start()

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
Muestra las fechas del torneo
"""
@bot.command()
async def fechas(ctx):
    await msg.show_rounds(ctx,th.rounds_saved)

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
    th.db.insert_one_player(player)
    await ctx.send(f"{data[0]} guardado.")

"""
Genera la tabla de puntos
"""
async def puntos(ctx,players):
    list_players = []
    for i in players:
        th.points[i] = 0
        if th.summoners.get(i) == None or th.summoners.get(i) == i:
            await ctx.send(f"🚨 {i} no esta guardado. Usa el comando '.guardar {i} + nombre en lol' 🚨")
            list_players.append({"player_ds_id":i,"player_lol_name":i})
    th.db.insert_many_players(list_players)

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
    if len(th.stadistics) > 0:
        for s in th.stadistics:
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
                if len(s['statistics']) == 0:
                    wins['wins_p'] = f"{s['summoner']} no jugo en los ultimos 3 dias :("
                else:
                    wins['wins_p'] = count / len(s['statistics'])
                wins_by_summoners.append(wins)
        await display_wins(ctx,wins_by_summoners)
    else: 
        await msg.not_data(ctx)

"""
Crea la liga con una lista de jugadores
"""
@bot.command()
async def liga(ctx,*args):
    if len(th.rounds_saved) == 0 and len(th.players_saved) == 0:
        players = [item for item in args]  # Convierte los argumentos a una lista
        league = Tournament(players)
        rounds = league.Generate()
        th.rounds_saved.extend(rounds)
        th.players_saved.extend(players)
        await puntos(ctx,players) # Crea una tabla de puntos inicial, con cero puntos para cada participante
        created = th.db.insert_tournament({"rounds": rounds, "players":players, "points":th.points, "name":"Los Pibardos"})
        if created == False:
            th.points.clear()
            th.players_saved.clear()
            th.rounds_saved.clear()
            await msg.err_tournament(ctx)
        else:
            await ctx.send("Creando liga...")
            await msg.show_rounds(ctx,rounds)
            # await tabla(ctx)
            await sync(ctx)
    else:
        await msg.err_tournament(ctx)

"""
Muestra la tabla de puntuacion de cada participante del torneo
"""
@bot.command()
async def tabla(ctx):
    await msg.show_points(ctx,th.points)

"""
Suma un punto a un jugador
"""
@bot.command()
async def para(ctx,player):
    try:
        if th.points[player] >= 0:
            th.points[player] += 1
            await ctx.send(f"Se agrego un punto a {player}")
            await tabla(ctx)
            th.db.update_tournament(th.points)
        else:
            await ctx.send(f"{player} no esta en este torneo")
    except:
        await ctx.send(f"{player} no esta en este torneo")

"""
Elimina todos los puntos del torneo
"""
@bot.command()
async def reiniciar(ctx):
    if len(th.rounds_saved) > 0 and len(th.players_saved) > 0:
        th.points.clear()
        for p in th.players_saved:
            th.points[p] = 0
        th.db.update_tournament(th.points)  # Actualiza la base de datos
        await msg.rest_points_tournament(ctx)
        await tabla(ctx)
    else:
        await msg.err_not_tournament(ctx)

"""
Borra el torneo activo
"""
@bot.command()
async def borrar(ctx):
    if len(th.rounds_saved) > 0 and len(th.players_saved) > 0:
        th.db.delete_tournament()
        await msg.tournament_deleted(ctx)
        sync_tournament()
    else:
        await msg.err_not_tournament(ctx)

"""
Sincronizacion manual

Ejecuta las funciones para obtener el torneo activo desde la base de datos y las
estadisticas desde la api de riot

Solo hace la syncro si no esta hay activa ninguna otra
"""
@bot.command()
async def sync(ctx):
    fuctions_thr = {
        "get_summoners" : get_summoners,
        "sync_tournament" : sync_tournament,
        "update_history" : update_history
    }
    sync_active = {
        "get_summoners" : False,
        "sync_tournament" : False,
        "update_history" : False
    }
    await msg.sync_activate(ctx)
    for thr in threading.enumerate():
        if thr.name == "get_summoner" or thr.name == "sync_tournament" or thr.name == "update_history" :
            sync_active[thr.name] = True

    for k,v in sync_active.items():
        if v == False:
            fuctions_thr[k]()
            
"""
syncro programada
"""
def sync_check():
    hour = datetime.datetime.now().hour
    if hour == 4 or hour == 5 or hour == 3:
        fuctions_thr = {
            "get_summoners" : get_summoners,
            "sync_tournament" : sync_tournament,
            "update_history" : update_history
        }
        sync_active = {
            "get_summoners" : False,
            "sync_tournament" : False,
            "update_history" : False
        }
        for thr in threading.enumerate():
            if thr.name == "get_summoner" or thr.name == "sync_tournament" or thr.name == "update_history" :
                sync_active[thr.name] = True

        for k,v in sync_active.items():
            if v == False:
                fuctions_thr[k]()


setInterval(43200,sync_check)

bot.run(TOKEN)





