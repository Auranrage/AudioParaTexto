import telebot
import AuxiliaryFiles.Botao as botao

#Teclado1 para o /idioma
idioma1 = telebot.types.InlineKeyboardMarkup()
idioma1.row(botao.ptBR, botao.esAR)
idioma1.row(botao.enUS, botao.esPY)
idioma1.row(botao.enGB, botao.esES)
idioma1.row(botao.jaJP, botao.koKR)
idioma1.row(botao.hiIN, botao.zhCN)
idioma1.row(botao.left1, botao.right1)

#Teclado2 para o /idioma
idioma2 = telebot.types.InlineKeyboardMarkup()
idioma2.row(botao.frFR, botao.deDE)
idioma2.row(botao.itIT, botao.elGR)
idioma2.row(botao.daDK, botao.arEG)
idioma2.row(botao.arIL, botao.afZA)
idioma2.row(botao.noNO, botao.zhTW)
idioma2.row(botao.left2, botao.right2)

#Teclado para ligar o /tradutor de texto
ligarTradutor = telebot.types.InlineKeyboardMarkup()
ligarTradutor.row(botao.sim, botao.nao)

#Menu 1 para escolher idioma do tradutor
tradutor1 = telebot.types.InlineKeyboardMarkup()
tradutor1.row(botao.portugues, botao.ingles)
tradutor1.row(botao.japones, botao.hindi)
tradutor1.row(botao.espanhol, botao.coreano)
tradutor1.row(botao.chinesS, botao.chinesT)
tradutor1.row(botao.left1, botao.right1)

#Menu 2 para escolher idioma do tradutor
tradutor2 = telebot.types.InlineKeyboardMarkup()
tradutor2.row(botao.frances, botao.alemao)
tradutor2.row(botao.italiano, botao.grego)
tradutor2.row(botao.dinamarca, botao.arabe)
tradutor2.row(botao.afrikaans, botao.noruega)
tradutor2.row(botao.left2, botao.right2)
