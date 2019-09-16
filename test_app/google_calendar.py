import pickle
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import re
from datetime import timedelta, datetime
import pytz
#from test_app.models import Reservation, Customer, Master, MasterGroup

CREDENTIALSFILE = './test_app/token.pkl'


def datetime_to_str(date_time):
    return date_time.isoformat()

def str_to_datetime(datetime_str):
    return datetime.fromisoformat(datetime_str)

class GoogleCalendar():
    def __init__(self):
        self.credentials = pickle.load(open(CREDENTIALSFILE, "rb"))
        self.service = build("calendar", "v3", credentials=self.credentials)
        self.calendar_name_regex = re.compile(r'[A-Z][0-9]+')

    def get_all_massager_calendar(self):
        result = self.service.calendarList().list().execute()

        all_massager_calendar = {}
        for i in result['items']:
            if self.calendar_name_regex.match(i['summary']):
                all_massager_calendar[i['summary'][0:4]] = i['id']
        return all_massager_calendar


class CalendarManager():
    def __init__(self):
        self.GC = GoogleCalendar()
        self.all_massager_calendar = self.GC.get_all_massager_calendar()
        self.timezone = 'Asia/Taipei'
        self.event_delta = timedelta(hours=1, minutes=59)
    

    def get_busy(self, start_time, end_time, *m_id_list):
        items = list()
        for m_id in m_id_list:
            items.append({"id": self.all_massager_calendar[m_id]})

        body = {
            "timeMin": start_time.isoformat(),
            "timeMax": end_time.isoformat(),
            "timeZone": self.timezone,
            "items": items
        }

        eventsResult = self.GC.service.freebusy().query(body=body).execute()
        cal_dict = eventsResult[u'calendars']

        tmp = {}
        for m_id in m_id_list:
            tmp[m_id] = cal_dict[self.all_massager_calendar[m_id]]['busy']

        result = {}
        for key, value in tmp.items():
            tmp = set()
            for item in value:
                start_time = str_to_datetime(item['start'])
                end_time = str_to_datetime(item['end'])
                time_interval = timedelta(hours=1)
                while start_time < end_time:                    
                    tmp.add(start_time)
                    start_time += time_interval                    
            result[key] = tmp

        return result


    def write_event(self, m_id, start_time, summary):
        calendar_id = self.all_massager_calendar[m_id]
        end_time = start_time + self.event_delta

        timezone = self.timezone
        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
        }

        event = self.GC.service.events().insert(calendarId=calendar_id, body=event).execute()

        return event
    

    def delete_event(self, m_id, event_id):
        calendar_id = self.all_massager_calendar[m_id]
        result = self.GC.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return result

    def insert_calendar(self, summary):
        calendar = {
            'summary': summary,
            'timeZone': self.timezone
        }
        created_calendar = self.GC.service.calendars().insert(body=calendar).execute()
        print(created_calendar['id'], '----', summary)
        

#for test
#CM = CalendarManager()
# starttime = datetime(2019, 9, 1, 7, 0)
# endtime = datetime(2019, 9, 7, 23, 59)#
# result = CM.get_busy(starttime, endtime, 'A001')
#result = CM.delete_event('A001', 'b8qogs6mbj4cqn8fuec9vcb50s')
#print(result)
