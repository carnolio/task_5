from flask import Flask, jsonify, request

"""
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
@app.route('/users', methods=['GET','POST'])

@app.route('/subscriptions/categories/', methods=['GET','POST','DELETE'])

@app.route('/subscriptions/keywords/', methods=['GET','POST','DELETE'])

@app.route('/news/', methods=['GET','POST','DELETE'])

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
    app.run(host='0.0.0.0', port=80