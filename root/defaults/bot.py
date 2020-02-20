#################################################
####        Programado por cRytoFono		 ####
#################################################
#------------------------------------------------
# Librerías necesarias                          #
#------------------------------------------------
# python3 -m pip install telegram --upgrade
# python3 -m pip install python-telegram-bot --upgrade
#------------------------------------------------

try:

	from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, InlineQueryHandler, CallbackQueryHandler)
	from telegram import (InlineQueryResultArticle, ParseMode, InputTextMessageContent, MessageEntity, InlineKeyboardButton, InlineKeyboardMarkup)
	import telegram
	import logging
	from os import remove
	import os
	from os import scandir, getcwd, rename
	import zipfile

	# Enable logging
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
	logger = logging.getLogger(__name__)



	#----------------------------------------------
	# Función para descargarse un archivo de
	# internet
	#----------------------------------------------
	def DownloadFile(url, ruta, filename):
		try:
			# local_filename = url.split('/')[-1]
			import urllib.request
			opener = urllib.request.build_opener()
			opener.addheaders = [('User-agent', 'Mozilla/5.0')]
			urllib.request.install_opener(opener)
			urllib.request.urlretrieve(url, ruta+filename)
		except Exception as e:
			print (e)

	#----------------------------------------------
	# Función para leer los archivos de un
	# directorio
	#----------------------------------------------
	def ls(ruta = getcwd()):
		return [arch.name for arch in scandir(ruta) if arch.is_file()]

	#----------------------------------------------
	# Función para quitar los ' ' del nombre de
	# los archivos
	#----------------------------------------------

	def rename_files(ruta):
		for archivos in ls(ruta):
			if archivos.startswith("'") and archivos.endswith("'"):
				rename(archivos, archivos[1:-1])

	#----------------------------------------------
	# Función para descargar .torrent y enviarlos
	# a una carpeta
	#----------------------------------------------

	def descargar_archivos(bot, update):

		try:
			m=update.message
			#La variable ruta será donde guarde los torrents, es decir será la carpeta que al cliente hay que ponerle para que la monitorice
			ruta='/config/normales/'
			tmp='/config/zip/'

			filename=m.document.file_name
			texto=m.text
			archivo = bot.getFile(m.document.file_id)

			if filename.endswith('.zip'):
				DownloadFile(archivo.file_path, tmp, filename)
				zf = zipfile.ZipFile(tmp+filename, "r")
				for torrents in zf.namelist():
					if os.path.dirname(torrents)=='' and torrents.endswith('.torrent'):
						zf.extract(torrents, ruta)
				zf.close()
				#rename_files()
				remove(tmp+filename)
				bot.send_message(chat_id=m.chat.id, text="Se han guardado los archivos de <b>"+filename+"</b> en la carpeta", parse_mode="HTML")

			if filename.endswith('.torrent'):
				DownloadFile(archivo.file_path, ruta, filename)
				bot.send_message(chat_id=m.chat.id, text="El archivo <b>"+filename+"</b> se ha añadido guardado en la carpeta", parse_mode="HTML")
			if "magnet" in texto:
				bot.send_message(chat_id=m.chat.id, text="Esto es un magnet tronco", parse_mode="HTML")
		except Exception as e:
			print (e)

	#----------------------------------------------
	# Función para descargar los magnet
	# a una carpeta
	#----------------------------------------------
	def descargar_texto(bot, update):

		try:
			m=update.message

			ruta='/config/normales/descarga.magnet'

			texto=m.text

			if "magnet" in texto or ".torrent" in texto:
				f = open (ruta,'w')
				f.write(texto)
				f.close()
				bot.send_message(chat_id=m.chat.id, text="Torrent añadidor por URL o Magnet Correctamente", parse_mode="HTML")

		except Exception as e:
			print (e)

	def error(bot, update, error):
		logger.warn('Update "%s" caused error "%s"' % (update, error))


	def main():
	    # Create the EventHandler and pass it your bot's token.

		updater = Updater("TU TOKEN BOT")
		dp = updater.dispatcher

		dp.add_handler(MessageHandler(Filters.document, descargar_archivos))
	    # Get the dispatcher to register handlers
		dp.add_handler(MessageHandler(Filters.text, descargar_texto))



	    # log all errors
		dp.add_error_handler(error)

	    # Start the Bot
		updater.start_polling(clean=True)

	    # Run the bot until you press Ctrl-C or the process receives SIGINT,
	    # SIGTERM or SIGABRT. This should be used most of the time, since
	    # start_polling() is non-blocking and will stop the bot gracefully.
		updater.idle()


	if __name__ == '__main__':
		main()
except Exception as e:
	print (e)
