from pynput import keyboard
import asyncio
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from utils import settings

from pynput import keyboard


class KeyboardListener:
    def __init__(self):
        pass

    @classmethod
    def lis(self, timeout, listen_for):
        loop = asyncio.new_event_loop()
        future = loop.create_future()
        def cancel():
            if not future.done():
                future.set_result('cancel')

        def snooze():
            if not future.done():
                future.set_result('snooze')

        def done():
            if not future.done():
                future.set_result('done')

        funcs = {
            "cancel": cancel,
            "snooze": snooze,
            "done": done
        }
        listener = keyboard.GlobalHotKeys({settings.get('keyboard-hotkeys').get(item): funcs[item] for item in listen_for})
        listener.start()

        sleep(timeout)
        
        if not future.done():
            future.set_result(None)
        return future.result()
    
    @classmethod
    def listen(self, timeout, listen_for):
        with ThreadPoolExecutor() as exe:
            future = exe.submit(self.lis, timeout, listen_for)
            return future.result()
        