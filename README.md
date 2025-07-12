# 🎟️ Ticketmaster Ticket Tracker Bot

A smart Python bot to monitor Ticketmaster event pages and notify you via Discord, Telegram, Slack, or Email when tickets become available!

---

## 🚀 Features
- Scrapes Ticketmaster event pages for ticket status ("Buy Tickets", "Tickets Not Available", etc.)
- Supports multiple event URLs via `config/config.json`
- Notifies you instantly via:
  - Discord Webhook
  - Telegram Bot
  - Slack Bot
  - Email (Gmail/Outlook)
- Logs every check with timestamps and colored alerts
- Tracks last known status in `data/status.json`
- Securely loads credentials from `.env`
- Retry logic and error handling
- Easy to run on Replit, Railway, Render, PythonAnywhere, or your own PC

---

## 🗂️ Folder Structure
```
TicketmasterBot/
├── config/
│   └── config.json
├── data/
│   └── status.json
├── src/
│   ├── notifier.py
│   ├── scraper.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

1. **Clone or Download the Repo**
2. **Install Python 3.10+**
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your `.env` file:**
   - Copy `.env.example` to `.env` and fill in your credentials (Discord webhook, Telegram token, etc.)
5. **Edit `config/config.json`:**
   - Add one or more Ticketmaster event URLs to track.
6. **Run the bot:**
   ```bash
   python src/main.py
   ```

---

## 🔔 Notification Setup
- **Discord:** Create a webhook in your server and paste the URL in `.env`
- **Telegram:** Create a bot with [@BotFather](https://t.me/BotFather), get the token, and your chat/user ID
- **Slack:** Create a bot and get the webhook URL or bot token
- **Email:** Use Gmail/Outlook app password (never your real password!)

---

## 🛠️ Deployment Options
- **Replit:** Import repo, add secrets, run `python src/main.py`
- **Railway/Render/PythonAnywhere:** Deploy as a Python service, set up environment variables
- **Local:** Just run as above

---

## 🧑‍💻 Advanced
- Optional: Run as a Flask/FastAPI app (see `src/main.py` for `/track` route example)
- Optional: Enable sound alert or desktop pop-up (see code comments)

---

## 📜 License
MIT

---

## 💡 Impress your friends with a smart, secure, and professional ticket tracker! 🎉 