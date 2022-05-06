# -*- coding: utf-8 -*-

import datetime
from datetime import date

import discord
import humanize

class Embed():

    def __init__(self):
        self.today = date.today() # Fecha actual

    """
    No hay un torneo
    """
    async def err_not_tournament(self,ctx):
        embed = discord.Embed(title="⚠️ 🚨 Ocurrio un error",
        description="No hay un torneo activo actualmente")
        await ctx.send(embed=embed)

    """
    Ya hay un torneo
    """
    async def err_tournament(self,ctx):
        embed = discord.Embed(title="⚠️ 🚨 Ocurrio un error",
        description="Actualmente ya hay un torneo activo, y hasta que este termine o se borre no se puede crear otro. Podes ver este torneo usando '.fechas' y '.tabla'. Si no aparece nada intenta sincronizar primero con .sync")
        await ctx.send(embed=embed)

    """
    Reinicio de puntos
    """
    async def rest_points_tournament(self,ctx):
        embed = discord.Embed(title=f"Reinicio del torneo Los Pibardos © {self.today.year}",
        description="Todos los puntajes del torneo se reiniciaron a cero")
        await ctx.send(embed=embed)

    """
    Muestra los puntos
    """
    async def show_points(self,ctx,points):
        embed = discord.Embed(title="Puntos de la Liga",
        description="Puntajes del Torneo Oficial "'Los Pibardos 'f"todos los derechos reservados © {self.today.year}")
        for k,v in points.items():
            embed.add_field(name=f"Puntos de:", value=f"{k} : {v}")
        await ctx.send(embed=embed)
    
    """
    Aviso de la sync
    """
    async def sync_activate(self,ctx):
        embed = discord.Embed(title="⚠️ Sincronizacion activada",
        description="Comenzo una sincronizacion con la API de Riot Games y la base de datos para obtener registros.")
        await ctx.send(embed=embed)
    
    """
    Aviso de sync ya activa
    """
    async def sync_is_activate(self,ctx):
        embed = discord.Embed(title="⚠️ Ya hay una sincronizacion activa",
        description="Aguarde un momento mientras termina la syncro actual.")
        await ctx.send(embed=embed)

    """
    Estadisticas vacias
    """
    async def not_data(self,ctx):
        embed = discord.Embed(title="⚠️ No hay estadisticas para mostrar",
        description="Ejecute el comando de sync para obtener estadisticas")
        await ctx.send(embed=embed)

    """
    Aviso de finalizacion de la sync
    """
    async def sync_end(self,ctx):
        embed = discord.Embed(title="✅ Sincronizacion finalizada",
        description="Se sincronizaron los datos correctamente.")
        await ctx.send(embed=embed)

    """
    Muesta estadisticas
    """
    async def show_stats(self,ctx,data):
        embed = discord.Embed(title="Estadisticas",
        description=f"Estas son las estadisticas de las partidas de los ultimos 3 dias de {data['summoner']}")
        for k,v in data.items():
            if k != 'summoner' and k != 'wins_p':
                embed.add_field(name=f'Ganadas con {k}', value=f'{v}')
            elif k == 'wins_p':
                if type(v) == str:
                    embed.add_field(name=f'Porcentaje de victorias', value=f'{v}')
                else:
                    embed.add_field(name=f'Porcentaje de victorias', value=f'{int(v * 100)} %')
            else:
                pass
        await ctx.send(embed=embed)

    """
    Muestra las fechas de la liga
    """
    async def show_rounds(self,ctx,rounds):
        count = 0
        match = 1
        for i in range(0, len(rounds)):
            embed = discord.Embed(title=f"Torneo de Lol Fecha {i + 1}",
            description=f"Torneo Oficial Fecha {i + 1} "'Los Pibardos 'f"todos los derechos reservados © {self.today.year}")
            while count < len(rounds[i]):
                embed.add_field(name=f"Partida {match}:" , value=f"{rounds[i][count]} VS {rounds[i][count+1]}")
                match = match + 1
                count = count + 2
            await ctx.send(embed=embed)
            count = 0

    """
    Informacion del server
    """
    async def show_server_info(self,ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}",
        description=f"Server de Los Pibardos todos los derechos reservados © {self.today.year}",timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed.add_field(name="Creado el dia" , value=humanize.naturaltime(ctx.guild.created_at))
        embed.add_field(name="Admin", value="<@602993773940572220>")
        embed.add_field(name="Server id ", value=f"{ctx.guild.id}")
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1268868861782298626/doLOgx55.jpg")
        await ctx.send(embed=embed)
    
    """
    Comandos del server
    """
    async def show_commands(self,ctx):
        embed = discord.Embed(title="Comandos de Experto en Top:",
        description=f"Creado por <@411704033225605130>, proyecto en desarrollo. Todos los derechos reservados © {self.today.year}",timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
        embed.add_field(name=".liga + @nombre del participante + @nombre del participante + ..." , value=f"Crea una liga para un torneo 1 vs 1 de Lol")
        embed.add_field(name=".tabla", value="Muestra la tabla de puntajes de los participantes del torneo")
        embed.add_field(name=".para + @nombre del participante", value="Suma un punto a un participante del torneo")
        embed.add_field(name=".reiniciar", value="Reinicia los puntos a cero del torneo activo")
        embed.add_field(name=".borrar", value="Borra el torneo activo")
        embed.add_field(name=".info", value="Muestra informacion del servidor")
        embed.add_field(name=".sync", value="Actualiza las estadisticas manualmente")
        embed.add_field(name=".fechas", value="Muestra las fechas del torneo actual")
        embed.add_field(name=".guardar + @nombre en ds + nombre en lol", value="Guarda el nombre de lol de un jugador")
        await ctx.send(embed=embed)
    
    """
    Eliminacion del torneo
    """
    async def tournament_deleted(self,ctx):
        embed = discord.Embed(title="Torneo borrado",
        description="Se elimino el torneo activo")
        await ctx.send(embed=embed)

