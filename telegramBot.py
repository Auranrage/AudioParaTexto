import passwords
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
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# Configuracoes basicas dos logs
logFilename = 'Logs/{:%Y%m%d}.log'.format(datetime.now())

logging.basicConfig(level=logging.INFO, filename=logFilename, filemode='a', datefmt='%y-%m-%d %H:%M:%S',
                    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s')

# Aviso de que o programa iniciou
logging.info('Bot started. Good morning administrator')
print('Bot started. Good morning administrator')

# regex para aceitar so numeros de 4 algarismos
regex = re.compile('^[0-9]{4}$')

#Variaveis
API_KEY = passwords.API_KEY
bot = telebot.TeleBot(API_KEY)
Google_Speech_API_KEY = passwords.Google_Speech_API_Key

#Iniciar analisador de sentimentos
s = SentimentIntensityAnalyzer()

#/start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        logging.info('User %s requested /start function', message.chat.id)
        print('User '+str(message.chat.id)+' requested /start function')

        bot.send_message(message.chat.id, "Bem vindo ao AudioParaTexto! Um bot que transforma seus audios em texto. "
                                        "Mande um audio ou arquivo de som e deixe a mágica acontecer!\n\n"
                                        "/ajuda = Mostra os comandos disponiveis para o bot.\n"
                                        "/idioma = Escolha o idioma do audio que será transcrito.\n"
                                        "/tradutor = Escolha se quer ligar o tradutor de texto e para qual idioma deseja traduzir.\n"
                                        "/config = Veja as configurações atuais do bot.\n"
                                        "/parental = Configure para um responsável receber alertas caso um dependente receba mensagens ofensivas.")

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

        bot.send_message(message.chat.id, "Bem vindo ao AudioParaTexto! Um bot que transforma seus audios em texto. "
                                        "Mande um audio ou arquivo de som e deixe a mágica acontecer!\n\n"
                                        "/ajuda = Mostra os comandos disponiveis para o bot.\n"
                                        "/idioma = Escolha o idioma do audio que será transcrito.\n"
                                        "/tradutor = Escolha se quer ligar o tradutor de texto e para qual idioma deseja traduzir.\n"
                                        "/config = Veja as configurações atuais do bot.\n"
                                        "/parental = Configure para um responsável receber alertas caso um dependente receba mensagens ofensivas.")

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

        #Verificar e criar user se nao existir
        chatId = message.chat.id
        first_name = message.chat.first_name
        last_name = message.chat.last_name

        dbFunc.checkUserExist(chatId, first_name, last_name)

        #Pegar dados do user no banco de dados
        userData = dbFunc.getUserData(message.chat.id)
        nome = userData[1]
        sobrenome = userData[2]
        audio = auxFunc.showInternalConfigToUser(userData[3])
        tradutorLigado = userData[4]
        tradutor = auxFunc.showInternalConfigToUser(userData[5])
        parentalFlag = userData[6]
        nomeFamilia=dbFunc.showParentalConfig(chatId, parentalFlag)

        if parentalFlag == 1:
            if tradutorLigado == 0:
                bot.send_message(message.chat.id, "Olá "+nome+" "+sobrenome+". AudioParaTexto está configurado da seguinte maneira para você. "
                                                  "Use os comandos /idioma e /tradutor para mudar suas configurações.\n\n"
                                                  "Idioma do audio que será transcrito = "+audio+"\nTradutor de texto = Desligado\n"
                                                  "Você está ligado ao responsável "+nomeFamilia[0]+" "+nomeFamilia[1])
            elif tradutorLigado == 1:
                bot.send_message(message.chat.id, "Olá "+nome+" "+sobrenome+". AudioParaTexto está configurado da seguinte maneira para você. "
                                                  "Use os comandos /idioma e /tradutor para mudar suas configurações.\n\n"
                                                  "Idioma do audio que será transcrito = "+audio+"\nTradutor de texto = Ligado\n"
                                                  "Idioma para o qual o texto será traduzido = "+tradutor+"\n"
                                                  "Você está ligado ao responsável "+nomeFamilia[0]+" "+nomeFamilia[1])
        elif parentalFlag == 3:
            if tradutorLigado == 0:
                bot.send_message(message.chat.id, "Olá "+nome+" "+sobrenome+". AudioParaTexto está configurado da seguinte maneira para você. "
                                                  "Use os comandos /idioma e /tradutor para mudar suas configurações.\n\n"
                                                  "Idioma do audio que será transcrito = "+audio+"\nTradutor de texto = Desligado\n"
                                                  "Você recebe alertas como responsável de "+nomeFamilia[0]+" "+nomeFamilia[1])
            elif tradutorLigado == 1:
                bot.send_message(message.chat.id, "Olá "+nome+" "+sobrenome+". AudioParaTexto está configurado da seguinte maneira para você. "
                                                  "Use os comandos /idioma e /tradutor para mudar suas configurações.\n\n"
                                                  "Idioma do audio que será transcrito = "+audio+"\nTradutor de texto = Ligado\n"
                                                  "Idioma para o qual o texto será traduzido = "+tradutor+"\n"
                                                  "Você recebe alertas como responsável de "+nomeFamilia[0]+" "+nomeFamilia[1])
        else:
            if tradutorLigado == 0:
                bot.send_message(message.chat.id, "Olá "+nome+" "+sobrenome+". AudioParaTexto está configurado da seguinte maneira para você. "
                                                  "Use os comandos /idioma e /tradutor para mudar suas configurações.\n\n"
                                                  "Idioma do audio que será transcrito = "+audio+"\nTradutor de texto = Desligado")
            elif tradutorLigado == 1:
                bot.send_message(message.chat.id, "Olá "+nome+" "+sobrenome+". AudioParaTexto está configurado da seguinte maneira para você. "
                                                  "Use os comandos /idioma e /tradutor para mudar suas configurações.\n\n"
                                                  "Idioma do audio que será transcrito = "+audio+"\nTradutor de texto = Ligado\n"
                                                  "Idioma para o qual o texto será traduzido = "+tradutor)


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

#/parental
@bot.message_handler(commands=['parental'])
def parental(message):
    try:
        logging.info('User %s requested /parental function', message.chat.id)
        print('User '+str(message.chat.id)+' requested /parental function')

        # Verificar e criar user se nao existir
        chatId = message.chat.id
        first_name = message.chat.first_name
        last_name = message.chat.last_name

        dbFunc.checkUserExist(chatId, first_name, last_name)

        # Pegar dados do user no banco de dados
        userData = dbFunc.getUserData(message.chat.id)
        parentalFlag = userData[6]

        if parentalFlag==3:
            bot.send_message(message.chat.id, "Para configurar o controle parental do bot, é necessário que o dependente"
                                        "mande um código para o responsável. Você é um responsável ou um dependente?",
                                        reply_markup=teclado.parentalR)
        else:
            bot.send_message(message.chat.id, "Para configurar o controle parental do bot, é necessário que o dependente"
                                        "mande um código para o responsável. Você é um responsável ou um dependente?",
                                        reply_markup=teclado.parental)

    except Exception as exception:
        logging.exception('An exception occurred = ')
        print("An exception occurred = "+str(exception))

#Handler dos botoes de /idioma, /tradutor e /parental
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

        #Se for responsavel, mandar um pin para saber o chatId do dependente
        elif buttonId == "responsavel":
            with connect:
                cursor.execute("UPDATE users SET parental_ligado = 2 WHERE user_id = :id",{'id':chatId})
            bot.edit_message_reply_markup(chatId, messageId)
            bot.send_message(chatId, "Ótimo. Agora no telegram do dependente, escolha a opção 'Dependente' "
                                     "e depois digite aqui o número de 4 algarismos criado.")

            logging.info('User %s turned on parental control to child %s. Waiting confirmation.', chatId, buttonId)
            print('User '+str(chatId)+' turned parental control to child '+buttonId+'. Waiting confirmation.')

        #Se for dependente, enviar um pin para ser usado pelo responsavel
        elif buttonId == "dependente":
            pinNumber=dbFunc.sendPinNumber(chatId)

            bot.edit_message_reply_markup(chatId, messageId)
            bot.send_message(chatId, "Mande o código abaixo para o responsável digitar:\n" + str(pinNumber))

            logging.info('User %s received code to send to parent', chatId)
            print('User ' + str(chatId) + ' received code to send to parent')

        elif buttonId == "cancelar":
            bot.edit_message_reply_markup(chatId, messageId)
            bot.send_message(chatId, "Tem certeza que deseja cancelar o controle parental de todos os seus dependentes?",
                             reply_markup=teclado.parentalCancelar)

            logging.info('User %s-Initiated parental control cancellation', chatId)
            print('User ' + str(chatId) + '-Initiated parental control cancellation')

        elif buttonId == "naoP":
            bot.edit_message_reply_markup(chatId, messageId)
            bot.send_message(chatId, "Ok, controle parental mantido")

            logging.info('User %s-Gave on cancelling parental control', chatId)
            print('User ' + str(chatId) + '-Gave on cancelling parental control')

        elif buttonId == "simP":
            dbFunc.cancelParentalControl(chatId)

            bot.edit_message_reply_markup(chatId, messageId)
            bot.send_message(chatId, "Entendido. Controle parental cancelado")

            logging.info('User %s-Cancellation of parental control completed', chatId)
            print('User ' + str(chatId) + '-Cancellation of parental control completed')

        connect.commit()
        connect.close()

    except Exception as exception:
        logging.exception('An exception occurred = ')
        print("An exception occurred = "+str(exception))


#Confirmacao do pin para controle parental
@bot.message_handler(content_types=['text'])
def parental_confirm(message):
    try:
        logging.info('User %s wrote a text', message.chat.id)
        print('User '+str(message.chat.id)+' wrote a text')

        chatId = message.chat.id
        first_name = message.chat.first_name
        last_name = message.chat.last_name

        dbFunc.checkUserExist(chatId, first_name, last_name)

        userData = dbFunc.getUserData(chatId)
        #print(userData)
        #userData example = (5480482418, 'Rodrigo', 'Cardoso', 'pt-BR', 0, 'portuguese', parentalFlag(int), parentalId(int))
        parentalFlag = userData[6]

        if parentalFlag == 2:
            match = regex.match(message.text)
            if match is None:
                bot.send_message(chatId, "O texto digitado não é um número de 4 algarismos. Por favor digite um código válido.")
                logging.info('User %s-Typed a text that is not a number of 4 digits', message.chat.id)
                raise Exception('Message is not numeric or its length is not 4')
            else:
                retorno = dbFunc.addParental(chatId, int(message.text))
                if retorno == 0:
                    bot.send_message(chatId, "Sucesso! Controle parental configurado.")
                elif retorno == 1:
                    bot.send_message(chatId, "Número inválido.")

        logging.info('User %s-End of text handler', message.chat.id)
        print('User ' + str(message.chat.id) + '-End of text handler')

    except Exception as exception:
        logging.exception('An exception occurred = ')
        print("An exception occurred = "+str(exception))


#Transcriçao de audio para texto
@bot.message_handler(content_types = ['audio', 'voice'])
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
        parentalControl = userData[6]
        parentalChatId = userData[7]

        downloadedAudioFile = 'TemporaryFiles/downloadedFile.ogg'
        convertedAudioFile = "TemporaryFiles/convertedFile.wav"

        file = ''
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

                #Analise de sentimento
                if idiomaAudio == 'en-US' or idiomaAudio == 'en-GB':
                    TextoEmIngles = TextoResultado
                else:
                    TextoEmIngles = GoogleTranslator(source=auxFunc.defineIdiomaTextoFonte(idiomaAudio),
                                                     target='english').translate(TextoResultado)

                TextoSentimento=s.polarity_scores(TextoEmIngles)
                print('User '+str(chatId)+'-text analyzed=\n'+TextoEmIngles)
                print('User '+str(chatId)+'-values of the sentiment=\n'+str(TextoSentimento))

                sentimentoPontuacao=TextoSentimento['compound']

                logging.info('User %s-Bot finished analyzing the sentiment of the text', chatId)
                print('User '+str(chatId)+'-Bot finished analyzing the sentiment of the text')


                #Traducao
                if tradutorLigado == 1:
                    if idiomaTradutor=='english':
                        TextoTraduzido=TextoEmIngles
                    else:
                        TextoTraduzido = GoogleTranslator(source=auxFunc.defineIdiomaTextoFonte(idiomaAudio),
                                                target=idiomaTradutor).translate(TextoResultado)

                    logging.info('User %s-Bot finished translating the resulting text', chatId)
                    print('User '+str(message.chat.id)+'-Bot finished translating the resulting text')

                    #Reply ao usuario
                    bot.reply_to(message, "Texto do audio: "+TextoResultado+"\n\nTexto Traduzido: "+TextoTraduzido)
                    if sentimentoPontuacao<0.0:
                        if parentalControl==1:
                            bot.send_message(parentalChatId, "Alerta!! Seu dependente recebeu uma mensagem com teor negativo, "
                                                             "que pode ser ofensiva ou prejudicial para ele.\n\n"
                                                             "Mensagem recebida: "+TextoResultado)

                    logging.info('User %s-Result of translation sent to user', chatId)
                    print('User '+str(chatId)+'-Result of translation sent to user')

                else:
                    bot.reply_to(message, TextoResultado)
                    if sentimentoPontuacao<0.0:
                        if parentalControl == 1:
                            bot.send_message(parentalChatId, "Alerta!! Seu dependente recebeu uma mensagem com teor negativo, "
                                                             "que pode ser ofensiva ou prejudicial para ele.\n\n"
                                                             "Mensagem recebida: "+TextoResultado)

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
