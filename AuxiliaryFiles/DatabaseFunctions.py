import sqlite3

def checkUserExist(chatId, first_name, last_name):
  connect = sqlite3.connect('database.db')
  cursor = connect.cursor()
  
  cursor.execute("SELECT count(user_id) FROM users WHERE user_id = :id",{'id': chatId})
  userExist = cursor.fetchone()
    
  if userExist[0] == 0:
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

  connect.close()