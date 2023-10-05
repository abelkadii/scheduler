from threading import Thread
from events import Event
import asyncio
from notification import notify
from utils import settings, threaded
import time
from date_time import DatetimeDecoder
from keyboard_listener import KeyboardListener


class Worker:
    def __init__(self):
        pass 

    @classmethod
    def run(self):
        with open(settings.get('paths').get('worker-state'), 'w') as f:
            f.write('RUNNING')
            f.close()

    @classmethod
    @threaded
    def worker(self):
        while self.check():
            self.scan()
            time.sleep(settings.get('worker-frq'))

        
    @classmethod
    @threaded
    def start(self, duration=None):
        self.run()
        self.worker()
        if duration:
            sleep(duration)
            self.stop()

    @classmethod
    def check(self):
        state = open(settings.get('paths').get('worker-state'), 'r').read()
        return state=='RUNNING'

    @classmethod
    def stop(self):
        with open(settings.get('paths').get('worker-state'), 'w') as f:
            f.write('STOPPED')
            f.close()
        

    @classmethod
    @threaded
    def notification(self, title, message, timeout):
        notify(title, message, timeout=timeout)

    @classmethod
    def scan(self):
        now = DatetimeDecoder.now()
        all_events = Event.all()
        for event in all_events:
            if event.status == 'soon':
                if (event.start_date+DatetimeDecoder.to_duration(event.snoozetime))>=now:
                    self.remind(event)
                continue
            if event.status == 'reminded':
                if event.start_date<=now:
                    self.notify(event)
                continue
            if event.status == 'pending':
                if event.end_date<=now:
                    self.passed(event)
                continue

        
    @classmethod
    @threaded
    def remind(self, event):
        time_left = DatetimeDecoder.time_until(event.start_date)
        timeout=settings.get('timeout').get('reminder')
        self.notification(title="in %s"%time_left, message=event.title, timeout=timeout)
        command = KeyboardListener.listen(timeout, ['cancel', 'snooze'])
        if command == 'cancel':
            event.status='cancel'
            event.save()
            timeout=settings.get('timeout').get('info')
            return self.notification(title='event id %s was canceled '%event.id, message=event.title, timeout=timeout)
        if command == 'snooze':
            event.snooze()
            timeout=settings.get('timeout').get('info')
            return self.notification(title='event id %s was snoozed to %s'%(event.id, DatetimeDecoder(event.start_date)), message=event.title, timeout=timeout)
        event.status = 'reminded'
        event.save()

    @classmethod
    @threaded
    def notify(self, event):
        timeout = settings.get('timeout').get('notification')
        self.notification(title="right now event id %s"%event.id, message=event.title, timeout=timeout)
        command = KeyboardListener.listen(timeout, ['cancel', 'snooze', 'done'])
        if command == 'cancel':
            event.status='cancel'
            event.save()
            timeout=settings.get('timeout').get('info')
            return self.notification(title='event id %s was canceled'%event.id, message=event.title, timeout=timeout)
        if command == 'snooze':
            event.snooze()
            timeout=settings.get('timeout').get('info')
            return self.notification(title='event id %s was snoozed to %s'%(event.id, DatetimeDecoder(event.start_date)), message=event.title, timeout=timeout)
        if command == 'snooze':
            event.status='done'
            event.save()
            timeout=settings.get('timeout').get('info')
            return self.notification(title='event id %s was set to done'%event.id, message=event.title, timeout=timeout)
        event.status = 'pending'
        event.save()

    @classmethod
    @threaded
    def passed(self, event):
        timeout = settings.get('timeout').get('passed')
        self.notification(title="event id %s has passed"%event.id, message=event.title, timeout=timeout)
        command = KeyboardListener.listen(timeout, ['done'])
        if command == 'snooze':
            event.status='done'
            event.save()
            timeout=settings.get('timeout').get('info')
            return self.notification(title='event id %s was set to done'%event.id, message=event.title, timeout=timeout)
        event.status = 'passed'
        event.save()
