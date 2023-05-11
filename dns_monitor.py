import time
import re
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class LogHandler(FileSystemEventHandler):
    def __init__(self, filename, domain, webhook):
        self.filename = filename
        self.domain = domain
        self.webhook = webhook

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.filename):
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                for line in lines[-1:]:  
                    match = re.search(r'\(([\w\.-]+)\)', line)
                    print(f'This is line {line}')
                    if match and self.domain in match.group(1):
                        data = {"content": f"Domain ***{match.group(1)}*** was resolved: ***{line}***"}
                        requests.post(self.webhook, data=data)


if __name__ == "__main__":
    filename = '/var/log/named/named.log'
    domain = 'put your kiri domain here'
    webhook = 'put your kiri webhook here'

    event_handler = LogHandler(filename, domain, webhook)
    observer = Observer()
    observer.schedule(event_handler, path='/'.join(filename.split('/')[:-1]), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()