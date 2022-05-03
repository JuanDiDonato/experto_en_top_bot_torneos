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

# Variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='.')
points = {}
todays_date = date.today() # Fecha actual

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
        description=f"Torneo Oficial Fecha {i + 1} "'Los Pibardos '"todos los derechos reservados ©")
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
    for i in players:
        try:
            points[summoners[i]] = 0
        except:
            points[i] = 0
"""
Crea la liga con una lista de jugadores
"""
@bot.command()
async def liga(ctx,*args):
    players = [item for item in args]  # Convierte los argumentos a una lista
    puntos(players) # Crea una tabla de puntos inicial, con cero puntos para cada participante
    league = Tournament(players)
    await ctx.send("Creando liga...")
    await message(ctx,league.Generate())
    await tabla(ctx)
    # account_data = RiotAPI()
    # account_data.get_players_data(players)

"""
Muestra la tabla de puntuacion de cada participante del torneo
"""
@bot.command()
async def tabla(ctx):
    embed = discord.Embed(title="Puntos de la Liga",
    description=f"Puntajes oficiales del Torneo Oficial "'Los Pibardos '"todos los derechos reservados ©")
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
        else:
            await ctx.send(f"{player} no esta en este torneo")
    except:
        await ctx.send(f"{player} no esta en este torneo")



bot.run(TOKEN)



