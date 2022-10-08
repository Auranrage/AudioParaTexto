import os
import telebot
import speech_recognition
import subprocess
from deep_translator import GoogleTranslator


#Variaveis
API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

Google_Speech_API_KEY = os.environ['Google_Speech_API_Key']
idiomaAudio='pt-BR'
idiomaTradutor='portuguese'

tradutorLigado = False

#Botoes para /idiomas
button_ptBR = telebot.types.InlineKeyboardButton('Português Brasil', callback_data='pt-BR')
button_enUS = telebot.types.InlineKeyboardButton('Inglês Americano', callback_data='en-US')
button_enGB = telebot.types.InlineKeyboardButton('Inglês Britânico', callback_data='en-GB')
button_jaJP = telebot.types.InlineKeyboardButton('Japonês', callback_data='ja-JP')
button_hiIN = telebot.types.InlineKeyboardButton('Hindi (India)', callback_data='hi-IN')
button_esAR = telebot.types.InlineKeyboardButton('Espanhol Argentino', callback_data='es-AR')
button_esPY = telebot.types.InlineKeyboardButton('Espanhol Paraguaio', callback_data='es-PY')
button_esES = telebot.types.InlineKeyboardButton('Espanhol Espanhol', callback_data='es-ES')
button_koKR = telebot.types.InlineKeyboardButton('Coreano', callback_data='ko-KR')
button_zhCN = telebot.types.InlineKeyboardButton('Chinês Mandarin', callback_data='zh-CN')
button_zhTW = telebot.types.InlineKeyboardButton('Chinês Taiwan', callback_data='zh-TW')
button_frFR = telebot.types.InlineKeyboardButton('Francês', callback_data='fr-FR')
button_deDE = telebot.types.InlineKeyboardButton('Alemão', callback_data='de-DE')
button_itIT = telebot.types.InlineKeyboardButton('Italiano', callback_data='it-IT')
button_elGR = telebot.types.InlineKeyboardButton('Grego', callback_data='el-GR')
button_daDK = telebot.types.InlineKeyboardButton('Dinamarquês', callback_data='da-DK')
button_arEG = telebot.types.InlineKeyboardButton('Árabe Egipcio', callback_data='ar-EG')
button_arIL = telebot.types.InlineKeyboardButton('Árabe Israel', callback_data='ar-IL')
button_afZA = telebot.types.InlineKeyboardButton('Afrikaans (África do Sul)', callback_data='af-ZA')
button_noNO = telebot.types.InlineKeyboardButton('Noruguês', callback_data='no-NO')

#Botões sim ou não
botao_sim = telebot.types.InlineKeyboardButton('Sim', callback_data='sim')
botao_nao = telebot.types.InlineKeyboardButton('Não', callback_data='nao')

#Botões de idiomas para o /tradutor
botao_portugues = telebot.types.InlineKeyboardButton('Português', callback_data='portuguese')
botao_ingles = telebot.types.InlineKeyboardButton('Inglês', callback_data='english')
botao_japones = telebot.types.InlineKeyboardButton('Japonês', callback_data='japanese')
botao_hindi = telebot.types.InlineKeyboardButton('Hindi (India)', callback_data='hindi')
botao_espanhol = telebot.types.InlineKeyboardButton('Espanhol', callback_data='spanish')
botao_coreano = telebot.types.InlineKeyboardButton('Coreano', callback_data='korean')
botao_chinesS = telebot.types.InlineKeyboardButton('Chinês Simplificado', callback_data='zh-CN')
botao_chinesT = telebot.types.InlineKeyboardButton('Chinês Tradicional', callback_data='zh-TW')
botao_frances = telebot.types.InlineKeyboardButton('Francês', callback_data='french')
botao_alemao = telebot.types.InlineKeyboardButton('Alemão', callback_data='german')
botao_italiano = telebot.types.InlineKeyboardButton('Italiano', callback_data='italian')
botao_grego = telebot.types.InlineKeyboardButton('Grego', callback_data='greek')
botao_dinamarca = telebot.types.InlineKeyboardButton('Dinamarquês', callback_data='danish')
botao_arabe = telebot.types.InlineKeyboardButton('Árabe', callback_data='arabic')
botao_afrikaans = telebot.types.InlineKeyboardButton('Afrikaans (África do Sul)', callback_data='afrikaans')
botao_noruega = telebot.types.InlineKeyboardButton('Noruguês', callback_data='norwegian')

#Botoes direita e esquerda menu
button_right1 = telebot.types.InlineKeyboardButton('->', callback_data='right1')
button_left1 = telebot.types.InlineKeyboardButton('<-', callback_data='left1')
button_right2 = telebot.types.InlineKeyboardButton('->', callback_data='right2')
button_left2 = telebot.types.InlineKeyboardButton('<-', callback_data='left2')

