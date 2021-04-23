from flask import Flask, jsonify, request
from newsapi import NewsApiClient
import sqlite3

"""
pip3 install flask
Сервер:
Предоставляет REST API для бота:
/users/ для регистрации пользователей.
/subscriptions/categories/ для получения/добавления/удаления подписок на категории.
/subscriptions/keywords/ для получения/добавления/удаления подписок на ключевые слова.
/news/ для получения списка новостей.
Взаимодействует с базой данных.
Взаимодействует с API https://newsapi.org/.
"""

app = Flask(__name__)

newsApiKey = ""
categoryList = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

def userExist(user_id):
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectUser = f"SELECT * FROM users WHERE ID = '{user_id}';"
        cursor.execute(sqlSelectUser)
        rows = cursor.fetchall()
        sqlConn.commit()
        cursor.close()
        if len(rows) > 0:
            # print(rows)
            return True
        else:
            return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()


def add_cat(user_id, message):
    # print('\n '.join(catForAdd))
    catForAdd = message
    msg = []
    # print(user_id, message)
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        for cat in catForAdd:
            # если категория из списка то добавляем
            # print(catForAdd[cat])
            if (cat in categoryList) and (catExist(cat, user_id) == False):
                sqlInsertCategory = f"INSERT INTO categories (name, user_id) VALUES ('{cat}', '{user_id}');"
                cursor = sqlConn.cursor()
                cursor.execute(sqlInsertCategory)
                sqlConn.commit()
                cursor.close()
                msg.append(cat + " добавлена")
            elif catExist(cat, user_id):
                msg.append(cat + " уже в вашем списке")
            else:
                msg.append(cat + " такой категории нет")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        msg = "Что-то пошло не так"
    finally:
        if sqlConn:
            sqlConn.close()
        # print(msg)
        return msg

def del_cat(user_id, message):
    catForDel = message
    # print('\n '.join(catForDel))
    msg = list()
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlDelCategory = "DELETE FROM categories where name = ? and user_id = ?;"
        for cat in range(len(catForDel)):
            # print(catForDel[cat])
            if catForDel[cat] in categoryList and catExist(catForDel[cat],user_id) == True:
                #print("jnjn")
                cursor = sqlConn.cursor()
                data_tuple = (catForDel[cat], user_id)
                cursor.execute(sqlDelCategory, data_tuple)
                sqlConn.commit()
                cursor.close()
                msg.append(catForDel[cat] + " удалена")
            else:
                msg.append(catForDel[cat] + " такой категории нет")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        msg.append("Что-то пошло не так")
    finally:
        if sqlConn:
            sqlConn.close()
    print(msg)
    return msg



def add_key(user_id, message):
    keyForAdd = message
    msg=list()
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlInsertKey = "INSERT INTO keywords (name, user_id) VALUES (?, ?);"
        for key in range(len(keyForAdd)):
            print("пытаемся добавить", keyForAdd[key])
            if keyExist(keyForAdd[key], user_id) == False:
                cursor = sqlConn.cursor()
                data_tuple = (keyForAdd[key], user_id)
                cursor.execute(sqlInsertKey, data_tuple)
                sqlConn.commit()
                cursor.close()
                msg.append(keyForAdd[key] + "- ключ добавлен")
            else:
                msg.append("Такой ключ уже есть")
    except sqlite3.Error as error:
        msg.append("Что-то пошло не так")
    finally:
        if sqlConn:
            sqlConn.close()
        return msg

def keyExist(key, user_id):
    rows = list()
    '''if key exist'''
    sqlConn = sqlite3.connect('newsBot.db')
    cursor = sqlConn.cursor()
    sqlSelectKeys = f"SELECT * FROM keywords WHERE user_id = '{user_id}' and name = '{key}'"
    cursor.execute(sqlSelectKeys)
    rows = cursor.fetchall()
    sqlConn.commit()
    cursor.close()
    if len(rows) > 0:
        return True
    else:
        return False


def catExist(cat, user_id):
    rows = list()
    '''if cat exist'''
    #print(cat, user_id)
    sqlConn = sqlite3.connect('newsBot.db')
    cursor = sqlConn.cursor()
    sqlSelectCats = f"SELECT name FROM categories WHERE user_id = '{user_id}' and name = '{cat}'"
    cursor.execute(sqlSelectCats)
    rows = cursor.fetchall()
    sqlConn.commit()
    cursor.close()
    if len(rows) > 0:
        return True
    else:
        return False


def init_db():
    """Подключение к БД и создание таблиц"""
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlCreateTableUsers = '''CREATE TABLE IF NOT EXISTS "users" (
                                 "id"	INTEGER NOT NULL,  PRIMARY KEY("id" AUTOINCREMENT));'''

        sqlCreateTableCategories = '''CREATE TABLE IF NOT EXISTS "categories" (
                                    "id"	INTEGER NOT NULL, "name" TEXT NOT NULL,
                                    "user_id"	INTEGER NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) );'''

        sqlCreateTableKeywords = '''CREATE TABLE IF NOT EXISTS "keywords" ("id"	INTEGER NOT NULL,
                                 "name"	TEXT NOT NULL, "user_id" INTEGER NOT NULL, PRIMARY KEY("id" AUTOINCREMENT));'''
        cursor = sqlConn.cursor()
        cursor.execute(sqlCreateTableUsers)
        cursor.execute(sqlCreateTableCategories)
        cursor.execute(sqlCreateTableKeywords)
        sqlConn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(error)

    finally:
        if (sqlConn):
            sqlConn.close()

