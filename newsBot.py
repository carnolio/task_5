'''
Бот
-Регистрация пользователя по идентификатору VK (telegram).
Работа с подписками:
-Просмотреть/добавить/удалить подписки на категории новостей.
-Просмотреть/добавить/удалить подписки на ключевые слова.
-Получение списка из 10 наиболее релевантных новостей по активным подпискам.
'''

import sqlite3, telebot, requests
from newsapi import NewsApiClient

botToken = "1700154841:AAEqEXDBhc4gZi02t4vttt6ZW5J6xKnYgPM"
newsApiKey = "7e40013ca7ea498589545453e4cea074"
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

def regNewUser(message):
    """ registration new user"""
    userId = message.from_user.id
    name = message.text
    msg="Пользователь "+name+" зарегистрирован"
    bot.send_message(message.from_user.id, msg, parse_mode=None)

@bot.message_handler(commands=['start'])
def startCommand(message):
    #print(userExist(message))
    if userExist(message) == False:
        #bot.send_message(message.from_user.id, "Введите ваше имя:", parse_mode=None)
        msg = bot.reply_to(message, "Введите Ваше имя")
        bot.register_next_step_handler(msg, regNewUser)
    else:
        bot.send_message(message.from_user.id, botHelp, parse_mode=None)

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
    bot.send_message(message.from_user.id, r.json(), parse_mode=None)

@bot.message_handler(commands=['getcatlist'])
def getCatListCommand(message):
    '''getcatlist'''
    bot.send_message(message.from_user.id, '\n '.join(categoryList), parse_mode=None)

@bot.message_handler(commands=['getkey'])
def getKeyCommand(message):
    '''getkey'''
    user_id = message.from_user.id
    data = {'user_id': user_id}
    r = requests.get(url='HTTP://localhost:8080/subscriptions/keywords/', params=data)
    print(' '.join(r.json()))
    bot.send_message(user_id, r.json(), parse_mode=None)









@bot.message_handler(commands=['addkey'])
def addKeycommand(message):
    '''add keywords to user'''
    # message.from_user.id
    keyForAdd = message.text.split()
    #print('\n '.join(keyForAdd))

    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlInsertKey = "INSERT INTO keywords (name, user_id) VALUES (?, ?);"
        for key in range(1,len(keyForAdd)):
            #print("пытаемся добавить", keyForAdd[key])


            if keyForAdd[key] != "/addkey" and keyExist(keyForAdd[key], message.from_user.id) == False:
                cursor = sqlConn.cursor()
                data_tuple = (keyForAdd[key], message.from_user.id)
                cursor.execute(sqlInsertKey, data_tuple)
                sqlConn.commit()
                cursor.close()
                msg = keyForAdd[key] + "- ключ добавлен"
            else:
                msg = "Такой ключ уже есть"
            bot.send_message(message.from_user.id, msg, parse_mode=None)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()

@bot.message_handler(commands=['addcat'])
def addCatCommand(message):
    '''add categories to user'''
    catForAdd = message.text.split()
    #print('\n '.join(catForAdd))

    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlInsertCategory = "INSERT INTO categories (name, user_id) VALUES (?, ?);"
        for cat in range(1,len(catForAdd)):
            #если категория из списка то добавляем
            #print(catForAdd[cat])
            if catForAdd[cat] in categoryList and catForAdd[cat] != "/addcat" and catExist(catForAdd[cat],message.from_user.id) == False:
                cursor = sqlConn.cursor()
                data_tuple = (catForAdd[cat], message.from_user.id)
                cursor.execute(sqlInsertCategory, data_tuple)
                sqlConn.commit()
                cursor.close()
                msg = catForAdd[cat] + " добавлена"
            elif catExist(catForAdd[cat],message.from_user.id):
                msg = catForAdd[cat] + " уже в вашем списке"
            else:
                msg = catForAdd[cat] + " такой категории нет"
            bot.send_message(message.from_user.id, msg, parse_mode=None)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()

