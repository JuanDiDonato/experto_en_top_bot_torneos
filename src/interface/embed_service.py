# -*- coding: utf-8 -*-

# Python modules
from abc import ABC, abstractmethod  # Abstract Base Classes

# Third modules
from discord.ext.commands import Context


class EmbedService(ABC):
    """
    Interfaz que define los metodos obligatorios para el servicio de Embed

    Es una interfaz porque los metodos no implementan codigo
    """

    @abstractmethod
    def create_embed(self, title: str, description: str):
        pass

    @abstractmethod
    async def send_embed(self, ctx: Context):
        pass

    @abstractmethod
    def with_field(self, name: str, value: str):
        pass