def del_key(user_id, message):
    msg=list()
    keyForDel = message
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        for key in range(len(keyForDel)):
            if keyExist(keyForDel[key], user_id) == True:
                sqlDelKey = f"DELETE FROM keywords WHERE name = '{keyForDel[key]}' AND user_id = '{user_id}'"
                cursor = sqlConn.cursor()
                cursor.execute(sqlDelKey)
                sqlConn.commit()
                cursor.close()
                msg.append(keyForDel[key] + " ключ удален")
            else:
                msg.append(keyForDel[key] + " Такого ключа нет")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        msg.append("Что-то пошло не так")
    finally:
        if sqlConn:
            sqlConn.close()
        return msg

def add_user(user_id):
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        if userExist(user_id):
            msg = f"Пользователь {user_id} уже зарегистрирован"
            # print(f"Пользователь {user_id} уже зарегистрирован")
        else:
            cursor = sqlConn.cursor()
            sqlInsertNewUser = f"INSERT INTO users (id) VALUES ('{user_id}');"
            cursor.execute(sqlInsertNewUser)
            sqlConn.commit()
            cursor.close()
            msg = f"Пользователь {user_id} зарегистрирован"
            # print(f"Пользователь {user_id} зарегистрирован")
        return msg
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        msg = "Что-то пошло не так"
    finally:
       sqlConn.close()
    return msg


def get_key(user_id):
    listKeyword = []
    rows = []
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectKeys = f"SELECT name FROM keywords WHERE user_id = '{user_id}'"
        cursor.execute(sqlSelectKeys)
        rows = cursor.fetchall()
        sqlConn.commit()
        cursor.close()
    except sqlite3.Error as error:
        # print(error)
        msg = "Что-то пошло не так"
        return msg
    finally:
       if sqlConn:
           sqlConn.close()
    if len(rows) > 0:
        for item in rows:
            listKeyword.append(item[0])
    else:
        listKeyword.append("Нет ключевых слов")
    return listKeyword


@app.route('/users/', methods=['POST'])
def users():
    """users"""
    if request.method == 'POST':
        user_id = request.form['user_id']
        # print("/users",user_id)
        return jsonify(add_user(user_id))


def get_news(user_id):
    listKeywords = get_key(user_id)  # getKeyCommand(message,isPrint=False)
    listCategory = get_cat(user_id)  # (message,isPrint=False
    # print("lists_news",listKeywords,listCategory)
    if listCategory[0] == 'Нет подписок на категории':
        listCategory=[]
    if listKeywords[0] == 'Нет ключевых слов':
        listKeywords=[]

    listSources = []
    listNews = []
    msg = []

    newsapi = NewsApiClient(api_key=newsApiKey)
    # sources = newsapi.get_sources()
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
        msg = listNews
        print("artic",msg)
    else:
        msg.append("По такой выборке данных не найдено")
    return msg


def get_cat(user_id):
    '''getcat'''
    userCats = list()
    rows = list()
    print(user_id)
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectCats = f"SELECT name FROM categories WHERE user_id ='{user_id}'"
        cursor.execute(sqlSelectCats)
        rows = cursor.fetchall()
        print(rows)
        sqlConn.commit()
        cursor.close()
    except sqlite3.Error as error:
        msg = "Что-то пошло не так"
    finally:
        if sqlConn:
            sqlConn.close()
        if len(rows) > 0:
            print(rows)
            for item in rows:
                userCats.append(item[0])
        # если ничего не пришло
        else:
            userCats.append("Нет подписок на категории")
        return userCats


@app.route('/subscriptions/categories/', methods=['GET', 'POST', 'DELETE'])
def subscriptions_categories():
    # add_cat
    if request.method == 'POST':
        message = request.form.getlist('message')
        user_id = request.form['user_id']
        return jsonify(add_cat(user_id, message))
    # del_key
    elif request.method == 'DELETE':
        message = request.form.getlist('message')
        user_id = request.form['user_id']
        return jsonify(del_cat(user_id, message))
    # get_key
    elif request.method == 'GET':
        user_id = request.args.get('user_id')
        print("GET",user_id)
        return jsonify(get_cat(user_id))


@app.route('/subscriptions/keywords/', methods=['GET', 'POST', 'DELETE'])
def subscriptions_keywords():
    # add_key
    if request.method == 'POST':
        message = request.form.getlist('message')
        user_id = request.form['user_id']
        return jsonify(add_key(user_id, message))
    # del_key
    elif request.method == 'DELETE':
        message = request.form.getlist('message')
        user_id = request.form['user_id']
        return jsonify(del_key(user_id, message))
    # get_key
    elif request.method == 'GET':
        user_id = request.args.get('user_id')
        return jsonify(get_key(user_id))


@app.route('/news/', methods=['GET'])
def news():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        #print('/news/',user_id)
        return jsonify(get_news(user_id))


if __name__ == '__main__':
    init_db()

    app.run(host='localhost', port=8080)
