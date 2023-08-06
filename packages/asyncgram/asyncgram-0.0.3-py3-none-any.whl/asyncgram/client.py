import os
import queue
import dotenv
import logging
import requests
import threading
from time import sleep

dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-9s) %(message)s')

class Asyncgram:
    def __init__(self, tg_token: str, tg_group: str, poll_interval: float = 0.1, daemon: bool = True):
        self.TG_TOKEN = tg_token
        self.TG_GROUP = tg_group
        self.TG_URL = f"https://api.telegram.org/bot{self.TG_TOKEN}/sendMessage"
        self.POLL_INTERVAL = poll_interval
        self.daemon = daemon
        self.queue = queue.Queue()
        self.__prepare_thread()

    def __prepare_thread(self):
        self.session = requests.Session()
        self.running = True
        self.stopped = False
        self.thread = threading.Thread(target=self.__alerter, daemon=self.daemon)

    def __alerter(self):
        while self.running or not self.queue.empty():
            if not self.queue.empty():
                try:
                    data = self.queue.get()
                except Exception as e:
                    logging.error("Error while trying to get item from producer queue")
                try:
                    self.session.post(self.TG_URL, data)
                except:
                    logging.error("Error while trying to send message to telegram")
            sleep(self.POLL_INTERVAL)
        self.stopped = True

    def put(self, item: str, group: str = None):
        if group is None:
            self.queue.put({'chat_id': str(self.TG_GROUP), "text": item})
        else:
            self.queue.put({'chat_id': str(group), "text": item})

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False
        while not self.stopped: sleep(0.1) 
        self.thread.join()