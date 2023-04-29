import sqlite3
import logging
from datetime import datetime

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
    
    cursor.execute("INSERT INTO users VALUES (:id, :first, :last, :idioma, :boolTradutor, :idiomaT)",
                   {'id': chatId,
                    'first':first_name,
                    'last':last_name,
                    'idioma':'pt-BR',
                    'boolTradutor':0,
                    'idiomaT':'portuguese'
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
    