#Teclado1 para o /idioma
teclado1 = telebot.types.InlineKeyboardMarkup()
teclado1.row(button_ptBR, button_esAR)
teclado1.row(button_enUS, button_esPY)
teclado1.row(button_enGB, button_esES)
teclado1.row(button_jaJP, button_koKR)
teclado1.row(button_hiIN, button_zhCN)
teclado1.row(button_left1, button_right1)

#Teclado2 para o /idioma
teclado2 = telebot.types.InlineKeyboardMarkup()
teclado2.row(button_frFR, button_deDE)
teclado2.row(button_itIT, button_elGR)
teclado2.row(button_daDK, button_arEG)
teclado2.row(button_arIL, button_afZA)
teclado2.row(button_noNO, button_zhTW)
teclado2.row(button_left2, button_right2)

#Teclado para ligar o /tradutor de texto
tecladoTradutorLigar = telebot.types.InlineKeyboardMarkup()
tecladoTradutorLigar.row(botao_sim, botao_nao)

#Menu 1 para escolher idioma do tradutor
tecladoTradutor1 = telebot.types.InlineKeyboardMarkup()
tecladoTradutor1.row(botao_portugues, botao_ingles)
tecladoTradutor1.row(botao_japones, botao_hindi)
tecladoTradutor1.row(botao_espanhol, botao_coreano)
tecladoTradutor1.row(botao_chinesS, botao_chinesT)
tecladoTradutor1.row(button_left1, button_right1)

#Menu 2 para escolher idioma do tradutor
tecladoTradutor2 = telebot.types.InlineKeyboardMarkup()
tecladoTradutor2.row(botao_frances, botao_alemao)
tecladoTradutor2.row(botao_italiano, botao_grego)
tecladoTradutor2.row(botao_dinamarca, botao_arabe)
tecladoTradutor2.row(botao_afrikaans, botao_noruega)
tecladoTradutor2.row(button_left2, button_right2)

#Funcao auxiliar para definir o idioma do texto antes da traducao para o google translate
def defineIdiomaTextoFonte():
  global idiomaAudio
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

#Funcao Auxiliar depois que um idioma para transcrição é escolhido
def idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId):
  global idiomaAudio
  idiomaAudio = buttonId

  bot.edit_message_reply_markup(chatId, messageId)  
  bot.send_message(chatId, "Ok, agora irei transcrever aúdios no idioma "+mensagem_idioma)

#Funcao Auxiliar depois que o idioma de tradução é escolhido
def idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId):
  global idiomaTradutor
  idiomaTradutor = buttonId

  bot.edit_message_reply_markup(chatId, messageId)  
  bot.send_message(chatId, "Ok, agora irei traduzir os aúdios para o idioma "+mensagem_idioma)

#Funcao para mudar o idioma de transcrição dos audios
def mudarIdiomaAudio (buttonId, chatId, messageId):
  if buttonId == "pt-BR":
    mensagem_idioma = "Português Brasil"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "en-US":
    mensagem_idioma = "Inglês Americano"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "en-BR":
    mensagem_idioma = "Inglês Britânico"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "ja-JP":
    mensagem_idioma = "Japonês"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "hi-IN":
    mensagem_idioma = "Hindi"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "es-AR":
    mensagem_idioma = "Espanhol Argentino"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "es-PY":
    mensagem_idioma = "Espanhol Paraguaio"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "es-ES":
    mensagem_idioma = "Espanhol Espanhol"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "ko-KR":
    mensagem_idioma = "Coreano"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "zh-CN":
    mensagem_idioma = "Chinês"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "zh-TW":
    mensagem_idioma = "Chinês Taiwan"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "fr-FR":
    mensagem_idioma = "Francês"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "de-DE":
    mensagem_idioma = "Alemão"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "it-IT":
    mensagem_idioma = "Italiano"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "el-GR":
    mensagem_idioma = "Grego"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "da-DK":
    mensagem_idioma = "Dinamarquês"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "ar-EG":
    mensagem_idioma = "Árabe Egipcio"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "ar-IL":
    mensagem_idioma = "Árabe Israel"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "af-ZA":
    mensagem_idioma = "Afrikaans (Africa do Sul)"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "no-NO":
    mensagem_idioma = "Noruguês"
    idioma_escolhido_audio(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "right1":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=teclado2)
  elif buttonId == "left2":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=teclado1)

