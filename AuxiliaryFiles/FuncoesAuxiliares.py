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
  elif idiomaAudio == "en-GB":
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
  responder = 1
  
  if buttonId == "pt-BR":
    mensagem_idioma = "Português Brasil"
  elif buttonId == "en-US":
    mensagem_idioma = "Inglês Americano"
  elif buttonId == "en-GB":
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
    responder = 0
  elif buttonId == "left2":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=teclado.idioma1)
    responder = 0

  if responder == 1:
    bot.edit_message_reply_markup(chatId, messageId)  
    bot.send_message(chatId, "Ok, agora irei transcrever aúdios no idioma "+mensagem_idioma)

#Funcao para mudar o idioma do tradutor
def mudarIdiomaTradutor (buttonId, chatId, messageId):
  responder = 1
  
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
    responder = 0
  elif buttonId == "left2":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=teclado.tradutor1)
    responder = 0

  if responder == 1:
    bot.edit_message_reply_markup(chatId, messageId)  
    bot.send_message(chatId, "Ok, agora irei traduzir os aúdios para o idioma "+mensagem_idioma)

def showInternalConfigToUser(userData):
  if userData == "pt-BR":
    mostrar = "Português Brasil"
  elif userData == "en-US":
    mostrar = "Inglês Americano"
  elif userData == "en-GB":
    mostrar = "Inglês Britânico"
  elif userData == "ja-JP" or userData == "japanese":
    mostrar = "Japonês"
  elif userData == "hi-IN" or userData == "hindi":
    mostrar = "Hindi"
  elif userData == "es-AR":
    mostrar = "Espanhol Argentino"
  elif userData == "es-PY":
    mostrar = "Espanhol Paraguaio"
  elif userData == "es-ES":
    mostrar = "Espanhol Espanhol"
  elif userData == "ko-KR" or userData == "korean":
    mostrar = "Coreano"
  elif userData == "zh-CN":
    mostrar = "Chinês Simplificado"
  elif userData == "zh-TW":
    mostrar = "Chinês Tradicional"
  elif userData == "fr-FR" or userData == "french":
    mostrar = "Francês"
  elif userData == "de-DE" or userData == "german":
    mostrar = "Alemão"
  elif userData == "it-IT" or userData == "italian":
    mostrar = "Italiano"
  elif userData == "el-GR" or userData == "greek":
    mostrar = "Grego"
  elif userData == "da-DK" or userData == "danish":
    mostrar = "Dinamarquês"
  elif userData == "ar-EG":
    mostrar = "Árabe Egipcio"
  elif userData == "ar-IL":
    mostrar = "Árabe Israel"
  elif userData == "af-ZA" or userData == "afrikaans":
    mostrar = "Afrikaans (Africa do Sul)"
  elif userData == "no-NO" or userData == "norwegian":
    mostrar = "Noruguês"
  elif userData == "portuguese":
    mostrar = "Português"
  elif userData == "english":
    mostrar = "Inglês"  
  elif userData == "spanish":
    mostrar = "Espanhol" 
  elif userData == "arabic":
    mostrar = "Árabe"

  return mostrar