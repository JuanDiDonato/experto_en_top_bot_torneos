# -*- coding: utf-8 -*-

# Third modules
from discord import Embed
from discord.ext.commands import Context

# App modules
from ..interface.embed_service import EmbedService


class EmbedBuilder(EmbedService):
    """
    Esta clase implementa una interfaz, o otra clase con metodos abstrabtos,
    y se encarga de crear y lanzar embeds simples.
    """

    # Constructor
    def __init__(self) -> None:
        super().__init__()
        self.__embed = None

    def create_embed(self, title: str, description: str):
        """
        Crea una instancia de embed basica y la guarda
        """

        self.__embed = Embed(title=title, description=description)
        return self

    def with_field(self, name: str, value: str):

        """
        Agrega campos personalizados al embed
        """

        self.__embed.add_field(name=name, value=value)
        return self

    def with_thumbnail(self, url: str):
        """
        Agrega una miniatura al mensaje
        """

        self.__embed.set_thumbnail(url=url)
        return self

    async def send_embed(self, ctx: Context):
        """
        Lanza el embed al canal de discord
        """

        await ctx.send(self.__embed)
