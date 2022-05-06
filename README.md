# Bot de torneos para Discord
Bot de discord para un servidor de amigos

El bot esta pensado para crear torneos de 1 vs 1 en League of Legends.
Puede crear una liga, y administrar los puntajes de los participantes.

Mi idea es utilizar la API de Riot Games para obtener el historial de partidas y estadisticas de los participantes del torneo,
para asi automatizar los puntajes en base a las partidas jugadas, y dar mas funcionalidades al bot.

ACTUALIZACION:
El bot consume la API de Riot para obtener los datos de las partidas jugadas, y asi obtener el winrate
del jugador y con que campeones gano.
La idea de automatizar los puntajes la deje de lado, no porque no se pueda hacer, sino que por la forma de jugar el torneo, sin fechas ni horas definidas hace que sea poco practico automatizar los puntos. Simplemente hay un comando para sumar puntos manualmente.

Realice la incorporacion de Threading, para evitar que cuando el bot solicite datos a la api se blooque. De esta forma, se pueden solicitar datos a la API y al mismo tiempo usar otros comandos del bot.

El bot actualmente se hosteo en Heroku mediante una simple imagen de Docker.
