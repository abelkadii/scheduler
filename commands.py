from events import Event
from console import *
from date_time import DatetimeDecoder
from worker import Worker
import os

class Commands:
    def __init__(self):
        pass

    @classmethod
    def ls(self, **params):
        return Table([e.to_dict() for e in Event.filter(**params)], log_length=True)

    @classmethod
    def create(self, **kwargs):
        event = Event.new(**kwargs)
        return Obj(event.to_dict(), msg='successfully created new event id %s'%event.id)

    @classmethod
    def cancel(self, id):
        event = Event.get(id)
        event.status='canceled'
        event.save()
        return Success('successfully canceled event id %s'%id)

    @classmethod
    def finish(self, id):
        event = Event.get(id)
        event.status='done'
        event.save()
        return Success('successfully finished event id %s'%id)

    @classmethod
    def get(self, id):
        return Obj(Event.get(id).to_dict())


    @classmethod
    def delete(self, id):
        event = Event.get(id)
        event.delete()
        return Success('successfully deleted event id %s'%id)

    @classmethod
    def delay(self, id, by=None, to=None):
        event = Event.get(id)
        if to and to < event.start_date:
            raise Error("can't delay backwards")
        if not by:
            by = to-event.start_date
        event.start_date+=by
        event.end_date+=by
        event.save()
        return Success('successfully delayed event id %s'%id)


    @classmethod
    def snooze(self, id):
        Event.get('id').snooze()
        return Success('successfully canceled event id %s'%id)

    @classmethod
    def rush(self, id, _in=None, to=None, by=None):
        event = Event.get(id)
        if to and to > event.start_date:
            raise Error("can't rush forwards")
        if _in:
            by = event.start_date-(DatetimeDecoder.now()+_in)
        if to:
            by = event.start_date-to
        
        event.start_date-=by
        event.end_date-=by
        event.save()
        return Success('successfully rushed event id %s'%id)

    @classmethod
    def update(self, id, **kwargs):
        event = Event.get(id)
        for key, value in kwargs.items():
            if hasattr(event, key):
                setattr(event, key, value)
        event.save()
        return Obj(event.to_dict(), msg='successfully updated event id %s'%id)


    @classmethod
    def start(self, duration=None):
        if Worker.check():
            return Warn('worker is already running')
        Worker.start(duration)
        return Success('successfully started worker')

    @classmethod
    def check(self):
        opened = Worker.check()
        if opened:
            return Success('worker is running')
        return Success('worker is stopped')



    @classmethod
    def stop(self):
        if not Worker.check():
            return Warn('worker is already stopped')
        Worker.stop()
        return Success('successfully stopped worker')

    # command line commands
    @classmethod
    def exit(self):
        raise Exit()

    @classmethod
    def clear(self):
        return os.system('cls')