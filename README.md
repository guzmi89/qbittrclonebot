# qbittrclonebot 🚀

[![Docker Pulls](https://img.shields.io/docker/pulls/rclone/rclone)](https://hub.docker.com/r/guzmi/qbittrclonebot)

Este contenedor de docker contiene el cliente qBittorrent, herramienta Rclone y un BOT extra en Python para telegram al cuál enviar los torrents y automáticamente se añadan al cliente qbittorrent, con la finalidad de automatizar la subida de nuestras descargas a los principales servidores cloud como gdrive etc.

### Pre-requisitos 📋
Únicamente necesitaremos tener docker instalado en nuestro sistema operativo.

## Despliegue 📦
La forma más recomendades para lanzar este contenedor es la siguiente:

```
docker run \
  --name=qbittorrent \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/London \
  -e UMASK_SET=022 \
  -e WEBUI_PORT=8085 \
  -p 6881:6881 \
  -p 6881:6881/udp \
  -p 8085:8085 \
  -v /tupath/config:/config \
  -v /tupath/downloads:/downloads \
  --restart unless-stopped \
-it guzmi/qbittrclonebot /bin/bash
```
## +info 📖
La versión que contiene del cliente qBittorrent es la v4.2.1
Para que el bot telgram pueda trabajar y debemos editar el archivo bot.py que se encuentra en la carpeta /config y añadir en lugar indicado el TOKEN ID de nuestro bot telegram, posteriormente a qBittorrent en configuración debemos configurarle como carpeta monitorizada /config/normales/

Es necesario que las carpetas a las cuáles apuntan los volúmenes tengan permisos de escritura y lectura de lo contrario rclone no podrá leer y escribir su fichero de configuración.

