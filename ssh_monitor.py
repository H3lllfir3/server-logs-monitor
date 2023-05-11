import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import datetime
import pytz

DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'
SSHD_LOG_FILE = '/var/log/auth.log'

class LogHandler(FileSystemEventHandler):
    def __init__(self, filename, webhook):
        self.filename = filename
        self.webhook = webhook

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.filename):
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                for line in lines[-2:]:  
                    sshd_match = re.search(r'(\w+\s+\d+ \d+:\d+:\d+) .*sshd\[\d+\]: Accepted .* for (\w+) from (\d+\.\d+\.\d+\.\d+) port', line)
                    if sshd_match:
                        log_time, username, ip_address = sshd_match.groups()
                        log_datetime = datetime.datetime.strptime(log_time, '%b %d %H:%M:%S')
                        current_year = datetime.datetime.now().year
                        log_datetime = log_datetime.replace(year=current_year)
                        log_datetime = log_datetime.astimezone(pytz.timezone('Asia/Tehran'))
                        formatted_datetime = log_datetime.strftime('%Y-%m-%d %H:%M:%S')
                        message = f'New SSH connection at {formatted_datetime}: User {username} logged in from {ip_address}'
                        data = {"content": message}
                        requests.post(self.webhook, data=data)

if __name__ == "__main__":
    event_handler = LogHandler(SSHD_LOG_FILE, DISCORD_WEBHOOK_URL)
    observer = Observer()
    observer.schedule(event_handler, path='/'.join(SSHD_LOG_FILE.split('/')[:-1]), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
