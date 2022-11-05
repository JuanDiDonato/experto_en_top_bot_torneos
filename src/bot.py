# -*- coding: utf-8 -*-

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from embed import Embed
from services.embed_builder import EmbedService
from league.league import Tournament
from threading import Threading
from services.syncro_service import Syncro
from services.threading_services.statistics_service import StatisticsService

# Variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Gestion de mensajes
msg = Embed()
embed_service = EmbedService()

# Gestion de subprocesos (Threading)
th = Threading()

# Gestion de la sincronizacion
syncro = Syncro()

# Servicios
statistics = StatisticsService()

bot = commands.Bot(command_prefix=".")  # prefix del bot


@bot.event
async def on_ready():

    """
    Evento que se ejecuta al inicio del bot
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


async def points(ctx, players):

    """
    Genera la tabla de puntos
    """

    list_players = []
    for i in players:
        th.points[i] = 0
        if th.summoners.get(i) is None or th.summoners.get(i) == i:
            await ctx.send(
                f"🚨 {i} no esta guardado. Usa el comando '.guardar {i} + nombre en lol' 🚨"
            )
            list_players.append({"player_ds_id": i, "player_lol_name": i})
    th.db.insert_many_players(list_players)


@bot.command()
async def estadisticas(ctx):
    """
    Ordena las estadisticas obtenidas desde la api de riot
    """

    wins_by_summoners = statistics.wins_by_summoners

    if len(wins_by_summoners) > 0:
        for d in wins_by_summoners:
            await msg.show_stats(ctx, d)
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
        await points(
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
        if not created:
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
