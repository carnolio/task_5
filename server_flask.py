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

"""
Сервер
@app.route('/categories', methods=['GET', 'POST', 'DELETE'])
def categories_rest():
    if request.method == 'POST':
        # add_keywords()
        name = request.form.getlist('name')
        user_id = request.form['user_id']
        query = {"user_id": user_id, "name": name}
        # print(query)
        return jsonify(add_categories(query))
    elif request.method == 'DELETE':
        name = request.form.getlist('name')
        user_id = request.form['user_id']
        query = {"user_id": user_id, "name": name}
        return jsonify(del_categories(query))
    else:
        user_id = request.args.get('user_id')
        return jsonify(show_categories(user_id))

Клиент:
def show_categories(query):
    '''Получение категорий'''
    user_id = query['user_id']
    data = {'user_id': user_id}
    r = requests.get(url=api_url_categories, params=data)
    print(' '.join(r.json()))
    return r.json()


def add_categories(query):
    '''Добавление категорий'''
    user_id = query['user_id']
    options = query['options']
    data = {'user_id': user_id, 'name': options}
    r = requests.post(url=api_url_categories, data=data)
    success = r.json()['success']
    fail = r.json()['fail']
    fail_invalid = r.json()['fail_invalid']
    if len(success):
        bot.send_message(user_id, f'Вы успешно подписались на категории: {" ".join(success)}')
    if len(fail):
        bot.send_message(user_id, f'Вы уже подписаны на категории: {" ".join(fail)}')
    if len(fail_invalid):
        bot.send_message(user_id, f'Недопустимое значение категории: {" ".join(fail)}. Загляни в /help')


def del_categories(query):
    '''Удаление категорий'''
    user_id = query['user_id']
    options = query['options']
    data = {'user_id': user_id, 'name': options}
    r = requests.delete(url=api_url_categories, data=data)
    success = r.json()['success']
    fail = r.json()['fail']
    if len(success):
        bot.send_message(user_id, f'Вы успешно удалили подписку на категории: {" ".join(success)}')
    if len(fail):
        bot.send_message(user_id, f'Вы не подписаны на категории: {" ".join(fail)}')
        
"""

app = Flask(__name__)
botToken = "1700154841:AAEqEXDBhc4gZi02t4vttt6ZW5J6xKnYgPM"
newsApiKey = "7e40013ca7ea498589545453e4cea074"
carnolioId = "124023217"
categoryList = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']


def get_user_category(message, isPrint=True):
    '''getcat'''
    userCats = list()
    rows = list()
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectCats = f"SELECT name FROM categories WHERE user_id = {message.from_user.id}"
        #data_tuple = (,)
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
                #print(item[0])
                userCats.append(item[0])
                if isPrint:
                    #bot.send_message(message.from_user.id, item[0], parse_mode=None)
                    return message.from_user.id, item[0]
                return userCats
        else:
            return jsonify(message.from_user.id, "Нет подписок на категории")
            #bot.send_message(message.from_user.id, "Нет подписок на категории", parse_mode=None)

def initDB():
    """Подключение к БД и создание таблиц"""
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        sqlCreateTableUsers = '''CREATE TABLE IF NOT EXISTS "users" (
                                 "id"	INTEGER NOT NULL, "name" TEXT NOT NULL, PRIMARY KEY("id" AUTOINCREMENT));'''

        sqlCreateTableCategories = '''CREATE TABLE IF NOT EXISTS "categories" (
                                    "id"	INTEGER NOT NULL, "name" TEXT NOT NULL,
                                    "user_id"	INTEGER NOT NULL, PRIMARY KEY("id" AUTOINCREMENT) );'''

        sqlCreateTableKeywords = '''CREATE TABLE IF NOT EXISTS "keywords" ("id"	INTEGER NOT NULL,
                                 "name"	TEXT NOT NULL, "user_id" INTEGER NOT NULL, PRIMARY KEY("id" AUTOINCREMENT));'''
        cursor = sqlConn.cursor()
        cursor.execute(sqlCreateTableUsers)
        sqlConn.commit()
        cursor.execute(sqlCreateTableCategories)
        sqlConn.commit()
        cursor.execute(sqlCreateTableKeywords)
        sqlConn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print(error)

    finally:
        if (sqlConn):
            sqlConn.close()

@app.route('/users', methods=['GET','POST'])
def users(userID,name):
    """ registration new user"""
    #userId = message.from_user.id
    #name = message.text
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlInsertNewUser = f"INSERT INTO users (id, name) VALUES ({userID}, {name});"
        cursor.execute(sqlInsertNewUser)
        sqlConn.commit()
        cursor.close()
        msg = "Пользователь " + name + " зарегистрирован"
        #bot.send_message(message.from_user.id, msg, parse_mode=None)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlConn:
            sqlConn.close()

@app.route('/subscriptions/categories/', methods=['GET','POST','DELETE'])
def subscriptions_categories(message, isPrint = True):
    '''getcat'''
    userCats = list()
    rows = list()
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectCats = f"SELECT name FROM categories WHERE user_id = {message.from_user.id}"
        #data_tuple = (message.from_user.id,)
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
                #print(item[0])
                userCats.append(item[0])
                if isPrint:
                    #bot.send_message(message.from_user.id, '\n '.join(userCats), parse_mode=None)
                    return jsonify(message.from_user.id, '\n '.join(userCats))
                return jsonify(userCats)
        else:
            #bot.send_message(message.from_user.id, "Нет подписок на категории", parse_mode=None)
            return jsonify(message.from_user.id, "Нет подписок на категории")

@app.route('/subscriptions/keywords/', methods=['GET','POST','DELETE'])
def subscriptions_keywords(message, isPrint=True):
#    def getKeyCommand(message, isPrint=True):
    '''getkey'''
    listKeyword = []
    rows = []
    try:
        sqlConn = sqlite3.connect('newsBot.db')
        cursor = sqlConn.cursor()
        sqlSelectKeys = """SELECT name FROM keywords WHERE user_id = ?"""
        data_tuple = (message.from_user.id,)
        cursor.execute(sqlSelectKeys, data_tuple)
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
            if isPrint:
                #bot.send_message(message.from_user.id, '\n '.join(listKeyword), parse_mode=None)
                return jsonify(message.from_user.id, '\n '.join(listKeyword))
            return listKeyword
        else:
            #bot.send_message(message.from_user.id, "Нет ключевых слов", parse_mode=None)
            return jsonify(message.from_user.id, "Нет ключевых слов")
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
    app.run(host='0.0.0.0', port=8080)
