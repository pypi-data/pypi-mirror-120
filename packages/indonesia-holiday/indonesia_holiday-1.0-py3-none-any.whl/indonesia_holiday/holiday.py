import datetime
from googleapiclient.discovery import build
from pytz import timezone


class IndonesiaHoliday:
    def __init__(self, developer_key=None, calendar_id='id.indonesian#holiday@group.v.calendar.google.com'):
        self.service = build('calendar', 'v3', developerKey=developer_key)
        self.event = set([])
        self.date = datetime.datetime.now(timezone("Asia/Jakarta"))
        self.calendar_id = calendar_id
        self.data = self.get_event_list()

    def get_event_list(self, time_min='', time_max=''):
        page_token = None
        epoch_year = datetime.datetime.now().year
        year_range = self.year_range(epoch_year, datetime.datetime)
        if not time_min:
            time_min = year_range[0].astimezone().replace(microsecond=0).isoformat()
        if not time_max:
            time_max = year_range[1].astimezone().replace(microsecond=0).isoformat()
        while True:
            events = self.service.events().list(
                calendarId=self.calendar_id, timeMin=time_min, timeMax=time_max, maxResults=100, pageToken=page_token
            ).execute()
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return events

    def get_event_detail(self, event_id=''):
        if not event_id:
            raise ValueError("Please provide event_id")
        if not isinstance(event_id, str):
            raise TypeError("event_id must be string")

        return self.service.events().get(calendarId=self.calendar_id, eventId=event_id).execute()

    def year_range(self, year, datetime_o=datetime.date):
        return (
            datetime_o.min.replace(year=year),
            datetime_o.max.replace(year=year)
        )

    def set_timezone(self, tz):
        self.date = datetime.datetime.now(timezone(tz))
        return self.date

    def check(self):
        check = (self.is_saturday(), self.is_sunday(), self.is_holiday())
        return True in check

    def is_sunday(self):
        now = self.date
        day = now.strftime("%A")
        if day != "Sunday":
            return False
        self.event.add("sunday")
        return True

    def is_saturday(self):
        now = self.date
        day = now.strftime("%A")
        if day != "Saturday":
            return False
        self.event.add("saturday")
        return True

    def is_holiday(self):
        try:
            d = self.date
            next_day = d + datetime.timedelta(days=1)
            events = self.get_event_list(time_min=self.date.astimezone().replace(microsecond=0).isoformat(), time_max=next_day.astimezone().replace(microsecond=0).isoformat())
            if events:
                for item in events['items']:
                    self.event.add(item['summary'])
                return True
            return False
        except KeyError:
            return False

    def set_date(self, y, m, d):
        self.date = datetime.datetime(int(y), int(m), int(d), 0, 0)
        return self.date

    def get_event(self):
        return list(self.event)


if __name__ == "__main__":
    # pass main
    pass
