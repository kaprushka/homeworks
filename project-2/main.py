from flask import Flask
from flask import url_for, render_template, request, redirect
import json
import os.path

# Сервер
app = Flask(__name__)
# JSON с данными
json_filename = 'data/forms.json'

# Получение JSON строки
def get_json_data():
    if os.path.isfile(json_filename):
        with open(json_filename, "r", encoding='utf-8') as json_file:
            json_data = json_file.read()
            json_file.close()
    else:
        json_data = '{ "data": [] }'
    return json_data
	
# Получение массива из JSON
def get_json_array():
	return json.loads(get_json_data())

# Занести оъект в файл
def set_json(json_array):
    with open(json_filename, "w", encoding='utf-8') as json_file:
        json.dump(json_array, json_file, ensure_ascii = False, indent = 4)
        json_file.close()
	
@app.route('/')
def get_form():
    # Загрузка формы
    return render_template('form.html')

@app.route('/send', methods=['GET'])
def send_form():
    # Считывание имеющихся данных
    json_array = get_json_array()
    # Запись новых данных
    json_array['data'].append(request.args)
    set_json(json_array)
    # Ответ клиенту
    return render_template('success_load.html', name=request.args['fio'])

@app.route('/json')
def print_json():
    # Получение JSON со всеми данными
    return get_json_data()

@app.route('/stats')
def get_stats():
    # Вывод данных по шаблону stats
    return render_template('stats.html', forms=get_json_array()["data"])

@app.route('/search')
def get_search_form():
    # Загрузка формы
    return render_template('search.html')

@app.route('/find', methods=['GET'])
def find():
    # Считывание имеющихся данных
    json_array = get_json_array()
    # Поиск
    result = []
    for form in json_array["data"]:
        if form['fio'].find(request.args['fio']) != -1 and (request.args['age'] == '' or form['age'] == request.args['age']):
            result.append(form)
    # Ответ клиенту
    return render_template('result.html', forms=result)

# Запуск сервера
if __name__ == '__main__':
    app.run()
