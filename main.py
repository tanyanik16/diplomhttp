# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests

url = 'http://localhost/webdemo11/hs/wdoc/note'
data = {
    "Услуга": "ывыыв",
    "Мастер": "Халитова Ангелина",
    "Клиент": "Никифорова Людмиоа",
    "ДатаИВремя": "2024-02-25T23:48:00"
}

username = 'bromuser'
password = ''

response = requests.post(url, json=data, auth=(username, password))

print(response.content.decode('utf-8'))