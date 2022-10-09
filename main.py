import os
import telebot
import sqlite3
import speech_recognition
import subprocess
from deep_translator import GoogleTranslator
import AuxiliaryFiles.Teclado as teclado
import AuxiliaryFiles.FuncoesAuxiliares as auxFunc
import AuxiliaryFiles.DatabaseFunctions as dbFunc


#Variaveis
API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

Google_Speech_API_KEY = os.environ['Google_Speech_API_Key']

#/start
@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, "Bem vindo ao AudioParaTexto! Um bot que transforma seus audios em texto. Mande um audio ou arquivo de som e deixe a mágica acontecer!\n\n/ajuda = Mostra os comandos disponiveis para o bot.\n/idioma = Escolha o idioma do audio que será transcrito.\n/tradutor = Escolha se quer ligar o tradutor de texto e para qual idioma deseja traduzir.")

#/ajuda
@bot.message_handler(commands=['ajuda'])
def ajuda(message):
  bot.send_message(message.chat.id, "Bem vindo ao AudioParaTexto! Um bot que transforma seus audios em texto. Mande um audio ou arquivo de som e deixe a mágica acontecer!\n\n/ajuda = Mostra os comandos disponiveis para o bot.\n/idioma = Escolha o idioma do audio que será transcrito.\n/tradutor = Escolha se quer ligar o tradutor de texto e para qual idioma deseja traduzir.")

#/idioma
@bot.message_handler(commands=['idioma'])
def MenuIdioma(message):
  bot.send_message(message.chat.id, "Selecione o idioma do audio que será transcrito:", reply_markup=teclado.idioma1)

#/tradutor
@bot.message_handler(commands=['tradutor'])
def tradutor(message):
  bot.send_message(message.chat.id, "Deseja ligar o tradutor de texto?", reply_markup=teclado.ligarTradutor)

#Handler dos botoes de /idioma e /tradutor
@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
  #Variaveis
  buttonId = query.data
  chatId = query.message.chat.id
  first_name = query.message.chat.first_name
  last_name = query.message.chat.last_name
  messageId = query.message.message_id
  messageText = query.message.text
  bot.answer_callback_query(query.id)

  dbFunc.checkUserExist(chatId, first_name, last_name)
  
  connect = sqlite3.connect('database.db')
  cursor = connect.cursor()
  
  if buttonId == "sim":
    with connect:
      cursor.execute("UPDATE users SET tradutor_ligado = 1 WHERE user_id = :id",{'id':chatId})
    bot.edit_message_reply_markup(chatId, messageId)
    bot.send_message(chatId, "Escolha para qual idioma deseja traduzir:", reply_markup=teclado.tradutor1)
  elif buttonId == "nao":
    with connect:
      cursor.execute("UPDATE users SET tradutor_ligado = 0 WHERE user_id = :id",{'id':chatId})
    bot.edit_message_reply_markup(chatId, messageId)  
    bot.send_message(chatId, "Ok, tradutor de texto desligado")
    
  elif messageText == "Selecione o idioma do audio que será transcrito:":
    auxFunc.mudarIdiomaAudio(buttonId, chatId, messageId)
    with connect:
      cursor.execute("UPDATE users SET idioma = :idioma WHERE user_id = :id",
                     {'idioma':buttonId,'id':chatId})
  elif messageText == "Escolha para qual idioma deseja traduzir:":
    auxFunc.mudarIdiomaTradutor(buttonId, chatId, messageId)
    with connect:
      cursor.execute("UPDATE users SET idioma_tradutor = :idiomaT WHERE user_id = :id",
                     {'idiomaT':buttonId,'id':chatId})
  
  connect.close()  
  
#Transcriçao de audio para texto
@bot.message_handler(content_types=['audio', 'video', 'video_note', 'voice'])
def transcriber(message):
  chatId = message.chat.id
  first_name = message.chat.first_name
  last_name = message.chat.last_name
  
  dbFunc.checkUserExist(chatId, first_name, last_name)

  #Get user data in database
  connect = sqlite3.connect('database.db')
  cursor = connect.cursor()
  cursor.execute("SELECT * FROM users WHERE user_id = :id",{'id': chatId})
  userData = cursor.fetchone()
  #print(userData)
  #userData example = (5480482418, 'Rodrigo', 'Cardoso', 'pt-BR', 0, 'portuguese')
  idiomaAudio = userData[3]
  tradutorLigado = userData[4]
  idiomaTradutor = userData[5]
  connect.close()
  
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
      
      TextoTraduzido = GoogleTranslator(source=auxFunc.defineIdiomaTextoFonte(idiomaAudio),
                                        target=idiomaTradutor).translate(TextoResultado)

      if tradutorLigado == 1:
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


