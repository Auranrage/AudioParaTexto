import telebot

#Botoes para /idiomas
ptBR = telebot.types.InlineKeyboardButton('Português Brasil', callback_data='pt-BR')
enUS = telebot.types.InlineKeyboardButton('Inglês Americano', callback_data='en-US')
enGB = telebot.types.InlineKeyboardButton('Inglês Britânico', callback_data='en-GB')
jaJP = telebot.types.InlineKeyboardButton('Japonês', callback_data='ja-JP')
hiIN = telebot.types.InlineKeyboardButton('Hindi (India)', callback_data='hi-IN')
esAR = telebot.types.InlineKeyboardButton('Espanhol Argentino', callback_data='es-AR')
esPY = telebot.types.InlineKeyboardButton('Espanhol Paraguaio', callback_data='es-PY')
esES = telebot.types.InlineKeyboardButton('Espanhol Espanhol', callback_data='es-ES')
koKR = telebot.types.InlineKeyboardButton('Coreano', callback_data='ko-KR')
zhCN = telebot.types.InlineKeyboardButton('Chinês Mandarin', callback_data='zh-CN')
zhTW = telebot.types.InlineKeyboardButton('Chinês Taiwan', callback_data='zh-TW')
frFR = telebot.types.InlineKeyboardButton('Francês', callback_data='fr-FR')
deDE = telebot.types.InlineKeyboardButton('Alemão', callback_data='de-DE')
itIT = telebot.types.InlineKeyboardButton('Italiano', callback_data='it-IT')
elGR = telebot.types.InlineKeyboardButton('Grego', callback_data='el-GR')
daDK = telebot.types.InlineKeyboardButton('Dinamarquês', callback_data='da-DK')
arEG = telebot.types.InlineKeyboardButton('Árabe Egipcio', callback_data='ar-EG')
arIL = telebot.types.InlineKeyboardButton('Árabe Israel', callback_data='ar-IL')
afZA = telebot.types.InlineKeyboardButton('Afrikaans (África do Sul)', callback_data='af-ZA')
noNO = telebot.types.InlineKeyboardButton('Noruguês', callback_data='no-NO')

#Botões sim ou não
sim = telebot.types.InlineKeyboardButton('Sim', callback_data='sim')
nao = telebot.types.InlineKeyboardButton('Não', callback_data='nao')

#Botões de idiomas para o /tradutor
portugues = telebot.types.InlineKeyboardButton('Português', callback_data='portuguese')
ingles = telebot.types.InlineKeyboardButton('Inglês', callback_data='english')
japones = telebot.types.InlineKeyboardButton('Japonês', callback_data='japanese')
hindi = telebot.types.InlineKeyboardButton('Hindi (India)', callback_data='hindi')
espanhol = telebot.types.InlineKeyboardButton('Espanhol', callback_data='spanish')
coreano = telebot.types.InlineKeyboardButton('Coreano', callback_data='korean')
chinesS = telebot.types.InlineKeyboardButton('Chinês Simplificado', callback_data='zh-CN')
chinesT = telebot.types.InlineKeyboardButton('Chinês Tradicional', callback_data='zh-TW')
frances = telebot.types.InlineKeyboardButton('Francês', callback_data='french')
alemao = telebot.types.InlineKeyboardButton('Alemão', callback_data='german')
italiano = telebot.types.InlineKeyboardButton('Italiano', callback_data='italian')
grego = telebot.types.InlineKeyboardButton('Grego', callback_data='greek')
dinamarca = telebot.types.InlineKeyboardButton('Dinamarquês', callback_data='danish')
arabe = telebot.types.InlineKeyboardButton('Árabe', callback_data='arabic')
afrikaans = telebot.types.InlineKeyboardButton('Afrikaans (África do Sul)', callback_data='afrikaans')
noruega = telebot.types.InlineKeyboardButton('Noruguês', callback_data='norwegian')

#Botoes direita e esquerda menu
right1 = telebot.types.InlineKeyboardButton('->', callback_data='right1')
left1 = telebot.types.InlineKeyboardButton('<-', callback_data='left1')
right2 = telebot.types.InlineKeyboardButton('->', callback_data='right2')
left2 = telebot.types.InlineKeyboardButton('<-', callback_data='left2')

#Botões /parental
responsavel = telebot.types.InlineKeyboardButton('Responsável', callback_data='responsavel')
dependente = telebot.types.InlineKeyboardButton('Dependente', callback_data='dependente')
cancelar = telebot.types.InlineKeyboardButton('Cancelar', callback_data='cancelar')

#Botões /parental cancelar
simP = telebot.types.InlineKeyboardButton('Sim', callback_data='simP')
naoP = telebot.types.InlineKeyboardButton('Não', callback_data='naoP')
