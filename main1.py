from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


def отправить_данные(data):
    url = 'http://localhost/salon/hs/wdoc/note'
    username = 'bromuser'
    password = ''

    try:
        response = requests.post(url, json=data, auth=(username, password))
        response.raise_for_status()  # Генерировать исключение при ошибке HTTP
        print("Код состояния HTTP ответа:", response.status_code)
        print("Ответ от сервера:", response.content.decode('utf-8'))
        return response.json()  # Возвращаем JSON ответ от сервера
    except requests.exceptions.RequestException as e:
        print('Ошибка при отправке запроса:', e)
        return {'error': 'Ошибка при отправке запроса'}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Получаем данные из формы
    услуга = request.form['input_text2']
    мастер = request.form['input_text1']
    клиент = request.form['input_text']
    датаИВремя = f"{request.form['select_date']}T{request.form['select_time']}"

    # Формируем словарь данных
    data = {
        "Услуга": услуга,
        "Мастер": мастер,
        "Клиент": клиент,
        "ДатаИВремя": датаИВремя
    }
    print(data)
    print("Отправляемые данные:", data)
    результат = отправить_данные(data)
    # Отправляем данные в виде JSON
    return jsonify(результат)


if __name__ == '__main__':
    app.run(debug=True)