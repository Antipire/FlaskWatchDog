import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from multiprocessing import Process
import configparser
import logging

# Настройка логирования
logging.basicConfig(filename='daemon.log', level=logging.INFO, format='%(asctime)s - %(message)s')


class Watcher:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.directory_to_watch = config['Directories']['directory_to_watch']
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            logging.info("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            logging.info(f"Received created event - {event.src_path}")
        elif event.event_type == 'modified':
            logging.info(f"Received modified event - {event.src_path}")
        elif event.event_type == 'deleted':
            logging.info(f"Received deleted event - {event.src_path}")


if __name__ == '__main__':
    w = Watcher()
    flask_process = Process(target=os.system, args=('python app.py',))
    flask_process.start()
    w.run()
    flask_process.join()
