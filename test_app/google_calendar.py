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

        tz = pytz.timezone(self.timezone)
        start_time = tz.localize(start_time)
        end_time = tz.localize(end_time)
        body = {
            "timeMin": start_time.isoformat(),
            "timeMax": end_time.isoformat(),
            "timeZone": self.timezone,
            "items": items
        }

        eventsResult = self.GC.service.freebusy().query(body=body).execute()
        cal_dict = eventsResult[u'calendars']

        #print(cal_dict)
        tmp = {}
        for m_id in m_id_list:
            tmp[m_id] = cal_dict[self.all_massager_calendar[m_id]]['busy']
        print(tmp)
        result = {}
        for key, value in tmp.items():
            tmp = set()
            for value2 in value:
                tmp.add(str_to_datetime(value2['start']))
            result[key] = tmp
        
        return result
        #result = {'master_id':{datetime set}}


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
        #print(event)
        return bool(event)

    # def get_free_time(self, start_time, end_time, group_id):
    #     g = MassagerGroup.objects.get(id = group_id)
    #     m_q = Massager.objects.filter(massagergroup = g)
    #     m_id_list = [m.m_name for m in m_q]
    #     starttime1 = datetime(2019, 9, 1, 9, 0)
    #     endtime2 = datetime(2019, 9, 7, 23, 59)
    #     #print(self.get_busy(starttime1, endtime2, *m_id_list))
    #     busy = self.get_busy(starttime1, endtime2, *m_id_list)
        
    #     return self.get_busy(starttime1, endtime2, *m_id_list)

    

# c = Customer.objects.get(id='2')
# print(c)

#CM = CalendarManager()
#CM.get_free_time(1, 2, 1)
# #result = CM.get_busy('m_A_12')
#starttime = datetime.fromisoformat('2019-09-03T08:00:00+08:06')
#starttime = datetime(2019, 9, 1, 7, 0)
#endtime = datetime.fromisoformat('2019-09-07T20:25:00+08:06')
#endtime = datetime(2019, 9, 7, 23, 59)#
#result = CM.get_busy(starttime, endtime, 'A001')
# result = CM.write_event('m_A_2', starttime, 'christest')
#print(result)
#result = CM.get_busy(starttime, endtime, 'm_A_12')
#print(result)
#for i in result['items']:
#    print(i['summary'], i['start'])
#print('end')
#get all massager calendar
# for i in all_massage_calendar:
#     result = service.events().list(calendarId=i['id'], timeZone="Asia/Taipei").execute()
#     print('----------------',i['summary'],'---------------------')
#     for event in result['items']:
#         print(event['summary'], event['start']['dateTime'])
#         #print(event)
