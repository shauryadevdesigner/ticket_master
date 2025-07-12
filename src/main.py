import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, Style, init as colorama_init
from src.scraper import scrape_ticket_status
from src.notifier import notify_all

colorama_init(autoreset=True)
load_dotenv()

# Send a test notification on startup
notify_all("Test notification from your Ticketmaster bot! If you see this, notifications are working.", subject="Test Alert")

CONFIG_PATH = "config/config.json"
STATUS_PATH = "data/status.json"
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 600))

# Load config
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
urls = config.get("urls", [])

# Load last known status
if os.path.exists(STATUS_PATH):
    with open(STATUS_PATH, "r") as f:
        last_status = json.load(f)
else:
    last_status = {url: "Unknown" for url in urls}

def save_status(status):
    with open(STATUS_PATH, "w") as f:
        json.dump(status, f, indent=2)

def log(msg, color=Fore.WHITE):
    print(color + f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}" + Style.RESET_ALL)

def main_loop():
    global last_status
    while True:
        for url in urls:
            log(f"Checking {url} ...", Fore.CYAN)
            status = scrape_ticket_status(url)
            if status:
                log(f"Status: {status}", Fore.GREEN if 'buy' in status.lower() else Fore.YELLOW)
                if last_status.get(url) != status:
                    if 'buy' in status.lower() or 'find' in status.lower():
                        alert = f"🎟️ TICKETS AVAILABLE! {url} ({status})"
                        log(alert, Fore.GREEN)
                        notify_all(alert, subject="Ticket Alert!")
                    elif 'sold out' in status.lower() or 'not available' in status.lower():
                        alert = f"❌ Tickets not available: {url} ({status})"
                        log(alert, Fore.RED)
                        notify_all(alert, subject="Ticket Update")
                    last_status[url] = status
                    save_status(last_status)
            else:
                log(f"Failed to get status for {url}", Fore.RED)
        log(f"Sleeping for {CHECK_INTERVAL//60} minutes...", Fore.BLUE)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop() 