import datetime as dt
from utils import settings

class DatetimeDecoder:
    def __init__(self):
        pass

    @classmethod
    def now(self):
        return dt.datetime.now()
    

    @classmethod
    def time(self, string):
        splited = string.split(':')
        now = self.now()
        if len(splited)==1:
            try:
                hour = int(splited[0])
            except:
                raise Exception("invalid time")
            return now.replace(hour=hour, minute=0, second=0, microsecond=0)
        if len(splited)==2:
            try:
                hour = int(splited[0])
                minute = int(splited[1])
            except:
                raise Exception("invalid time")
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if len(splited)>3:
            raise 
        try:
            hour = int(splited[0])
            minute = int(splited[1])
            second = int(splited[2])
        except:
            raise Exception("invalid time")
        return now.replace(hour=hour, minute=minute, second=second, microsecond=0)        

    @classmethod
    def date(self, string):
        today = self.now().date()
        refrences = ['yesterday', 'today', 'tomorrow']
        if (cin:=string.lower()) in refrences:
            return today + dt.timedelta(refrences.index(cin)-1)
        weekdays = ['monday', 'tuesday', 'wedensday', 'thursday', 'friday','satuday', 'sunday']
        if cin in weekdays:
            return today + dt.timedelta(weekdays.index(cin)-today.weekday())
        splited = string.split('/')
        if len(splited)==1:
            try:
                day = int(splited[0])
            except:
                raise Exception("invalid date")
            return today.replace(day=day)
        if len(splited)==2:
            try:
                month = int(splited[0])
                day = int(splited[1])
            except:
                raise Exception("invalid date")
            return today.replace(day=day, month=month)
        if len(splited)>3:
            raise 
        try:
            month = int(splited[0])
            day = int(splited[1])
            if len(splited[2])==4:
                year = int(splited[2])
            else:
                if (y:=int(splited[2]))>70:
                    year = 1900+y
                else:
                    year=2000+y
        except:
            raise Exception("invalid date")
        return today.replace(day=day, month=month, year=year)

    @classmethod
    def datetime(self, string):
        if '@' not in string:
            if ':' in string:
                return dt.datetime.combine(dt.datetime.today(), decode_time(string).time())
            return decode_date(string)
            
        date, time = string.split('@')
        return dt.datetime.combine(self.date(date), self.time(time).time())

    @classmethod
    def parse(self, datetime):
        return datetime.strftime(settings.get('formats').get('datetime'))

    @classmethod
    def load(self, datetime):
        return dt.datetime.strptime(datetime, settings.get('formats').get('datetime'))

    @classmethod
    def duration(self, string):
        units = {'y': 'years', 'M': 'months', 'w': 'weeks', 'd': 'days', 'h': 'hours', 'm': 'minutes', 's': 'seconds'}
        days_units =  {'y': 365, 'M': 30, 'w': 7}
        delta = {
            'days': 0,
            'hours': 0,
            'minutes': 0,
            'seconds': 0
        }
        cur=""
        last_unit = None
        for c in string:
            if not 47<ord(c)<58:
                if not cur:
                    raise Exception('invalid duration expretion "%s"'%c)
                if c not in units:
                    raise Exception('unkown unit "%s"'%c)
                if c in days_units:
                    delta['days']+=days_units[c]*int(cur)
                else:
                    delta[units[c]]+=int(cur)
                last_unit=c
                cur=""
            else:
                cur+=c
        if cur:
            if not last_unit:
                raise Exception('unit not provided for "%s"'%cur)
            index = list(units.keys()).index(last_unit)
            if index==len(units)-1:
                Exception('unit not provided for "%s"'%cur)
            c = list(units.keys())[index+1]
            if c in days_units:
                delta['days']+=days_units[c]*int(cur)
            else:
                delta[units[c]]+=int(cur)
        return dt.timedelta(**delta)


    @classmethod
    def to_duration(self, seconds):
        return dt.timedelta(seconds=seconds)
    
    @classmethod
    def duration_to_seconds(self, string):
        return self.duration(duration).total_seconds()
    
    @classmethod
    def time_until(self, time):
        time_left = (time-self.now()).total_seconds()
        mapper = {'seconds':60, 'minutes':60, 'hours':24, 'days':30, 'months': 12, 'years': 10, 'decades': 10, 'centuries': 10, 'melenia': 10}        
        cur_unit = 'now'
        for unit in mapper:
            if time_left>mapper[unit]:
                cur_unit = unit
                time_left/=mapper[unit]
                continue
            break
        return str(round(time_left)) + ' ' + unit