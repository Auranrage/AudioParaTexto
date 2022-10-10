import os
import telebot
import sqlite3
import subprocess
import logging
from datetime import datetime
import speech_recognition
from deep_translator import GoogleTranslator
import AuxiliaryFiles.Teclado as teclado
import AuxiliaryFiles.FuncoesAuxiliares as auxFunc
import AuxiliaryFiles.DatabaseFunctions as dbFunc


logFilename = 'Logs/{:%Y%m%d}.log'.format(datetime.now())

logging.basicConfig(level=logging.INFO, filename=logFilename, filemode='a', datefmt='%y-%m-%d %H:%M:%S',
                    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s')
logging.info('Bot started. Good morning administrator')
print('Bot started. Good morning administrator')

#Variaveis
API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)

Google_Speech_API_KEY = os.environ['Google_Speech_API_Key']


  #/start
@bot.message_handler(commands=['start'])
def start(message):
  try:
    logging.info('User %s requested /start function', message.chat.id)
    print('User '+str(message.chat.id)+' requested /start function')
    
    bot.send_message(message.chat.id, "Bem vindo ao AudioParaTexto! Um bot que transforma seus audios em texto. Mande um audio ou arquivo de som e deixe a mágica acontecer!\n\n/ajuda = Mostra os comandos disponiveis para o bot.\n/idioma = Escolha o idioma do audio que será transcrito.\n/tradutor = Escolha se quer ligar o tradutor de texto e para qual idioma deseja traduzir.\n/config = Veja as configurações atuais do bot.")

    logging.info('User %s request to /start function COMPLETED', message.chat.id)
    print('User '+str(message.chat.id)+' request to /start function COMPLETED')

  except Exception as exception:
    logging.exception('An exception occurred = ')
    print("An exception occurred = "+str(exception))

#/ajuda
@bot.message_handler(commands=['ajuda'])
def ajuda(message):
  try:
    logging.info('User %s requested /ajuda function', message.chat.id)
    print('User '+str(message.chat.id)+' requested /ajuda function')
    
    bot.send_message(message.chat.id, "Bem vindo ao AudioParaTexto! Um bot que transforma seus audios em texto. Mande um audio ou arquivo de som e deixe a mágica acontecer!\n\n/ajuda = Mostra os comandos disponiveis para o bot.\n/idioma = Escolha o idioma do audio que será transcrito.\n/tradutor = Escolha se quer ligar o tradutor de texto e para qual idioma deseja traduzir.\n/config = Veja as configurações atuais do bot.")
  
    logging.info('User %s request to /ajuda function COMPLETED', message.chat.id)
    print('User '+str(message.chat.id)+' request to /ajuda function COMPLETED')
    
  except Exception as exception:
    logging.exception('An exception occurred = ')
    print("An exception occurred = "+str(exception))

#/config
@bot.message_handler(commands=['config'])
def config(message):
  try:
    logging.info('User %s requested /config function', message.chat.id)
    print('User '+str(message.chat.id)+' requested /config function')

    userData = dbFunc.getUserData(message.chat.id)
    nome = userData[1]
    sobrenome = userData[2]
    audio = auxFunc.showInternalConfigToUser(userData[3])
    tradutorLigado = userData[4]
    tradutor = auxFunc.showInternalConfigToUser(userData[5])
    
    if tradutorLigado == 0:
      	bot.send_message(message.chat.id, "Olá "+nome+" "+sobrenome+". AudioParaTexto está configurado da seguinte maneira para você. Use os comandos /idioma e /tradutor para mudar suas configurações.\n\nIdioma do audio que será transcrito = "+audio+"\nTradutor de texto = Desligado")
    elif tradutorLigado == 1:
      	bot.send_message(message.chat.id, "Olá "+nome+" "+sobrenome+". AudioParaTexto está configurado da seguinte maneira para você. Use os comandos /idioma e /tradutor para mudar suas configurações.\n\nIdioma do audio que será transcrito = "+audio+"\nTradutor de texto = Ligado\nIdioma para o qual o texto será traduzido = "+tradutor)
  
    logging.info('User %s request to /config function COMPLETED', message.chat.id)
    print('User '+str(message.chat.id)+' request to /config function COMPLETED')
    
  except Exception as exception:
    logging.exception('An exception occurred = ')
    print("An exception occurred = "+str(exception))

    
#/idioma
@bot.message_handler(commands=['idioma'])
def MenuIdioma(message):
  try:
    logging.info('User %s requested /idioma function', message.chat.id)
    print('User '+str(message.chat.id)+' requested /idioma function', message.chat.id)
    
    bot.send_message(message.chat.id, "Selecione o idioma do audio que será transcrito:", reply_markup=teclado.idioma1)
    
  except Exception as exception:
    logging.exception('An exception occurred = ')
    print("An exception occurred = "+str(exception))

#/tradutor
@bot.message_handler(commands=['tradutor'])
def tradutor(message):
  try:
    logging.info('User %s requested /tradutor function', message.chat.id)
    print('User '+str(message.chat.id)+' requested /tradutor function')
  
    bot.send_message(message.chat.id, "Deseja ligar o tradutor de texto?", reply_markup=teclado.ligarTradutor)
  
  except Exception as exception:
    logging.exception('An exception occurred = ')
    print("An exception occurred = "+str(exception))

