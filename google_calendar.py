import pprint

from google.oauth2 import service_account
from googleapiclient.discovery import  build
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



obj=GoogleCalendar()

calendar='tanya.nikiforova2002@gmail.com'

event={
    'summary':'nn',
    'location': 'Москва',
    'description': 'nn',
    'start': {
        'date':'2024-02-08',
    },
    'end': {
        'date': '2024-02-10',
    }
}

event=obj.add_event(calendar_id=calendar, body=event)
pprint.pp(obj.get_calendar_list())