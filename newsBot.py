'''
Бот
-Регистрация пользователя по идентификатору VK (telegram).
Работа с подписками:
-Просмотреть/добавить/удалить подписки на категории новостей.
-Просмотреть/добавить/удалить подписки на ключевые слова.
-Получение списка из 10 наиболее релевантных новостей по активным подпискам.
'''

import telebot, requests
#import sqlite3


botToken = "1700154841:AAEqEXDBhc4gZi02t4vttt6ZW5J6xKnYgPM"

carnolioId = "124023217"
categoryList = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

botHelp = """
    /addcat -   добавить категорию 
    /addkey -   добавить ключ  
    /delcat -   удалить категорию  
    /delkey -   удалить ключ  
    /getcat -   получить список ваших категорий
    /getcatlist -   получить список возможных категорий
    /getkey -   получить список ваших ключевых слов  
    /getnews -  получить 10 новостей в соответствии с набором 
                категория/ключ 
    /help -     это сообщение
    /start -    Зарегистрироваться, глянуть хелп если зарегистрирован
    """
#pip3 install PyTelegramBotAPI
#pip3 install newsapi-python

bot = telebot.TeleBot(botToken, parse_mode = None)
#bot = telebot.TeleBot(botToken)

#def regNewUser(message):
#    """ registration new user"""
#    userId = message.from_user.id
    #name = message.text
    #msg="Пользователь "+name+" зарегистрирован"
    #bot.send_message(message.from_user.id, msg, parse_mode=None)


@bot.message_handler(commands=['start'])
def startCommand(message):
    user_id = message.from_user.id
    data = {'user_id': user_id}
    print(f"до сюда старт доходит, дальше запрос к серверу {user_id}")
    r = requests.post(url='HTTP://localhost:8080/users/', data=data)
    print("че сервер вернул",r)
    bot.send_message(user_id, r.json(), parse_mode=None)

@bot.message_handler(commands=['help'])
def helpCommand(message):
    msg = bot.reply_to(message, botHelp, parse_mode=None)


@bot.message_handler(commands=['getcat'])
def getCatCommand(message):
    '''getcat'''
    user_id = message.from_user.id
    data = {'user_id': user_id}
    r = requests.get(url='HTTP://localhost:8080/subscriptions/categories/', data=data)
    print(' '.join(r.json()))
    bot.send_message(user_id, r.json(), parse_mode=None)

@bot.message_handler(commands=['getkey'])
def getKeyCommand(message):
    '''getkey'''
    user_id = message.from_user.id
    data = {'user_id': user_id}
    r = requests.get(url='HTTP://localhost:8080/subscriptions/keywords/', params=data)
    print(' '.join(r.json()))
    bot.send_message(user_id, r.json(), parse_mode=None)

@bot.message_handler(commands=['getcatlist'])
def getCatListCommand(message):
    '''getcatlist'''
    bot.send_message(message.from_user.id, '\n '.join(categoryList), parse_mode=None)




@bot.message_handler(commands=['addkey'])
def addKeycommand(message):
    '''add keywords to user'''
    user_id = message.from_user.id
    msg = message.text.split()
    data = {'user_id': user_id, 'message': msg}
    r = requests.post(url='HTTP://localhost:8080/subscriptions/keywords/', params=data)
    print(' '.join(r.json()))
    bot.send_message(user_id, r.json(), parse_mode=None)


@bot.message_handler(commands=['addcat'])
def addCatCommand(message):
    '''add categories to user'''
    user_id = message.from_user.id
    msg = list(message.text.split())
    msg = msg[1:]
    print("bot_add_cat",user_id,msg)
    data = {'user_id': user_id, 'message': msg}
    r = requests.post(url='HTTP://localhost:8080/subscriptions/categories/', params=data)
    #print(' '.join(r.json()))
    bot.send_message(user_id, r.json(), parse_mode=None)

@bot.message_handler(commands=['delcat'])
def delCatCommand(message):
    '''delcat'''
    user_id = message.from_user.id
    msg = message.text.split()

    data = {'user_id': user_id, 'message': msg}
    r = requests.delete(url='HTTP://localhost:8080/subscriptions/categories/', params=data)
    print(' '.join(r.json()))
    bot.send_message(user_id, r.json(), parse_mode=None)



@bot.message_handler(commands=['delkey'])
def delKeyCommand(message):
    '''delkey'''
    user_id = message.from_user.id
    data = {'user_id': user_id, 'message': message.text}
    r = requests.delete(url='HTTP://localhost:8080/subscriptions/keywords/', params=data)
    print(' '.join(r.json()))
    bot.send_message(user_id, r.json(), parse_mode=None)

def regNewUser(message):
    """ registration new user"""


@bot.message_handler(commands=['getnews'])
def getNewsCommand(message):
    pass

def check_server():
    pass

"""

Принимать параметры надо так
if request.method == 'POST':
        message = request.form.getlist('message')
        user_id = request.form['user_id']

а не так

if request.method == 'POST':
        user_id = request.args.get('user_id')
        message = request.args.get('message')
"""


check_server()
bot.polling()