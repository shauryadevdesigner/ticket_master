import os
import requests
from dotenv import load_dotenv
from colorama import Fore, Style
from slack_sdk.webhook import WebhookClient
import asyncio
from telegram import Bot
from datetime import datetime
import json

load_dotenv()

# Discord
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
# Slack
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

LOG_PATH = os.path.join(os.path.dirname(__file__), '../data/notification_log.json')

def log_notification(message, subject=None):
    log_entry = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'message': message,
        'subject': subject or '',
    }
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.insert(0, log_entry)  # newest first
        with open(LOG_PATH, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(Fore.RED + f"[notifier] Log error: {e}" + Style.RESET_ALL)

def notify_discord(message):
    if not DISCORD_WEBHOOK_URL:
        return
    data = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
    except Exception as e:
        print(Fore.RED + f"[notifier] Discord error: {e}" + Style.RESET_ALL)

def notify_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    async def send():
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    try:
        asyncio.run(send())
    except Exception as e:
        print(Fore.RED + f"[notifier] Telegram error: {e}" + Style.RESET_ALL)

def notify_slack(message):
    if not SLACK_WEBHOOK_URL:
        return
    try:
        webhook = WebhookClient(SLACK_WEBHOOK_URL)
        webhook.send(text=message)
    except Exception as e:
        print(Fore.RED + f"[notifier] Slack error: {e}" + Style.RESET_ALL)

def notify_all(message, subject=None):
    log_notification(message, subject)
    notify_discord(message)
    notify_telegram(message)
    notify_slack(message) 