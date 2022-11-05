# -*- coding: utf-8 -*-

# python modules
from datetime import date

# third modules
import discord
import humanize

# app modules
from services.embed_builder import EmbedBuilder
from services.embed_statistics_builder import EmbedStatisticsBuilder
from models.Statistics import Statistics


class Embed:
    __embed_service: EmbedBuilder = EmbedBuilder()  # Constructor de embeds
    __embed_statistics_service: EmbedStatisticsBuilder = EmbedStatisticsBuilder()
    __today: date = date.today()  # Fecha actual
    __WINS: str = "wins"
    __DEFEAT: str = "defeats"
    __WINRATE: str = "wins_p"
    __MATCHES_PLAYED: str = "played"
    __THUMBNAIL: str = "https://pbs.twimg.com/profile_images/1268868861782298626/doLOgx55.jpg"
    __ADMIN_ID: str = "<@602993773940572220>"

    # Titulos
    __ERROR: str = "Ocurrio un error"
    __RESTART_TOURNAMENT: str = f"Reinicio del torneo Los Pibardos © {__today.year}"

    # Descripciones
    __POINTS: str = f"Puntajes del Torneo Oficial Los Pibardos todos los derechos reservados © {__today.year}"
    __SERVER_INFO: str = f"Server de Los Pibardos todos los derechos reservados © {__today.year}"

    async def err_not_tournament(self, ctx):

        """
        No hay un torneo activo
        """

        message: str = "No hay un torneo activo"
        await self.__embed_service.create_embed(self.__ERROR, message).send_embed(ctx=ctx)

    async def err_tournament(self, ctx):

        """
        Ya hay un torneo activo
        """

        message: str = "Actualmente ya hay un torneo activo, y hasta que este termine o se borre no se puede crear otro."
        await self.__embed_service.create_embed(self.__ERROR, message).send_embed(ctx=ctx)

    async def rest_points_tournament(self, ctx):

        """
        Reinicio de los puntos del torneo
        """

        message: str = "Todos los puntajes del torneo se reiniciaron a cero"
        await self.__embed_service.create_embed(self.__RESTART_TOURNAMENT, message).send_embed(ctx=ctx)

    async def show_points(self, ctx, points):

        """
        Muestra los puntos del torneo
        """

        title: str = "Puntos de la liga"
        embed = self.__embed_service.create_embed(title, self.__POINTS)

        for k, v in points.items():
            embed.with_field(name=f"Puntos de:", value=f"{k} : {v}")

        await embed.send_embed(ctx=ctx)

    async def not_data(self, ctx):

        """
        Estadisticas vacias
        """

        message: str = "Los datos se obtienen automaticamente, aguarde un momento y vuelva a intentar"
        await self.__embed_service.create_embed(self.__ERROR, message).send_embed(ctx=ctx)

    async def show_stats(self, ctx, data: Statistics):

        """
        Muesta las estadisticas
        """

        title: str = "Estadisticas"
        description: str = f"Estas son las estadisticas de las partidas de los ultimos 3 dias de {data.get_summoner}"
        await self.__embed_statistics_service.with_field(title, description).with_statistics(data).send_embed(ctx=ctx)

    async def show_rounds(self, ctx, rounds):

        """
        Muestra las fechas de la liga
        """

        count = 0
        match = 1

        for i in range(0, len(rounds)):

            title: str = f"Torneo de Lol Fecha {i + 1}"
            description: str = f"Torneo Oficial Fecha {i + 1} Los Pibardos todos los derechos reservados © {self.__today.year}"
            embed: EmbedBuilder = self.__embed_service.create_embed(title, description)

            while count < len(rounds[i]):
                embed.with_field(
                    name=f"Partida {match}:",
                    value=f"{rounds[i][count]} VS {rounds[i][count + 1]}",
                )
                match = match + 1
                count = count + 2

            await embed.send_embed(ctx=ctx)
            count = 0

    async def show_server_info(self, ctx):

        """
        Muestra la nformacion del server
        """

        title: str = f"{ctx.guild.name}"
        description: str = self.__SERVER_INFO

        embed: EmbedBuilder = self.__embed_service.create_embed(title, description)

        embed.with_field(name="Creado el dia", value=humanize.naturaltime(ctx.guild.created_at))
        embed.with_field(name="Admin", value=self.__ADMIN_ID)
        embed.with_field(name="Server id ", value=f"{ctx.guild.id}")
        embed.with_thumbnail(url=self.__THUMBNAIL)

        await embed.send_embed(ctx=ctx)

    async def show_commands(self, ctx):

        """
        Comandos del server
        """

        embed = discord.Embed(
            title="Comandos de Experto en Top:",
            description=f"Creado por <@411704033225605130>, proyecto en desarrollo. Todos los derechos reservados © {self.today.year}",
        )
        embed.add_field(
            name=".liga + @nombre del participante + @nombre del participante + ...",
            value=f"Crea una liga para un torneo 1 vs 1 de Lol",
        )
        embed.add_field(
            name=".tabla",
            value="Muestra la tabla de puntajes de los participantes del torneo",
        )
        embed.add_field(
            name=".para + @nombre del participante",
            value="Suma un punto a un participante del torneo",
        )
        embed.add_field(
            name=".reiniciar", value="Reinicia los puntos a cero del torneo activo"
        )
        embed.add_field(name=".borrar", value="Borra el torneo activo")
        embed.add_field(name=".info", value="Muestra informacion del servidor")
        embed.add_field(name=".fechas", value="Muestra las fechas del torneo actual")
        embed.add_field(
            name=".guardar + @nombre en ds + nombre en lol",
            value="Guarda el nombre de lol de un jugador",
        )
        await ctx.send(embed=embed)

    """
    Eliminacion del torneo
    """

    async def tournament_deleted(self, ctx):
        embed = discord.Embed(
            title="Torneo borrado", description="Se elimino el torneo activo"
        )
        await ctx.send(embed=embed)
