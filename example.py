
#server
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

#client
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