#Funcao para mudar o idioma do tradutor
def mudarIdiomaTradutor (buttonId, chatId, messageId):
  if buttonId == "portuguese":
    mensagem_idioma = "Português"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "english":
    mensagem_idioma = "Inglês"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)    
  elif buttonId == "japanese":
    mensagem_idioma = "Japonês"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "hindi":
    mensagem_idioma = "Hindi"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "spanish":
    mensagem_idioma = "Espanhol"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)    
  elif buttonId == "korean":
    mensagem_idioma = "Coreano"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "zh-CN":
    mensagem_idioma = "Chinês Simplificado"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "zh-TW":
    mensagem_idioma = "Chinês Tradicional"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "french":
    mensagem_idioma = "Francês"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "german":
    mensagem_idioma = "Alemão"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "italian":
    mensagem_idioma = "Italiano"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "greek":
    mensagem_idioma = "Grego"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "danish":
    mensagem_idioma = "Dinamarquês"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "arabic":
    mensagem_idioma = "Árabe"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)    
  elif buttonId == "afrikaans":
    mensagem_idioma = "Afrikaans (Africa do Sul)"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)  
  elif buttonId == "norwegian":
    mensagem_idioma = "Noruguês"
    idioma_escolhido_tradutor(chatId, messageId, mensagem_idioma, buttonId)
  elif buttonId == "right1":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=tecladoTradutor2)
  elif buttonId == "left2":
    bot.edit_message_reply_markup(chatId, messageId, reply_markup=tecladoTradutor1)

#/ajuda
@bot.message_handler(commands=['ajuda'])
def ajuda(message):
    bot.send_message(message.chat.id, "Bem vindo ao AudioParaTexto! Um bot que transforma seus audios em texto. Mande um audio ou arquivo de som e deixe a mágica acontecer!\n\n/ajuda = Mostra os comandos disponiveis para o bot.\n/idioma = Escolha o idioma do audio que será transcrito.\n/tradutor = Escolha se quer ligar o tradutor de texto e para qual idioma deseja traduzir.")

#/idioma
@bot.message_handler(commands=['idioma'])
def MenuIdioma(message):
    bot.send_message(message.chat.id, "Selecione o idioma do audio que será transcrito:", reply_markup=teclado1)

#/tradutor
@bot.message_handler(commands=['tradutor'])
def tradutor(message):
    bot.send_message(message.chat.id, "Desejar ligar o tradutor de texto?", reply_markup=tecladoTradutorLigar)

#Handler dos botoes de /idioma e /tradutor
@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
  #print(query)
  buttonId = query.data
  chatId = query.message.chat.id
  messageId = query.message.message_id
  messageText = query.message.text
  bot.answer_callback_query(query.id)

  global tradutorLigado
  
  if buttonId == "sim":
    tradutorLigado = True
    bot.edit_message_reply_markup(chatId, messageId)
    bot.send_message(chatId, "Escolha para qual idioma deseja traduzir:", reply_markup=tecladoTradutor1)
  elif buttonId == "nao":
    tradutorLigado = False
    bot.edit_message_reply_markup(chatId, messageId)  
    bot.send_message(chatId, "Ok, tradutor de texto desligado")
    
  elif messageText == "Selecione o idioma do audio que será transcrito:":
    mudarIdiomaAudio(buttonId, chatId, messageId)
  elif messageText == "Escolha para qual idioma deseja traduzir:":
    mudarIdiomaTradutor(buttonId, chatId, messageId)
    
#Transcriçao de audio para texto
@bot.message_handler(content_types=['audio', 'video', 'video_note', 'voice'])
def transcriber(message):
  downloadedAudioFile = 'TemporaryFiles/downloadedFile.ogg'
  convertedAudioFile = "TemporaryFiles/convertedFile.wav"

  
  if message.content_type == 'voice':
    file = bot.get_file(message.voice.file_id)
  elif message.content_type == 'audio':
    file = bot.get_file(message.audio.file_id)

  downloaded_file = bot.download_file(file.file_path)
  with open(downloadedAudioFile, 'wb') as new_file:
    new_file.write(downloaded_file)


  # convert mp3 to wav file
  subprocess.call(['ffmpeg', '-i', downloadedAudioFile, convertedAudioFile, '-y'])
   
  # initialize the recognizer
  recognizer = speech_recognition.Recognizer()

  # open the file
  with speech_recognition.AudioFile(convertedAudioFile) as source:
    # listen for the data (load audio to memory)
    audio_data = recognizer.record(source)
    
    # recognize (convert from speech to text)
    try:
      print("\nIdioma a ser usado = "+idiomaAudio+"\n")
      TextoResultado = recognizer.recognize_google(audio_data, 
                                           key=Google_Speech_API_KEY, 
                                           language=idiomaAudio)
      
      TextoTraduzido = GoogleTranslator(source=defineIdiomaTextoFonte(),
                                        target=idiomaTradutor).translate(TextoResultado)

      if tradutorLigado == True:
        bot.reply_to(message, "Texto do audio: "+TextoResultado+"\nTexto Traduzido: "+TextoTraduzido)
      else:
        bot.reply_to(message, TextoResultado)
      
    except speech_recognition.UnknownValueError:
      MensagemErro = 'Desculpa, não entendi o que voce falou.'
      bot.reply_to(message, MensagemErro)

    except speech_recognition.RequestError as error:
      print("Could not request results from Google Speech API service; {0}".format(error))
      MensagemErro = 'Sistema fora do ar. Tente novamente mais tarde.'
      bot.reply_to(message, MensagemErro)

bot.polling()


