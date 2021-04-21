from flask import Flask, jsonify, request
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

def keyExist(key,user_id):
    rows = list()
    '''if key exist'''
    sqlConn = sqlite3.connect('newsBot.db')
    cursor = sqlConn.cursor()
    sqlSelectKeys = f"SELECT * FROM keywords WHERE user_id = {user_id} and name = {key}"
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
    sqlSelectCats = f"SELECT name FROM categories WHERE user_id = {user_id} and name = {cat}"
    cursor.execute(sqlSelectCats)
    rows = cursor.fetchall()
    sqlConn.commit()
    cursor.close()
    #print(rows)
    if len(rows) > 0:
        #print("cat exist",rows)
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

def get_key(user_id):
    listKeyword = []
    rows = []
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectKeys = f"SELECT name FROM keywords WHERE user_id = {user_id}"
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





@app.route('/users', methods=['GET','POST'])
def users(user_id):
    pass

def get_cat(user_id):
    '''getcat'''
    userCats = list()
    rows = list()
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectCats = f"SELECT name FROM categories WHERE user_id = {user_id}"
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
    #add_cat
    if request.method == 'POST':
        pass
    #del_cat
    elif request.method == 'DELETE':
        pass
    #get_cat
    elif request.method == 'GET':
        user_id= request.args.get('user_id')
        return jsonify(get_cat(user_id))



@app.route('/subscriptions/keywords/', methods=['GET','POST','DELETE'])
def subscriptions_keywords():
    #add_cat
    if request.method == 'POST':
        pass
    #del_cat
    elif request.method == 'DELETE':
        pass
    #get_cat
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
