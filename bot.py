# -*- coding: utf-8 -*-

import os
import time
import datetime
from datetime import date

import discord
import humanize
from dotenv import load_dotenv
from discord.ext import commands

from src.league import Tournament
from src.riot_api import RiotAPI
from src.database.db import Database

# Variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Base de datos
db = Database()
db.start_db()

bot = commands.Bot(command_prefix='.')
todays_date = date.today() # Fecha actual
points = {}  # puntos del torneo
rounds_saved = []
players_saved = []


"""
Ids de Discord con sus equivalentes en nombres de lol
"""
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

@bot.event
async def on_ready(): 
    await bot.change_presence(activity=discord.Game(name=".comandos para mas info!"))
    print("Bot conectado")
    sync_tournament()


def sync_tournament():
    tournament = db.get_tournament()
    print(tournament)
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

"""
Retorna informacion del servidor
"""
@bot.command()
async def info(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}",
    description=f"Server de Los Pibardos todos los derechos reservados © {todays_date.year}",timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    embed.add_field(name="Creado el dia" , value=humanize.naturaltime(ctx.guild.created_at))
    embed.add_field(name="Admin", value="<@602993773940572220>")
    embed.add_field(name="Server id ", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1268868861782298626/doLOgx55.jpg")
    await ctx.send(embed=embed)

"""
Muestra los comandos del bot
"""
@bot.command()
async def comandos(ctx):
    embed = discord.Embed(title="Comandos de Experto en Top:",
    description=f"Creado por <@411704033225605130>, proyecto en desarrollo. Todos los derechos reservados © {todays_date.year}",timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
    embed.add_field(name=".liga + @nombre del participante + @nombre del participante + ..." , value=f"Crea una liga para un torneo 1 vs 1 de Lol")
    embed.add_field(name=".tabla", value="Muestra la tabla de puntajes de los participantes del torneo")
    embed.add_field(name=".para + @nombre del participante", value="Suma un punto a un participante del torneo")
    embed.add_field(name=".reiniciar", value="Reinicia los puntos a cero del torneo activo")
    embed.add_field(name=".borrar", value="Borra el torneo activo")
    embed.add_field(name=".info", value="Muestra informacion del servidor")
    await ctx.send(embed=embed)

"""
Genera los mensajes para cada fecha de la liga
"""
async def message(ctx,rounds):
    count = 0
    match = 1
    for i in range(0, len(rounds)):
        embed = discord.Embed(title=f"Torneo de Lol Fecha {i + 1}",
        description=f"Torneo Oficial Fecha {i + 1} "'Los Pibardos 'f"todos los derechos reservados © {todays_date.year}")
        while count < len(rounds[i]):
            embed.add_field(name=f"Partida {match}:" , value=f"{rounds[i][count]} VS {rounds[i][count+1]}")
            match = match + 1
            count = count + 2
        await ctx.send(embed=embed)
        count = 0

"""
Genera la tabla de puntos
"""
def puntos(players):
    list_players = []

    for i in players:
        try:
            points[summoners[i]] = 0
            list_players.append({"player_ds_id":i,"player_name":summoners[i]})
        except:
            points[i] = 0
            list_players.append({"player_ds_id":i,"player_name":"undefined"})

    db.insert_many_players(list_players)

async def error(ctx):
    embed = discord.Embed(title="⚠️ 🚨 Ocurrio un error",
    description="Actualmente ya hay un torneo activo, y hasta que este termine o se borre no se puede crear otro. A continuacion te muestro el torneo activo! ↓↓")
    await ctx.send(embed=embed)
    await message(ctx,rounds_saved)

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
        puntos(players) # Crea una tabla de puntos inicial, con cero puntos para cada participante
        created = db.insert_tournament({"rounds": rounds, "players":players, "points":points, "name":"Los Pibardos"})
        if created == False:
            await error(ctx)
        else:
            await ctx.send("Creando liga...")
            await message(ctx,rounds)
            await tabla(ctx)
    else:
        await error(ctx)
    # account_data = RiotAPI()
    # account_data.get_players_data(players)

"""
Muestra la tabla de puntuacion de cada participante del torneo
"""
@bot.command()
async def tabla(ctx):
    embed = discord.Embed(title="Puntos de la Liga",
    description="Puntajes del Torneo Oficial "'Los Pibardos 'f"todos los derechos reservados © {todays_date.year}")
    for k,v in points.items():
        embed.add_field(name=f"Puntos de {k}", value=f"{v}")
    await ctx.send(embed=embed)


"""
Suma un punto a un jugador
"""
@bot.command()
async def para(ctx,player):
    try:
        if points[summoners[player]] >= 0:
            points[summoners[player]] += 1
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
            try:
                points[summoners[p]] = 0
            except:
                points[p] = 0
        db.update_tournament(points)  # Actualiza la base de datos
        embed = discord.Embed(title=f"Reinicio del torneo Los Pibardos © {todays_date.year}",
        description="Todos los puntajes del torneo se reiniciaron a cero")
        await ctx.send(embed=embed)
        await tabla(ctx)
    else:
        embed = discord.Embed(title="⚠️ 🚨 Ocurrio un error",
        description="No hay un torneo activo para reiniciar los puntajes")
        await ctx.send(embed=embed)

"""
Borra el torneo activo
"""
@bot.command()
async def borrar(ctx):
    if len(rounds_saved) > 0 and len(players_saved) > 0:
        db.delete_tournament()
        embed = discord.Embed(title="Torneo borrado",
        description="Se elimino el torneo activo")
        await ctx.send(embed=embed)
        sync_tournament()
    else:
        embed = discord.Embed(title="⚠️ 🚨 Ocurrio un error",
        description="No hay un torneo activo para borrar")
        await ctx.send(embed=embed)





bot.run(TOKEN)



