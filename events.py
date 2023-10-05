from utils import *
from date_time import DatetimeDecoder

class Event:
    def __init__(self, _id, _type, title, message, start_date, end_date, notification, snoozetime, status):
        self.id = _id
        self.type = _type
        self.title = title
        self.message = message
        self.start_date = start_date
        self.end_date = end_date
        self.notification = notification
        self.snoozetime = snoozetime
        self.status = status

    @classmethod
    def new(self, _type=None, title=None, message=None, start_date=None, duration=None, end_date=None, notification=None, snoozetime=None, status=None):
        """
        this method is used to create a new event
        """
        if title is None:
            raise Exception('title not provided')
        if start_date is None:
            raise Exception('start_date not provided')
        if end_date is None and duration is None:
            raise Exception('either end_date or duration has to be provided')
        
        _id = self.generate_id()
        _type = _type or "event"
        message = message or ""
        end_date = end_date or start_date+duration
        notification = notification or settings.get('default-notification-time')
        snoozetime = snoozetime or settings.get('default-snooze-time')
        status = status or 'soon'
        
        new_event = Event(_id, _type, title, message, start_date, end_date, notification, snoozetime, status)
        new_event.save()
        return new_event

    

    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'start_date': DatetimeDecoder.parse(self.start_date),
            'end_date': DatetimeDecoder.parse(self.end_date),
            'notification': self.notification,
            'snoozetime': self.snoozetime,
            'status': self.status,
        }
    @classmethod
    def from_dict(self, obj):
        return Event(**obj)


    @classmethod
    def write(self, events):
        return Data.json_write([event.to_dict() for event in events], settings.get('paths').get('data'))

    def save(self):
        all_events = self.all()
        for i, event in enumerate(all_events):
            if event.id == self.id:
                all_events[i]=self
                return self.write(all_events)
        all_events.append(self)
        return self.write(all_events)

    @classmethod
    def generate_id(self):
        # generating a unique new id
        all_ids = [e.id for e in self.all()]
        while (rnd:=random_id()) in all_ids:
            continue
        return rnd
    
    @classmethod
    def all(self):
        return [self.from_dict(event) for event in Data.json_read(settings.get('paths').get('data'))]
    
    @classmethod
    def get(self, id):
        all_events = self.all()
        for event in all_events:
            if event.id==id:
                return event
        raise Exception('404, no event with id="%s"'%id)
    
    
    def delete(self):
        all_events = self.all()
        for i, event in enumerate(all_events):
            if event.id == self.id:
                all_events.pop(i)
                return self.write(all_events)
        raise Exception('404, no event with id="%s"'%id)

    
    @classmethod
    def filter(self, **kwargs):
        all_events = self.all()
        if not kwargs:
            return all_events
        filtered=[]
        for event in all_events:
            if any([event.__getattribute__(key)!=kwargs[key] for key in kwargs]):
                continue
            filtered.append(event)
        return self.range(kwargs.get('start_date'), kwargs.get('end_date'), filtered)
    
    @classmethod
    def range(start=None, end=None, events=None):
        all_events = events or self.all()
        if not start and not end:
            return all_events
        filtered = []
        for event in events:
            if (not start or event.start_date>=start or event.end_date>=start) and (not end or event.end_date<=end or event.start_date<=end):
                filtered.append(event)
        return sorted(filtered, key=lambda i:i.start_date)
    
    @classmethod
    def snooze(self):
        self.start_date+=DatetimeDecoder.in_duration(self.snoozetime)
        self.end_date+=DatetimeDecoder.in_duration(self.snoozetime)
        self.status = 'soon'
        self.save()
        
class Data:
    def __init__(self):
        pass
    
    @classmethod
    def json_read(self, path):
        return json.load(open(path, 'r'))

    @classmethod
    def json_write(self, data, path):
        return json.dump(data, open(path, 'w'), indent=4)