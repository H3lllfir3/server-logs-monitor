import os
import time
import re
import datetime

from discord_webhook import DiscordWebhook
import pytz


DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1103702671501840475/LJmxTrmBFdq1OB75-8r_l7aKokJ2TubldCDMGSsKOkrv0JN-Y9KVxUripdhaygjXIK5P'
SSHD_LOG_FILE = '/var/log/auth.log'

def send_discord_notification(message):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
    webhook.execute()

def monitor_ssh_log():
    tehran_tz = pytz.timezone('Asia/Tehran')

    with open(SSHD_LOG_FILE, 'r') as log_file:
        log_file.seek(0, os.SEEK_END)
        last_processed_position = log_file.tell()

    while True:
        with open(SSHD_LOG_FILE, 'r') as log_file:
            log_file.seek(last_processed_position)
            log_data = log_file.readlines()
            if not log_data:
                time.sleep(5)
                continue

            for line in log_data:
                sshd_match = re.search(r'(\w+\s+\d+ \d+:\d+:\d+) .*sshd\[\d+\]: Accepted .* for (\w+) from (\d+\.\d+\.\d+\.\d+) port', line)

                if sshd_match:
                    log_time, username, ip_address = sshd_match.groups()
                    log_datetime = datetime.datetime.strptime(log_time, '%b %d %H:%M:%S')
                    current_year = datetime.datetime.now().year
                    log_datetime = log_datetime.replace(year=current_year)
                    log_datetime = log_datetime.astimezone(tehran_tz)
                    formatted_datetime = log_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    message = f'New SSH connection at ***{formatted_datetime}***: User ***{username}*** logged in from ***{ip_address}***'
                    send_discord_notification(message)

            last_processed_position = log_file.tell()

        time.sleep(5)


if __name__ == '__main__':
    monitor_ssh_log()