#Handler dos botoes de /idioma e /tradutor
@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
  try:
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
      
      logging.info('User %s turned the translator on', chatId)
      print('User '+str(chatId)+' turned the translator on')
      
    elif buttonId == "nao":
      with connect:
        cursor.execute("UPDATE users SET tradutor_ligado = 0 WHERE user_id = :id",{'id':chatId})
      bot.edit_message_reply_markup(chatId, messageId)  
      bot.send_message(chatId, "Ok, tradutor de texto desligado")
  
      logging.info('User %s turned the translator off', chatId)
      print('User '+str(chatId)+' turned the translator off')
      
    elif messageText == "Selecione o idioma do audio que será transcrito:":
      auxFunc.mudarIdiomaAudio(buttonId, chatId, messageId)
      with connect:
        cursor.execute("UPDATE users SET idioma = :idioma WHERE user_id = :id",
                       {'idioma':buttonId,'id':chatId})
      
      logging.info('User %s changed transcriber language to %s', chatId, buttonId)
      print('User '+str(chatId)+' changed transcriber language to '+buttonId)
      
    elif messageText == "Escolha para qual idioma deseja traduzir:":
      auxFunc.mudarIdiomaTradutor(buttonId, chatId, messageId)
      with connect:
        cursor.execute("UPDATE users SET idioma_tradutor = :idiomaT WHERE user_id = :id",
                       {'idiomaT':buttonId,'id':chatId})
        
      logging.info('User %s changed translator language to %s', chatId, buttonId)
      print('User '+str(chatId)+' changed translator language to '+buttonId)
    
    connect.close()
    
  except Exception as exception:
    logging.exception('An exception occurred = ')
    print("An exception occurred = "+str(exception))
    
#Transcriçao de audio para texto
@bot.message_handler(content_types=['audio', 'video', 'video_note', 'voice'])
def transcriber(message):
  try:
    logging.info('User %s started transcriber function', message.chat.id)
    print('User '+str(message.chat.id)+' started transcriber function')
    
    chatId = message.chat.id
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    
    dbFunc.checkUserExist(chatId, first_name, last_name)
  
    userData = dbFunc.getUserData(chatId)
    #print(userData)
    #userData example = (5480482418, 'Rodrigo', 'Cardoso', 'pt-BR', 0, 'portuguese')
    idiomaAudio = userData[3]
    tradutorLigado = userData[4]
    idiomaTradutor = userData[5]
    
    downloadedAudioFile = 'TemporaryFiles/downloadedFile.ogg'
    convertedAudioFile = "TemporaryFiles/convertedFile.wav"
  
    if message.content_type == 'voice':
      file = bot.get_file(message.voice.file_id)
    elif message.content_type == 'audio':
      file = bot.get_file(message.audio.file_id)
  
    downloaded_file = bot.download_file(file.file_path)
    with open(downloadedAudioFile, 'wb') as new_file:
      new_file.write(downloaded_file)
  
    logging.info('User %s-Bot downloaded audio file successfully', chatId)
    print('User '+str(message.chat.id)+'-Bot downloaded audio file successfully')
  
    # convert mp3 to wav file
    subprocess.call(['ffmpeg', '-i', downloadedAudioFile, convertedAudioFile, '-y'])
  
    logging.info('User %s-Bot converted the file to WAV', chatId)
    print('User '+str(message.chat.id)+'-Bot converted the file to WAV')
    
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
  
        logging.info('User %s-Bot finished transcribing the file', chatId)
        print('User '+str(chatId)+'-Bot finished transcribing the file from user')
  
        if tradutorLigado == 1:
          TextoTraduzido = GoogleTranslator(source=auxFunc.defineIdiomaTextoFonte(idiomaAudio),
                                          target=idiomaTradutor).translate(TextoResultado)
  
          logging.info('User %s-Bot finished translating the resulting text', chatId)
          print('User '+str(message.chat.id)+'-Bot finished translating the resulting text')
  
          bot.reply_to(message, "Texto do audio: "+TextoResultado+"\nTexto Traduzido: "+TextoTraduzido)
  
          logging.info('User %s-Result of translation sent to user', chatId)
          print('User '+str(chatId)+'-Result of translation sent to user')
          
        else:
          bot.reply_to(message, TextoResultado)
  
          logging.info('User %s-Result of transcriber sent to user', chatId)
          print('User '+str(chatId)+'-Result of transcriber sent to user')
        
      except speech_recognition.UnknownValueError:
        print("Google Speech API was not able to understand the audio file")
        logging.exception('Not able to understand the audio file = ')
        MensagemErro = 'Desculpa, não entendi o que voce falou.'
        bot.reply_to(message, MensagemErro)
  
      except speech_recognition.RequestError as error:
        print("Could not request results from Google Speech API service; {0}".format(error))
        logging.exception('Request error with Google Speech API = ')
        MensagemErro = 'Sistema fora do ar. Tente novamente mais tarde.'
        bot.reply_to(message, MensagemErro)
        
  except Exception as exception:
    logging.exception('An exception occurred = ')
    print("An exception occurred = "+str(exception))

bot.polling()