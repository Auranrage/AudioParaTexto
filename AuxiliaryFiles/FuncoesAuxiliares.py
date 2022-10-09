import os
import telebot
import AuxiliaryFiles.Teclado as teclado

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

#Funcao auxiliar para definir o idioma do texto antes da traducao para o google translate
def defineIdiomaTextoFonte(idiomaAudio):
  idiomaTextoFonte = 'portuguese'
  
  if idiomaAudio == 'pt-BR':
      idiomaTextoFonte = 'portuguese'
  elif idiomaAudio == "en-US":
    idiomaTextoFonte = 'english'
  elif idiomaAudio == "en-BR":
    idiomaTextoFonte = 'english'
  elif idiomaAudio == "ja-JP":
    idiomaTextoFonte = 'japanese'
  elif idiomaAudio == "hi-IN":
    idiomaTextoFonte = 'hindi'
  elif idiomaAudio == "es-AR":
    idiomaTextoFonte = 'spanish'
  elif idiomaAudio == "es-PY":
    idiomaTextoFonte = 'spanish'
  elif idiomaAudio == "es-ES":
    idiomaTextoFonte = 'spanish'
  elif idiomaAudio == "ko-KR":
    idiomaTextoFonte = 'korean'
  elif idiomaAudio == "zh-CN":
    idiomaTextoFonte = 'zh-CN'
  elif idiomaAudio == "zh-TW":
    idiomaTextoFonte = 'zh-TW'
  elif idiomaAudio == "fr-FR":
    idiomaTextoFonte = 'french'
  elif idiomaAudio == "de-DE":
    idiomaTextoFonte = 'german'
  elif idiomaAudio == "it-IT":
    idiomaTextoFonte = 'italian'
  elif idiomaAudio == "el-GR":
    idiomaTextoFonte = 'greek'
  elif idiomaAudio == "da-DK":
    idiomaTextoFonte = 'danish'
  elif idiomaAudio == "ar-EG":
    idiomaTextoFonte = 'arabic'
  elif idiomaAudio == "ar-IL":
    idiomaTextoFonte = 'arabic'
  elif idiomaAudio == "af-ZA":
    idiomaTextoFonte = 'afrikaans'
  elif idiomaAudio == "no-NO":
    idiomaTextoFonte = 'norwegian'
  else:
    idiomaTextoFonte = 'auto'

  return idiomaTextoFonte

#Funcao para mudar o idioma de transcrição dos audios
def mudarIdiomaAudio (buttonId, chatId, messageId):
  if buttonId == "pt-BR":
    mensagem_idioma = "Português Brasil"
  elif buttonId == "en-US":
    mensagem_idioma = "Inglês Americano"
  elif buttonId == "en-BR":
    mensagem_idioma = "Inglês Britânico"
  elif buttonId == "ja-JP":
    mensagem_idioma = "Japonês"
  elif buttonId == "hi-IN":
    mensagem_idioma = "Hindi"
  elif buttonId == "es-AR":
    mensagem_idioma = "Espanhol Argentino"
  elif buttonId == "es-PY":
    mensagem_idioma = "Espanhol Paraguaio"
  elif buttonId == "es-ES":
    mensagem_idioma = "Espanhol Espanhol"
  elif buttonId == "ko-KR":
    mensagem_idioma = "Coreano"
  elif buttonId == "zh-CN":
    mensagem_idioma = "Chinês"
  elif buttonId == "zh-TW":
    mensagem_idioma = "Chinês Taiwan"
  elif buttonId == "fr-FR":
    mensagem_idioma = "Francês"
  elif buttonId == "de-DE":
    mensagem_idioma = "Alemão"
  elif buttonId == "it-IT":
    mensagem_idioma = "Italiano"
  elif buttonId == "el-GR":
    mensagem_idioma = "Grego"
  elif buttonId == "da-DK":
    mensagem_idioma = "Dinamarquês"
  elif buttonId == "ar-EG":
    mensagem_idioma = "Árabe Egipcio"
  elif buttonId == "ar-IL":
    mensagem_idioma = "Árabe Israel"
  elif buttonId == "af-ZA":
    mensagem_idioma = "Afrikaans (Africa do Sul)"
  elif buttonId == "no-NO":
    mensagem_idioma = "Noruguês"
  elif buttonId == "right1":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=teclado.idioma2)
  elif buttonId == "left2":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=teclado.idioma1)

  bot.edit_message_reply_markup(chatId, messageId)  
  bot.send_message(chatId, "Ok, agora irei transcrever aúdios no idioma "+mensagem_idioma)

#Funcao para mudar o idioma do tradutor
def mudarIdiomaTradutor (buttonId, chatId, messageId):
  if buttonId == "portuguese":
    mensagem_idioma = "Português"
  elif buttonId == "english":
    mensagem_idioma = "Inglês"  
  elif buttonId == "japanese":
    mensagem_idioma = "Japonês"
  elif buttonId == "hindi":
    mensagem_idioma = "Hindi"
  elif buttonId == "spanish":
    mensagem_idioma = "Espanhol" 
  elif buttonId == "korean":
    mensagem_idioma = "Coreano"
  elif buttonId == "zh-CN":
    mensagem_idioma = "Chinês Simplificado"
  elif buttonId == "zh-TW":
    mensagem_idioma = "Chinês Tradicional"
  elif buttonId == "french":
    mensagem_idioma = "Francês"
  elif buttonId == "german":
    mensagem_idioma = "Alemão"
  elif buttonId == "italian":
    mensagem_idioma = "Italiano"
  elif buttonId == "greek":
    mensagem_idioma = "Grego"
  elif buttonId == "danish":
    mensagem_idioma = "Dinamarquês"
  elif buttonId == "arabic":
    mensagem_idioma = "Árabe"
  elif buttonId == "afrikaans":
    mensagem_idioma = "Afrikaans (Africa do Sul)"
  elif buttonId == "norwegian":
    mensagem_idioma = "Noruguês"
  elif buttonId == "right1":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=teclado.tradutor2)
  elif buttonId == "left2":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=teclado.tradutor1)

  bot.edit_message_reply_markup(chatId, messageId)  
  bot.send_message(chatId, "Ok, agora irei traduzir os aúdios para o idioma "+mensagem_idioma)