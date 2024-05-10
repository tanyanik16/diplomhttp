from flask import Flask, render_template, request, jsonify
import requests
import pprint
from google.oauth2 import service_account
from googleapiclient.discovery import  build
import json
from datetime import datetime, timedelta
import Server

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
    url = 'http://localhost/InfoBase3/hs/wdoc1/note1'
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
    url = 'http://localhost/InfoBase3/hs/wdoc1/dd1'
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
    url = 'http://localhost/InfoBase3/hs/wdoc1/service1'
    username = 'bromuser'
    password = ''

    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        response_text = response.text
        service = json.loads(response_text)
        наименование_услуги = [item["Наименование"] for item in service]
        return наименование_услуги
    else:
        print("Ошибка2:", response.status_code)
        return None

def получить_данныесправочникСотрудники():
    url = 'http://localhost/InfoBase3/hs/wdoc1/master1'
    username = 'bromuser'
    password = ''

    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        response_text = response.text
        master = json.loads(response_text)
        наименование_сотрудники = [item["Наименование"] for item in master]
        return наименование_сотрудники
    else:
        print("Ошибка1:", response.status_code)
        return None

def получить_данные_документов():
    url = 'http://localhost/InfoBase3/hs/wdoc1/note1'
    username = 'bromuser'
    password = ''
    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        return response.json()

    else:
        print("Ошибка3:", response.status_code)
        return None
