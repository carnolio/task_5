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
Для проверки текущего пользователя можно использовать его telegram(vk) id.
PS. для получения/добавления/удаления используйте HTTP глаголы.

"""


app = Flask(__name__)
botToken = "1700154841:AAEqEXDBhc4gZi02t4vttt6ZW5J6xKnYgPM"
newsApiKey = "7e40013ca7ea498589545453e4cea074"
carnolioId = "124023217"
categoryList = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

# message.from_user.id

# print('\n '.join(keyForAdd))

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
            #print(rows)
            return True
        else:
            return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()


def add_cat(user_id, message):
    catForAdd = message[1:]
    # print('\n '.join(catForAdd))
    msg = []
    print(user_id, message)
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        for cat in range(len(catForAdd)):
            #если категория из списка то добавляем
            #print(catForAdd[cat])
            if (catForAdd[cat] in categoryList) and (catExist(catForAdd[cat], user_id) == False):
                sqlInsertCategory = f"INSERT INTO categories (name, user_id) VALUES ('{catForAdd[cat]}', '{user_id}');"
                cursor = sqlConn.cursor()
                cursor.execute(sqlInsertCategory)
                sqlConn.commit()
                cursor.close()
                msg.append(catForAdd[cat] + " добавлена")
            elif catExist(catForAdd[cat],user_id):
                msg.append(catForAdd[cat] + " уже в вашем списке")
            else:
                msg.append(catForAdd[cat] + " такой категории нет")

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()
    print("222 ", msg)
    return msg

def del_cat(user_id, message):
    catForDel = message.text.split()
    #print('\n '.join(catForDel))

    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlDelCategory = "DELETE FROM categories where name = ? and user_id = ?;"
        for cat in range(1,len(catForDel)):
            #print(catForDel[cat])
            #if catForDel[cat] in categoryList and catForDel[cat] != "/delcat" and catExist(catForDel[cat],message.from_user.id) == True:
            if catForDel[cat] in categoryList and catForDel[cat] != "/delcat" :
                cursor = sqlConn.cursor()
                data_tuple = (catForDel[cat], message.from_user.id)
                cursor.execute(sqlDelCategory, data_tuple)
                sqlConn.commit()
                cursor.close()
                msg = catForDel[cat] + " удалена"
            else:
                msg = catForDel[cat] + " такой категории нет"
            #bot.send_message(message.from_user.id, msg, parse_mode=None)
            return jsonify(msg)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()



def add_key(user_id, message):
    keyForAdd = message.text.split()
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlInsertKey = "INSERT INTO keywords (name, user_id) VALUES (?, ?);"
        for key in range(1, len(keyForAdd)):
            # print("пытаемся добавить", keyForAdd[key])

            if keyForAdd[key] != "/addkey" and keyExist(keyForAdd[key], user_id) == False:
                cursor = sqlConn.cursor()
                data_tuple = (keyForAdd[key], user_id)
                cursor.execute(sqlInsertKey, data_tuple)
                sqlConn.commit()
                cursor.close()
                msg = keyForAdd[key] + "- ключ добавлен"
            else:
                msg = "Такой ключ уже есть"
            #bot.send_message(message.from_user.id, msg, parse_mode=None)
            return jsonify(msg)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()


def keyExist(key,user_id):
    rows = list()
    '''if key exist'''
    sqlConn = sqlite3.connect('newsBot.db')
    cursor = sqlConn.cursor()
    sqlSelectKeys = f"SELECT * FROM keywords WHERE user_id = '{user_id}' and name = '{key}'"
    cursor.execute(sqlSelectKeys)
    #print(cursor.execute(sqlSelectKeys, data_tuple))
    rows = cursor.fetchall()
    sqlConn.commit()
    cursor.close()
    if len(rows) > 0:
        return True
    else:
        return False

def catExist(cat,user_id):
    rows = list()
    '''if key exist'''
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

def del_key(user_id,message):
    #print('\n '.join(keyForDel))
    keyForDel = message.text.split()

    try:
        sqlConn = sqlite3.connect('newsBot.db')

        for key in range(1,len(keyForDel)):
            #if keyForDel[key] != "/delkey" and keyExist(keyForDel[key], message.from_user.id) == True:
            if keyForDel[key] != "/delkey":
                sqlDelKey = f"DELETE FROM keywords WHERE name = '{keyForDel[key]}' AND user_id = '{user_id}'"
                cursor = sqlConn.cursor()
                #data_tuple = (keyForDel[key], message.from_user.id)
                #cursor.execute(sqlDelKey, data_tuple)
                cursor.execute(sqlDelKey)
                sqlConn.commit()
                cursor.close()
                msg = keyForDel[key] + " ключ удален"
            else:
                msg = keyForDel[key] + " Такого ключа нет"
            #bot.send_message(message.from_user.id, msg, parse_mode=None)
            return jsonify(msg)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
        return jsonify(error)
    finally:
        if sqlConn:
            sqlConn.close()


def add_user(user_id):
    try:
        if userExist(user_id):
            msg = f"Пользователь {user_id} уже зарегистрирован"
            print(f"Пользователь {user_id} уже зарегистрирован")
        else:
            sqlConn = sqlite3.connect('newsBot.db')
            cursor = sqlConn.cursor()
            sqlInsertNewUser = f"INSERT INTO users (id) VALUES ('{user_id}');"
            cursor.execute(sqlInsertNewUser)
            sqlConn.commit()
            cursor.close()
            msg = f"Пользователь {user_id} зарегистрирован"
            print(f"Пользователь {user_id} зарегистрирован")
        return jsonify(msg)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()


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
        print(error)
    finally:
        if sqlConn:
            sqlConn.close()
        if len(rows) > 0:
            for item in rows:
                listKeyword.append(item[0])
            #if isPrint:
            #    bot.send_message(message.from_user.id, '\n '.join(listKeyword), parse_mode=None)
        else:
            #bot.send_message(message.from_user.id, "Нет ключевых слов", parse_mode=None)
            listKeyword.append("Нет ключевых слов")
        return listKeyword





@app.route('/users/', methods=['GET','POST','DELETE'])
def users():
    """users"""
    if request.method == 'POST':
        user_id = request.form['user_id']
        #print("/users",user_id)
        return jsonify(add_user(user_id))

def get_news(user_id):
    listKeywords = get_key(user_id)#getKeyCommand(message,isPrint=False)
    listCategory = get_cat(user_id)#(message,isPrint=False)
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
        #bot.send_message(message.from_user.id, "По такой выборке данных не найдено")
        msg = "По такой выборке данных не найдено"
        return jsonify(msg)

    for i in range(len(listNews)):
        title = listNews[i]["title"]
        description = listNews[i]["description"]
        url = listNews[i]["url"]
        publishedAt = listNews[i]["publishedAt"]
        msg = f"{title}\n\n{description}\n{url}\n{publishedAt}"
        #bot.send_message(message.from_user.id, f"{title}\n\n{description}\n{url}\n{publishedAt}",disable_web_page_preview=True)
        return jsonify(msg)


def get_cat(user_id):
    '''getcat'''
    userCats = list()
    rows = list()
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectCats = f"SELECT name FROM categories WHERE user_id = '{user_id}'"
        cursor.execute(sqlSelectCats)
        rows = cursor.fetchall()
        sqlConn.commit()
        cursor.close()
    except sqlite3.Error as error:
        print(error)
    finally:
        if sqlConn:
            sqlConn.close()

        if len(rows) > 0:
            #print(rows)
            for item in rows:
                userCats.append(item[0])
        #если ничего не пришло
        else:
            userCats.append("Нет подписок на категории")
        return userCats




@app.route('/subscriptions/categories/', methods=['GET','POST','DELETE'])
def subscriptions_categories():
    # add_cat
    if request.method == 'POST':
        message = request.form.getlist('message')
        user_id = request.form['user_id']
        return jsonify(add_cat(user_id, message))
    #del_key
    elif request.method == 'DELETE':
        message = request.form.getlist('message')
        user_id = request.form['user_id']
        return jsonify(del_cat(user_id, message))
    #get_key
    elif request.method == 'GET':
        user_id= request.args.get('user_id')
        return jsonify(get_cat(user_id))



@app.route('/subscriptions/keywords/', methods=['GET','POST','DELETE'])
def subscriptions_keywords():
    #add_key
    if request.method == 'POST':
        message = request.form.getlist('message')
        user_id = request.form['user_id']
        return jsonify(add_key(user_id, message))
    #del_key
    elif request.method == 'DELETE':
        user_id = request.args.get('user_id')
        message = request.args.get('message')
        return jsonify(del_key(user_id, message))
    #get_key
    elif request.method == 'GET':
        user_id= request.args.get('user_id')
        return jsonify(get_key(user_id))

@app.route('/news/', methods=['GET','POST','DELETE'])
def news():
    pass


"""
@app.route('/rest', methods=['GET'])
def rest():
    user = {"name":"nick", 'email':'example.com', 'tel':['+790853535','+783294892384']}
    return jsonify(user)

@app.route('/calc', methods=['GET','POST'])
def calc():
    if request.method == 'GET':
        return render_template('calc.html')
    if request.method == 'POST':
        a = float(request.form.get('number_one'))
        b = float(request.form.get('number_two'))
        if request.form['calc'] == 'Сумма':
            c = a + b
        if request.form['calc'] == 'Разность':
            c = a - b
        return render_template('calc.html', c=c)
"""

if __name__ == '__main__':
    init_db()
    app.run(host='localhost', port=8080)
