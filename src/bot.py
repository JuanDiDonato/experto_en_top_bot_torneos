# -*- coding: utf-8 -*-

import datetime
import os
from datetime import date
from threading import Timer

import discord
from discord.ext import commands
from dotenv import load_dotenv

from embed import Embed
from league.league import Tournament
from threadings import Threadings
from services.syncro import Syncro

# Variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Gestion de mensajes
msg = Embed()

# Gestion de subprocesos (Threading)
th = Threadings()

syncro = Syncro()

bot = commands.Bot(command_prefix=".")  # prefix del bot


def setInterval(timer, task):

    """
    Funcion para manejar intevalos
    """

    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()


@bot.event
async def on_ready():

    """
    Evento de inicio del bot
    """

    await bot.change_presence(activity=discord.Game(name=".comandos para mas info!"))
    syncro.enable_auto_sync()

    print("Bot conectado y en linea ")


@bot.command()
async def info(ctx):

    """
    Retorna informacion del servidor
    """

    await msg.show_server_info(ctx)


@bot.command()
async def comandos(ctx):

    """
    Muestra los comandos del bot
    """

    await msg.show_commands(ctx)


@bot.command()
async def fechas(ctx):

    """
    Muestra las fechas del torneo
    """

    await msg.show_rounds(ctx, th.rounds_saved)


@bot.command()
async def guardar(ctx, *args):

    """
    Guarda el nombre de invocador en la base de datos
    """

    data = [item for item in args]
    if len(data) > 2:
        player = {
            "player_ds_id": data[0],
            "player_lol_name": "".join(e + " " for e in data[1:]),
        }  # Guarda el nombre con espacios
    else:
        player = {
            "player_ds_id": data[0],
            "player_lol_name": data[1],
        }  # Guarda el nombre sin espacios
    th.db.insert_one_player(player)
    await ctx.send(f"{data[0]} guardado.")



async def puntos(ctx, players):

    """
    Genera la tabla de puntos
    """

    list_players = []
    for i in players:
        th.points[i] = 0
        if th.summoners.get(i) == None or th.summoners.get(i) == i:
            await ctx.send(
                f"🚨 {i} no esta guardado. Usa el comando '.guardar {i} + nombre en lol' 🚨"
            )
            list_players.append({"player_ds_id": i, "player_lol_name": i})
    th.db.insert_many_players(list_players)



async def display_wins(ctx, data):

    """
    Muestra en el canal de ds las estadisticas 
    """

    for d in data:
        await msg.show_stats(ctx, d)



@bot.command()
async def partidas(ctx):

    """
    Ordena las estadisticas obtenidas desde la api de riot
    """

    wins_by_summoners = []
    if len(th.stadistics) > 0:
        for s in th.stadistics:
            if s["summoner"] != "Fecha libre":
                summoner_data = {}
                wins = {}
                defeat = {}
                played = {}
                win_count = 0
                def_count = 0
                try:
                    for p in s["statistics"]:
                        try:
                            played[p["champ"]] = played[p["champ"]] + 1
                        except:
                            played[p["champ"]] = 1
                        if p["win"] == True:
                            win_count = win_count + 1
                            try:
                                wins[p["champ"]] = wins[p["champ"]] + 1
                            except:
                                wins[p["champ"]] = 1
                        else:
                            def_count = def_count + 1
                            try:
                                defeat[p["champ"]] = defeat[p["champ"]] + 1
                            except:
                                defeat[p["champ"]] = 1
                except:
                    continue
                summoner_data["wins"] = wins
                summoner_data["defeats"] = defeat
                summoner_data["played"] = played
                summoner_data["summoner"] = s["summoner"]
                if len(s["statistics"]) == 0:
                    summoner_data[
                        "wins_p"
                    ] = f"{s['summoner']} no jugo en los ultimos 3 dias :("
                else:
                    summoner_data["wins_p"] = win_count / len(s["statistics"])
                wins_by_summoners.append(summoner_data)
        await display_wins(ctx, wins_by_summoners)
    else:
        await msg.not_data(ctx)


@bot.command()
async def liga(ctx, *args):

    """
    Crea la liga con una lista de jugadores
    """

    if len(th.rounds_saved) == 0 and len(th.players_saved) == 0:
        players = [item for item in args]  # Convierte los argumentos a una lista
        league = Tournament(players)
        rounds = league.Generate()
        th.rounds_saved.extend(rounds)
        th.players_saved.extend(players)
        await puntos(
            ctx, players
        )  # Crea una tabla de puntos inicial, con cero puntos para cada participante
        created = th.db.insert_tournament(
            {
                "rounds": rounds,
                "players": players,
                "points": th.points,
                "name": "Los Pibardos",
            }
        )
        if created == False:
            th.points.clear()
            th.players_saved.clear()
            th.rounds_saved.clear()
            await msg.err_tournament(ctx)
        else:
            await ctx.send("Creando liga...")
            await msg.show_rounds(ctx, rounds)
            syncro.sync()
    else:
        await msg.err_tournament(ctx)


@bot.command()
async def tabla(ctx):

    """
    Muestra la tabla de puntuacion de cada participante del torneo
    """

    await msg.show_points(ctx, th.points)



@bot.command()
async def para(ctx, player):

    """
    Suma un punto a un jugador
    """

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



@bot.command()
async def reiniciar(ctx):

    """
    Elimina todos los puntos del torneo
    """

    if len(th.rounds_saved) > 0 and len(th.players_saved) > 0:
        th.points.clear()
        for p in th.players_saved:
            th.points[p] = 0
        th.db.update_tournament(th.points)  # Actualiza la base de datos
        await msg.rest_points_tournament(ctx)
        await tabla(ctx)
    else:
        await msg.err_not_tournament(ctx)



@bot.command()
async def borrar(ctx):

    """
    Borra el torneo activo
    """

    if len(th.rounds_saved) > 0 and len(th.players_saved) > 0:
        th.db.delete_tournament()
        await msg.tournament_deleted(ctx)
        syncro.sync()
    else:
        await msg.err_not_tournament(ctx)

if "__main__" == __name__:
    bot.run(TOKEN)
