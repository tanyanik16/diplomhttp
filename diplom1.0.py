from flask import Flask, render_template, request, jsonify
import requests
import pprint
from google.oauth2 import service_account
from googleapiclient.discovery import  build


app = Flask(__name__)

#РАБОТА С ГУГЛ КАЛЕНДАРЕМ
class GoogleCalendar:
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    FILE_PATN='plan-413713-746340edf6c0.json'
    def __init__(self):
        credentials=service_account.Credentials.from_service_account_file(
            filename=self.FILE_PATN, scopes=self.SCOPES
        )
        self.service=build('calendar','v3',credentials=credentials)
    def get_calendar_list(self):
        return self.service.calendarList().list().execute()
    def add_calendar(self, calendar_id):
        calendar_list_entry={
            'id':calendar_id
        }
        return self.service.calendarList().insert(
            body=calendar_list_entry).execute()
    def add_event(self,calendar_id,body):
        return self.service.events().insert(
            calendarId=calendar_id,
            body=body).execute()


#РАБОТА С 1С
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

def отправить_данныесправочник(datasp):
    url = 'http://localhost/salon/hs/wdoc/dd'
    username = 'bromuser'
    password = ''

    try:
        response = requests.post(url, json=datasp, auth=(username, password))
        response.raise_for_status()  # Генерировать исключение при ошибке HTTP
        print("Код состояния HTTP ответа:", response.status_code)
        print("Ответ от сервера:", response.content.decode('utf-8'))
        return response.json()  # Возвращаем JSON ответ от сервера
    except requests.exceptions.RequestException as e:
        print('Ошибка при отправке запроса:', e)
        return {'error': 'Ошибка при отправке запроса'}

#РАБОТА С WEB-САЙТОМ
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
    дата=f"{request.form['select_date']}T{request.form['select_time']}:00+03:00"
    Телефон=request.form['input_phone']
    АдресЭП=request.form['email']
    ДатаРождения=f"{request.form['dob']}"
    # Формируем словарь данных
    data = {
        "Услуга": услуга,
        "Мастер": мастер,
        "Клиент": клиент,
        "ДатаИВремя": датаИВремя
    }
    datasp={
        "Наименование": клиент,
        "Телефон": Телефон,
        "АдресЭП": АдресЭП,
        "ДатаРождения": ДатаРождения
    }
    print("Отправляемые данные:", data)
    результат = отправить_данные(data)
    результатsp = отправить_данныесправочник(datasp)
    # Отправляем данные в виде JSON

    #дОБАВЛЕНИЕ данных в гугл календарь
    obj = GoogleCalendar()
    calendar = 'tanya.nikiforova2002@gmail.com'

    event = {
        'summary': услуга,
        'location': 'Москва',
        'description': 'nn',
        'start': {
            'dateTime': дата

        },
        'end': {
            'dateTime': дата

        }
    }
    event= obj.add_event(calendar_id=calendar, body=event)
    pprint.pp(obj.get_calendar_list())

    return jsonify(результат)
    return jsonify(результатsp)

if __name__ == '__main__':
    app.run(debug=True)