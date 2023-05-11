# Bind9 Log Monitor

This Python script continuously monitors a Bind9 log file and sends a Discord notification each time a specified domain is resolved.

## Prerequisites

1. Python 3.6 or later.
2. Python packages: `watchdog` and `requests`.

You can install the necessary Python packages with pip:

```bash
pip install watchdog requests
```

## Setup

1. Clone this repository or download the script.

2. Replace `'your-domain.com'` and `'YOUR_DISCORD_WEBHOOK_URL'` in the script with your actual domain and Discord webhook URL.

3. Replace `'/var/log/named/named.log'` with the path to your Bind9 log file if it's different.

## Usage

The recommended way to use this script is to set it up as a system service. This allows the script to start automatically when the server boots and restart if it crashes.

1. Create a systemd service file for the script:

```ini
[Unit]
Description=Bind9 Log Monitor

[Service]
ExecStart=/usr/bin/python3 /path/to/your/bind9_monitor.py
Restart=always
User=yourusername
Group=yourgroup
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Replace `/path/to/your/bind9_monitor.py` with the actual path to your Python script, and replace `yourusername` and `yourgroup` with your system's username and group (you can get these by running `whoami` and `id -gn` commands in the terminal).

2. Save the service file to `/etc/systemd/system/`, for example, at `/etc/systemd/system/bind9-log-monitor.service`.

3. Enable the service with:

```bash
sudo systemctl enable bind9-log-monitor
```

4. Start the service with:

```bash
sudo systemctl start bind9-log-monitor
```

Now, your script will run as a service, and you should receive a Discord notification each time your domain is resolved according to your Bind9 logs.