def получить_данные_документа_Запись():
    данные_документов = получить_данные_документов()
    if данные_документов is None:
        return None

    данные_запись = []

    for документ in данные_документов:
        данные_запись.append({
            "Дата": datetime.strptime(документ["Дата"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%dT%H:%M"),
            "Сотрудник": документ["Сотрудник"]

        })
    return данные_запись



def получитьзанятыедатаивремя():
    данные_документов = получить_данные_документов()

    if данные_документов is not None:
        for документ in данные_документов:

            занятые_дата_и_время = документ.get("Дата", "")# Получаем дату и время из JSON
            # Здесь можно выполнить дополнительные действия с датой и временем
            return занятые_дата_и_время
            print(дата_и_время)
    else:
        print("Не удалось получить данные о документах.")



# Функция для генерации всех временных слотов с 9:00 до 18:00 в заданном диапазоне дат
def generate_time_slots(start_date, end_date):
    time_slots = []
    current_date = start_date

    while current_date <= end_date:
        current_time = datetime(current_date.year, current_date.month, current_date.day, 9, 0)
        end_time = datetime(current_date.year, current_date.month, current_date.day, 18, 0)

        while current_time <= end_time:
            time_slots.append(current_time)
            current_time += timedelta(hours=1)

        current_date += timedelta(days=1)

    return time_slots

# Функция для отображения расписания
def display_schedule(time_slots, данные_документов):
    for time_slot in time_slots:
        found = False
        for документ in данные_документов:
            дата = datetime.strptime(документ["Дата"], "%Y-%m-%dT%H:%M:%SZ")
            if дата.hour == time_slot.hour and дата.minute == time_slot.minute:
                print(f'Время: {time_slot.strftime("%H:%M")}, Сотрудник: {документ["Сотрудник"]}')
                found = True
                break
        if not found:
            print(f'Время: {time_slot.strftime("%H:%M")}, Сотрудник: Нет записи')

def display_schedule2(time_slots, данные_документов):
    for time_slot in time_slots:
        found = False
        for документ in данные_документов:
            дата = datetime.strptime(документ["Дата"], "%Y-%m-%dT%H:%M")
            if дата.hour == time_slot.hour and дата.minute == time_slot.minute:
                print(f'Время: {time_slot.strftime("%H:%M")}, Сотрудник: {документ["Сотрудник"]}')
                found = True
                break
        if not found:
            print(f'Время: {time_slot.strftime("%H:%M")}, Сотрудник: Нет записи для {документ["Сотрудник"]}')

def filter_out_past_records(documents_data):

    if documents_data is None:
        return None

    current_time = datetime.now()
    filtered_data = []

    for document in documents_data:
        date_string = document.get("Дата", "")
        if date_string:
            date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M")
            if date >= current_time:
                filtered_data.append({
                    "Дата": date.strftime("%Y-%m-%dT%H:%M"),
                    "Сотрудник": document["Сотрудник"]
                })

    return filtered_data
#Авторизация
@app.route('/')
def author():

    return render_template('authorization.html')

#Регистрация
@app.route('/registr', methods=['GET', 'POST'])
def registr():
    if request.method == 'POST':
        username = request.form.get('fullname')
        password = request.form.get('password')
        # Здесь вы можете добавить код для сохранения данных пользователя в базу данных
        return f'Пользователь {username} успешно зарегистрирован!'
    return render_template('registr.html')

#Отмена записи
@app.route('/Cancel')
def Cancel():
    # Здесь вы можете добавить код для сохранения данных пользователя в базу данных

    данные = получить_данные_документа_Запись()
    if данные is None:
        return "Данные недоступны"
    return render_template('Cancel.html',данные=данные)

#Запись на услугу
@app.route('/index',methods=['GET','POST'])
def index():
    наименование_услуги = получить_данныесправочникУслуги()
    наименование_сотрудники = получить_данныесправочникСотрудники()
    занятые_дата_и_время=получить_данные_документа_Запись()


    render_data = {
        'services': наименование_услуги,
        'masters': наименование_сотрудники,
        'datatime':занятые_дата_и_время
    }

    # Возвращаем страницу регистрации с передачей данных
    if request.method == 'GET':
        return render_template('index.html', **render_data)

    # Получаем данные из формы
    услуга = request.form['input_text2']
    мастер = request.form['input_text1']
    клиент = request.form['input_text']
    датаИВремя = f"{request.form['select_date']}T{request.form['select_time']}"
    дата = f"{request.form['select_date']}T{request.form['select_time']}:00+03:00"
    датак = f"{request.form['select_date']}T{request.form['select_time']}:00+01:00"
    Телефон = request.form['input_phone']
    АдресЭП = request.form['email']
    ДатаРождения = f"{request.form['dob']}"

    #формирование расписания
    start_date = datetime(2024, 5, 10)  # Начальная дата
    end_date = datetime(2024, 5, 10)  # Конечная дата
    данные_запись1 = получить_данные_документа_Запись()

    time_slots = generate_time_slots(start_date, end_date)
    display_schedule2(time_slots, данные_запись1)

    #return render_template('index.html', display_schedule=display_schedule)


    # Формируем словарь данных
    data = {
        "Услуга": услуга,
        "Мастер": мастер,
        "Клиент": клиент,
        "ДатаИВремя": датаИВремя
    }
    datasp = {
        "Наименование": клиент,
        "Телефон": Телефон,
        "АдресЭП": АдресЭП,
        "ДатаРождения": ДатаРождения
    }

    # Проверка на существование документа в 1с
    данные_запись = получить_данные_документа_Запись()
    документ_найден = False
    for документ in данные_запись:
        if документ["Сотрудник"] == мастер and датаИВремя == документ["Дата"]:
            документ_найден = True
            break  # Прерываем цикл, если найден хотя бы один документ с указанным мастером
    if документ_найден:
        print("Документ существует!")
    else:

        print("Документ не существует!")
        результат = отправить_данные(data)
        результатsp = отправить_данныесправочник(datasp)

        # дОБАВЛЕНИЕ данных в гугл календарь
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
                'dateTime': датак

            }
        }
        event = obj.add_event(calendar_id=calendar, body=event)
        pprint.pp(obj.get_calendar_list())
        return jsonify(результатsp, результат)


    # Загружаем данные в перечисление услугу и мастера на сайт
    наименование_услуги = получить_данныесправочникУслуги()
    наименование_сотрудники = получить_данныесправочникСотрудники()
if __name__ == '__main__':
    app.run(debug=True)