from flask import Flask, render_template, request, jsonify
import requests
import pprint
from google.oauth2 import service_account
from googleapiclient.discovery import  build
import json
from datetime import datetime

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

def получить_данныесправочникУслуги():
    url = 'http://localhost/salon/hs/wdoc/service'
    username = 'bromuser'
    password = ''

    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        response_text = response.text
        service = json.loads(response_text)
        наименование_услуги = [item["Наименование"] for item in service]
        return наименование_услуги
    else:
        print("Ошибка:", response.status_code)
        return None

def получить_данныесправочникСотрудники():
    url = 'http://localhost/salon/hs/wdoc/master'
    username = 'bromuser'
    password = ''

    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        response_text = response.text
        master = json.loads(response_text)
        наименование_сотрудники = [item["Наименование"] for item in master]
        return наименование_сотрудники
    else:
        print("Ошибка:", response.status_code)
        return None

def получить_данныедокументЗаписьДата():
    url = 'http://localhost/salon/hs/wdoc/note'
    username = 'bromuser'
    password = ''
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        дата_запись = [item["Дата"] for item in data]
        return дата_запись

    else:
        print("Ошибка1:", response.status_code)
        return None

def получить_данныедокументЗаписьСотрудник():
    url = 'http://localhost/salon/hs/wdoc/note'
    username = 'bromuser'
    password = ''
    response = requests.get(url, auth=(username, password))
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        сотрудник_запись=[item["Сотрудник"] for item in data]
        return сотрудник_запись
    else:
        print("Ошибка:", response.status_code)
        return None

#РАБОТА С WEB-САЙТОМ
@app.route('/')
def index():
    наименование_услуги = получить_данныесправочникУслуги()
    наименование_сотрудники=получить_данныесправочникСотрудники()
    return render_template('index.html',services=наименование_услуги, masters=наименование_сотрудники)

@app.route('/submit', methods=['POST'])
def submit():
    # Получаем данные из формы
    услуга = request.form['input_text2']
    мастер = request.form['input_text1']
    клиент = request.form['input_text']
    датаИВремя = f"{request.form['select_date']}T{request.form['select_time']}"
    дата=f"{request.form['select_date']}T{request.form['select_time']}:00+03:00"
    датак = f"{request.form['select_date']}T{request.form['select_time']}:00+01:00"
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

    #Проверка если документ сущшествует на текущую дату и время выводит сообщение в консоль об этом
    дата1=получить_данныедокументЗаписьДата()
    сотрудник=получить_данныедокументЗаписьСотрудник()
    датаИсотрудникпреобраз=[datetime.strptime(дата, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M") for дата in дата1]



    print(датаИсотрудникпреобраз)
    print(сотрудник)
    print(мастер)

    if датаИВремя in датаИсотрудникпреобраз and мастер not in сотрудник:
        print(f"Документ на  не существует1.{датаИВремя}{датаИсотрудникпреобраз}{мастер}{сотрудник}")
        результат = отправить_данные(data)
        результатsp = отправить_данныесправочник(datasp)
        return jsonify(результат)
        return jsonify(результатsp)
    elif датаИВремя not in датаИсотрудникпреобраз and мастер in сотрудник:
        print(f"Документ на текущую дату и время не существует2.{датаИВремя}{датаИсотрудникпреобраз}{мастер}{сотрудник}")
        результат = отправить_данные(data)
        результатsp = отправить_данныесправочник(datasp)
        return jsonify(результат)
        return jsonify(результатsp)
    elif датаИВремя not in датаИсотрудникпреобраз and мастер not in сотрудник:
        print(f"Документ на текущую дату и время не существует3.{датаИВремя}{датаИсотрудникпреобраз}{мастер}{сотрудник}")
        результат = отправить_данные(data)
        результатsp = отправить_данныесправочник(datasp)
        return jsonify(результат)
        return jsonify(результатsp)
    elif датаИВремя in датаИсотрудникпреобраз and мастер  in сотрудник:
        print('hdsjd')
        return jsonify({"message": "Мастер ззанят на данную дату и время ."})

    # if датаИВремя in датаИсотрудникпреобраз:
    #     print("Документ на текущую дату и время уже существует.")
    # else:
    #     print("Документ на текущую дату и время не существует.")
    #     результат = отправить_данные(data)
    #     результатsp = отправить_данныесправочник(datasp)

    print("Отправляемые данные:", data)

    наименование_услуги = получить_данныесправочникУслуги()
    наименование_сотрудники = получить_данныесправочникСотрудники()
    # Отправляем данные в виде JSON

    #дОБАВЛЕНИЕ данных в гугл календарь
    # obj = GoogleCalendar()
    # calendar = 'tanya.nikiforova2002@gmail.com'
    # event = {
    #     'summary': услуга,
    #     'location': 'Москва',
    #     'description': 'nn',
    #     'start': {
    #         'dateTime': дата
    #
    #     },
    #     'end': {
    #         'dateTime': датак
    #
    #     }
    # }
    # event= obj.add_event(calendar_id=calendar, body=event)
    # pprint.pp(obj.get_calendar_list())



if __name__ == '__main__':
    app.run(debug=True)