@bot.message_handler(commands=['delcat'])
def delCatCommand(message):
    '''delcat'''
    catForDel = message.text.split()
    #print('\n '.join(catForDel))

    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlDelCategory = "DELETE FROM categories where name = ? and user_id = ?;"
        for cat in range(1,len(catForDel)):
            #print(catForDel[cat])
            if catForDel[cat] in categoryList and catForDel[cat] != "/delcat" and catExist(catForDel[cat],message.from_user.id) == True:
                cursor = sqlConn.cursor()
                data_tuple = (catForDel[cat], message.from_user.id)
                cursor.execute(sqlDelCategory, data_tuple)
                sqlConn.commit()
                cursor.close()
                msg = catForDel[cat] + " удалена"
            else:
                msg = catForDel[cat] + " такой категории нет"
            bot.send_message(message.from_user.id, msg, parse_mode=None)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()


@bot.message_handler(commands=['delkey'])
def delKeyCommand(message):
    '''delkey'''
    keyForDel = message.text.split()
    #print('\n '.join(keyForDel))

    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlDelKey = """DELETE FROM keywords WHERE name = ? AND user_id = ?"""
        for key in range(1,len(keyForDel)):
            if keyForDel[key] != "/delkey" and keyExist(keyForDel[key], message.from_user.id) == True:
                cursor = sqlConn.cursor()
                data_tuple = (keyForDel[key], message.from_user.id)
                cursor.execute(sqlDelKey, data_tuple)
                sqlConn.commit()
                cursor.close()
                msg = keyForDel[key] + " ключ удален"
            else:
                msg = keyForDel[key] + " Такого ключа нет"
            bot.send_message(message.from_user.id, msg, parse_mode=None)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()


def userExist(message):
    userId = message.from_user.id
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectUser = """SELECT * FROM users WHERE ID = ?;"""
        params = (userId,)
        cursor.execute(sqlSelectUser, params)
        rows = cursor.fetchall()
        sqlConn.commit()
        cursor.close()
        if len(rows) > 0:
            #print(rows)
            return True
        else:
            return False

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()


def regNewUser(message):
    """ registration new user"""
    userId = message.from_user.id
    name = message.text
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlInsertNewUser = """INSERT INTO users (id, name) VALUES (?, ?);"""
        params = (userId, name)
        cursor.execute(sqlInsertNewUser, params)
        sqlConn.commit()
        cursor.close()
        msg="Пользователь "+name+" зарегистрирован"
        bot.send_message(message.from_user.id, msg, parse_mode=None)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()





@bot.message_handler(commands=['getnews'])
def getNewsCommand(message):
    listKeywords = getKeyCommand(message,isPrint=False)
    listCategory = getCatCommand(message,isPrint=False)
    listSources = []
    listNews = []

    newsapi = NewsApiClient(api_key=newsApiKey)
    #sources = newsapi.get_sources()
    if len(listCategory) > 0:
        for category in listCategory:
            sources = newsapi.get_sources(category=category)
            for source in sources['sources']:
                listSources.append(source['id'])
        response = newsapi.get_everything(q=' OR '.join(listKeywords), sources=','.join(listSources),
                                          sort_by='relevancy', page_size=10)
    elif len(listKeywords) > 0:
        response = newsapi.get_everything(q=' OR '.join(listKeywords), sort_by='relevancy', page_size=10)
    else:
        response = {"articles": []}

    if len(response["articles"]) < 10:
        count_news = len(response["articles"])
    else:
        count_news = 10
    if len(response["articles"]) > 0:
        for i in range(count_news):
            listNews.append({
                "title": response["articles"][i]["title"],
                "description": response["articles"][i]["description"],
                "url": response["articles"][i]["url"],
                "publishedAt": response["articles"][i]["publishedAt"],
            })
    #return listNews
    else:
        bot.send_message(message.from_user.id, "По такой выборке данных не найдено")

    for i in range(len(listNews)):
        title = listNews[i]["title"]
        description = listNews[i]["description"]
        url = listNews[i]["url"]
        publishedAt = listNews[i]["publishedAt"]
        bot.send_message(message.from_user.id,
                         f"{title}\n\n{description}\n{url}\n{publishedAt}",disable_web_page_preview=True)
def check_server():
    pass


check_server()
bot.polling()