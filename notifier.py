from app import App, Command, Arg
from commands import Commands
from date_time import DatetimeDecoder

class Log:
    log=print

notifier = App('Notifer', provider=input, root="abelkadii@event$~ ")
notifier.setLogger(Log())

notifier.register(Command('create', ['create', 'add'], [
    Arg("_type", ['type']),
    Arg("title", ['title', 't'], required=True),
    Arg("message", ['message', 'm']),
    Arg("start_date", ['start_date', 'sd', 'start'], decode=DatetimeDecoder.datetime, required=True),
    Arg("duration", ['duration', 'd'], decode=DatetimeDecoder.duration),
    Arg("end_date", ['end_date'], decode=DatetimeDecoder.datetime),
    Arg("notification", ['notification', 'nt'], decode=int),
    Arg("snoozetime", ['snoozetime', 'snooze', 'st'], decode=int)
], Commands.create))

notifier.register(Command('ls', ['ls', 'list'], [
    Arg("type", ['type']),
    Arg("title", ['title', 't']),
    Arg("message", ['message', 'm']),
    Arg("start_date", ['start_date', 'sd', 'start'], decode=DatetimeDecoder.datetime),
    Arg("end_date", ['end_date', 'ed', 'end'], decode=DatetimeDecoder.datetime),
], Commands.ls))

notifier.register(Command('snooze', ['snooze'], [Arg("id", ['id', 0], required=True)], Commands.snooze))
notifier.register(Command('cancel', ['cancel'], [Arg("id", ['id', 0], required=True)], Commands.cancel))
notifier.register(Command('finish', ['finish'], [Arg("id", ['id', 0], required=True)], Commands.finish))
notifier.register(Command('get', ['get'], [Arg("id", ['id', 0], required=True)], Commands.get))
notifier.register(Command('delete', ['delete'], [Arg("id", ['id', 0], required=True)], Commands.delete))

notifier.register(Command('delay', ['delay'], [
    Arg("id", ['id', 0], required=True),
    Arg("to", keys=['to'], decode=DatetimeDecoder.datetime),
    Arg("by", keys=['by'], decode=DatetimeDecoder.duration),
    ], Commands.delay))


notifier.register(Command('rush', ['rush'], [
    Arg("id", ['id', 0], required=True),
    Arg("to", keys=['to'], decode=DatetimeDecoder.datetime),
    Arg("by", keys=['by'], decode=DatetimeDecoder.duration),
    Arg("_in", keys=['in'], decode=DatetimeDecoder.duration),
    ], Commands.rush))

notifier.register(Command('update', ['update', 'change'], [
    Arg("id", ['id', 0], required=True),
    Arg("type", ['type']),
    Arg("title", ['title', 't']),
    Arg("message", ['message', 'm']),
    Arg("start_date", ['start_date', 'sd', 'start'], decode=DatetimeDecoder.datetime),
    Arg("end_date", ['end_date', 'ed', 'end'], decode=DatetimeDecoder.datetime),
    Arg("notification", ['notification', 'nt'], decode=int),
    Arg("snoozetime", ['snoozetime', 'st'], decode=int),
    Arg("status", ['status'])

], Commands.update))

# worker commands
notifier.register(Command('start', ['start'], [
    Arg('duration', ['duration', 'd'], decode=DatetimeDecoder.duration_to_seconds)
], Commands.start))

notifier.register(Command('check', ['check'], [], Commands.check))
notifier.register(Command('stop', ['stop'], [], Commands.stop))
notifier.register(Command('exit', ['exit'], [], Commands.exit))
notifier.register(Command('clear', ['clear', 'cls'], [], Commands.clear))