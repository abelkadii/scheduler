import os, json, random
from threading import Thread


def random_id():
    return chr(random.randint(65, 90))+chr(random.randint(48, 57))+chr(random.randint(48, 57))

cwd = os.path.dirname(__file__)
settings = json.load(open("static/config.json", 'r'))
for key in settings['paths']:
    settings['paths'][key]=os.path.join(cwd, settings['paths'][key])

raw_settings=json.load(open("static/config.json", 'r'))

def write_settings(settings):
    json.dump(settings, open("static/config.json", 'w'), indent=4)

def threaded(f):
    def wrapper(*args, **kwargs):
        thread=Thread(target=f, args=args, kwargs=kwargs)
        thread.start()
    return wrapper
