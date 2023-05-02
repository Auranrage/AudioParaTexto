import sqlite3
import logging
from datetime import datetime
import random


logFilename = 'Logs/{:%Y%m%d}.log'.format(datetime.now())
logging.basicConfig(level=logging.INFO, filename=logFilename, filemode='a', datefmt='%y-%m-%d %H:%M:%S',
                    format='%(asctime)s-%(process)d-%(levelname)s-%(message)s')



def checkUserExist(chatId, first_name, last_name):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()
  
    cursor.execute("SELECT count(user_id) FROM users WHERE user_id = :id",{'id': chatId})
    userExist = cursor.fetchone()
  
    if userExist[0] == 0:
        logging.info('User %s is using the system for the first time. Adding user to database.', chatId)
        print('User '+str(chatId)+' is using the system for the first time. Adding user to database.')
    
        cursor.execute("INSERT INTO users VALUES (:id, :first, :last, :idioma, :boolTradutor, :idiomaT, :parental_ligado, :parental_chatId)",
                       {'id': chatId,
                        'first':first_name,
                        'last':last_name,
                        'idioma':'pt-BR',
                        'boolTradutor':0,
                        'idiomaT':'portuguese',
                        'parental_ligado':0,
                        'parental_chatId':0
                        }
                    )
        connect.commit()

        logging.info('User %s added to users table.', chatId)
        print('User '+str(chatId)+' added to users table.')
    connect.close()

def getUserData(chatId):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = :id",{'id': chatId})
    userData = cursor.fetchone()
    #print(userData)
    #userData example = (5480482418, 'Rodrigo', 'Cardoso', 'pt-BR', 0, 'portuguese')
  
    connect.close()
    return userData

#Criar e enviar o pin do dependente
def sendPinNumber(chatId):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    #Mudar para seed()
    random.seed()

    #Cria um numero aleatorio entre 0 e 9999
    pinNumber=random.randint(1000, 9999)
    logging.info('User %s-Pin %s created.', chatId, pinNumber)
    print('User '+str(chatId)+' Number '+str(pinNumber))

    #Deleta pins com mais de 10 minutos gravados no banco de dados
    cursor.execute("DELETE FROM parental_codes WHERE user_id in ("
                   "SELECT user_id FROM parental_codes WHERE date <= ("
                   "select datetime('now','-10 minutes')"
                   "))")
    connect.commit()

    #Verifica se esse pin ja ta sendo usado, se ja tem um row no bd com esse pin
    cursor.execute("SELECT count(pin_number) FROM parental_codes WHERE pin_number = :pin", {'pin': pinNumber})
    pinExist = cursor.fetchone()

    #Se tiver, cria outro pin ate ser um pin novo
    while pinExist[0] == 1:
        random.seed()
        logging.info('User %s-Pin %s already exists. Creating new pin.', chatId, pinNumber)
        print('User ' + str(chatId) + ' Number ' + str(pinNumber)+" already exists. Creating new pin.")

        pinNumber = random.randint(1000, 9999)

        logging.info('User %s-Pin %s created.', chatId, pinNumber)
        print('User ' + str(chatId) + ' Number ' + str(pinNumber))

        cursor.execute("SELECT count(pin_number) FROM parental_codes WHERE pin_number = :pin",
                       {'pin': pinNumber})
        pinExist = cursor.fetchone()

    #Insere o pin junto com o chatId na tabela
    cursor.execute("SELECT count(user_id) FROM parental_codes WHERE user_id = :id", {'id': chatId})
    userExist = cursor.fetchone()

    if userExist[0] == 0:
        cursor.execute("INSERT INTO parental_codes VALUES (:id, :pin, datetime('now'))",
                            {'id': chatId,
                            'pin': pinNumber
                            }
                        )
        connect.commit()
    else:
        cursor.execute("SELECT pin_number FROM parental_codes WHERE user_id = :id", {'id': chatId})
        pinNumberTemp = cursor.fetchone()
        pinNumber = pinNumberTemp[0]

    logging.info('User %s-Pin created and added to parental table.', chatId)
    print('User ' + str(chatId) + '-Pin created and added to parental table.')

    connect.close()
    return pinNumber

#Ligar parent ao child de acordo com o pin
def addParental(chatId, pin):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    logging.info('User %s-Adding parent to child parental control.', chatId)
    print('User ' + str(chatId) + '-Adding parent to child parental control.')

    #Id do responsavel foi quem iniciou o processo
    parentId=chatId

    #Id do dependente esta na tabela parental_codes de acordo com o pin
    cursor.execute("SELECT user_id FROM parental_codes WHERE pin_number = :pin", {'pin': pin})
    childIdTemp = cursor.fetchone()

    if childIdTemp == None:
        return 1

    childId = childIdTemp[0]

    # Tirar a flag do responsavel para avisar ao sistema que nao precisa mais esperar por um codigo
    # 3 = responsavel que tem um dependente configurado
    cursor.execute("UPDATE users SET parental_ligado = 3 WHERE user_id = :id",
                   {'id': parentId})

    #Update na tabela users, para o dependente passar a enviar alertas ao responsavel
    cursor.execute("UPDATE users SET parental_ligado = 1, parental_chatId=:parentId WHERE user_id = :id",
                   {'parentId': parentId, 'id': childId})

    #Apagar o pin da tabela de pins
    cursor.execute("DELETE FROM parental_codes WHERE pin_number=:pin", {'pin': pin})

    logging.info('User %s-Parent chatId added successfully to child parental control', chatId)
    print('User ' + str(chatId) + ' Parent chatId added successfully to child parental control')

    connect.commit()
    connect.close()
    return 0

def cancelParentalControl(chatId):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    # Update o child que tava ligado ao parent para 0 e deixar de mandar alertas
    cursor.execute("UPDATE users SET parental_ligado=0, parental_chatId=0 WHERE parental_chatId=:id", {'id': chatId})

    #Atualizar de 3 para 0 no responsavel para ele deixar de ser considerado um responsavel
    cursor.execute("UPDATE users SET parental_ligado=0 WHERE user_id=:id", {'id': chatId})

    connect.commit()
    connect.close()

def showParentalConfig(chatId, parentalFlag):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    name = 'none'

    #Se 1, dependente. Mostrar o parent
    if parentalFlag==1:
        cursor.execute("SELECT parental_chatId FROM users WHERE user_id = :id", {'id': chatId})
        parentIdTemp = cursor.fetchone()
        parentId = parentIdTemp[0]

        cursor.execute("SELECT first_name, last_name FROM users WHERE user_id = :id", {'id': parentId})
        name = cursor.fetchone()


    #Se 3, responsavel, mostrar o dependente
    elif parentalFlag==3:
        cursor.execute("SELECT first_name, last_name FROM users WHERE parental_chatId = :id", {'id': chatId})
        name = cursor.fetchone()

    connect.close()
    return name


