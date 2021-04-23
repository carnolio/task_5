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


botToken = ""
categoryList = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

botHelp = """
    /addcat -   добавить категорию, можно несколько через пробел
    /addkey -   добавить ключ, можно несколько через пробел  
    /delcat -   удалить категорию, можно несколько через пробел  
    /delkey -   удалить ключ, можно несколько через пробел  
    /getcat -   получить список ваших категорий
    /getcatlist -   получить список возможных категорий
    /getkey -   получить список ваших ключевых слов  
    /getnews -  получить 10 новостей в соответствии с набором 
                категория/ключ 
    /help -     это сообщение
    /start -    Зарегистрироваться
    """
#pip3 install PyTelegramBotAPI
#pip3 install newsapi-python

bot = telebot.TeleBot(botToken, parse_mode = None)



@bot.message_handler(commands=['start'])
def startCommand(message):
    user_id = message.from_user.id
    data = {'user_id': user_id}
    # print(f"до сюда старт доходит, дальше запрос к серверу {user_id}")
    r = requests.post(url='HTTP://localhost:8080/users/', data=data)
    # print("че сервер вернул",r)
    bot.send_message(user_id, r.json(), parse_mode=None)
    helpCommand(message)

@bot.message_handler(commands=['help'])
def helpCommand(message):
    msg = bot.reply_to(message, botHelp, parse_mode=None)


@bot.message_handler(commands=['getcat'])
def getCatCommand(message):
    '''getcat'''
    user_id = message.from_user.id
    data = {'user_id': user_id}
    r = requests.get(url='HTTP://localhost:8080/subscriptions/categories/', params=data)
    print(' '.join(r.json()))
    bot.send_message(user_id, '\n'.join(r.json()), parse_mode=None)

@bot.message_handler(commands=['getkey'])
def getKeyCommand(message):
    '''getkey'''
    user_id = message.from_user.id
    data = {'user_id': user_id}
    r = requests.get(url='HTTP://localhost:8080/subscriptions/keywords/', params=data)
    bot.send_message(user_id, '\n'.join(r.json()), parse_mode=None)

@bot.message_handler(commands=['getcatlist'])
def getCatListCommand(message):
    '''getcatlist'''
    bot.send_message(message.from_user.id, '\n '.join(categoryList), parse_mode=None)

@bot.message_handler(commands=['addkey'])
def addKeycommand(message):
    '''add keywords to user'''
    user_id = message.from_user.id
    msg = list(message.text.split())
    print(msg)
    msg = msg[1:]
    if len(msg)==0:
        bot.send_message(user_id, 'Пустая команда', parse_mode=None)
    else:
        data = {'user_id': user_id, 'message': msg}
        r = requests.post(url='HTTP://localhost:8080/subscriptions/keywords/', data=data)
        bot.send_message(user_id, '\n'.join(r.json()), parse_mode=None)

@bot.message_handler(commands=['addcat'])
def addCatCommand(message):
    '''add categories to user'''
    user_id = message.from_user.id
    msg = list(message.text.split())
    msg = msg[1:]
    if len(msg)==0:
        bot.send_message(user_id, 'Пустая команда', parse_mode=None)
    else:
        print("bot_add_cat",user_id,msg)
        data = {'user_id': user_id, 'message': msg}
        r = requests.post(url='HTTP://localhost:8080/subscriptions/categories/', data=data)
        #print(' '.join(r.json()))
        bot.send_message(user_id, '\n'.join(r.json()), parse_mode=None)

@bot.message_handler(commands=['delcat'])
def delCatCommand(message):
    '''delcat'''
    msg = list(message.text.split())
    msg = msg[1:]
    user_id = message.from_user.id
    if len(msg)==0:
        bot.send_message(user_id, 'Пустая команда', parse_mode=None)
    else:
        data = {'user_id': user_id, 'message': msg}
        r = requests.delete(url='HTTP://localhost:8080/subscriptions/categories/', data=data)
        bot.send_message(user_id, '\n'.join(r.json()), parse_mode=None)

@bot.message_handler(commands=['delkey'])
def delKeyCommand(message):
    '''delkey'''
    user_id = message.from_user.id
    msg = list(message.text.split())
    msg = msg[1:]
    if len(msg)==0:
        bot.send_message(user_id, 'Пустая команда', parse_mode=None)
    else:
        data = {'user_id': user_id, 'message': msg}
        r = requests.delete(url='HTTP://localhost:8080/subscriptions/keywords/', data=data)
        bot.send_message(user_id, '\n'.join(r.json()), parse_mode=None)

@bot.message_handler(commands=['getnews'])
def getNewsCommand(message):
    '''get news'''
    user_id = message.from_user.id
    data = {'user_id': user_id}
    r = requests.get(url='HTTP://localhost:8080/news/', params=data)
    listNews=r.json()
    print(listNews)
    if listNews[0] == 'По такой выборке данных не найдено':
        bot.send_message(user_id, f"По такой выборке данных не найдено", disable_web_page_preview=True)
    else:
        for i in range(len(listNews)):
            title = listNews[i]["title"]
            description = listNews[i]["description"]
            url = listNews[i]["url"]
            publishedAt = listNews[i]["publishedAt"]
            #msg.append( f"{title}\n\n{description}\n{url}\n{publishedAt}")
            bot.send_message(user_id, f"{title}\n\n{description}\n{url}\n{publishedAt}",disable_web_page_preview=True)
    #print("print msgnews", msg)

def check_server():
    pass

check_server()
bot.polling()