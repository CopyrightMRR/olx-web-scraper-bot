![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Redis](https://img.shields.io/badge/redis-required-DC382D)
 
A Telegram bot that watches [OLX.ua](https://www.olx.ua) search results for you. Save a search query, and the bot polls OLX in the background and messages you the moment a new listing matching it appears.
 
## Table of Contents
 
- [About](#about)
- [Quickstart](#quickstart)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Notes & Known Limitations](#notes--known-limitations)
- [License](#license)
## 🚀 About
 
Add a query, tap **Start**, and the bot takes it from there — polling OLX's GraphQL search endpoint every 30 seconds and notifying you in Telegram as soon as something new comes up, with duplicate-free delivery backed by Redis.
 
- **Multiple trackers per chat** — track as many OLX searches as you want at once.
- **Persistent** — trackers are stored in PostgreSQL and survive a bot restart.
- **No duplicate pings** — each tracker keeps a Redis set of listing IDs it has already notified you about.
- **One tap to pause** — stop a tracker without losing it; start it again whenever.
## ⚡ Quickstart
 
```bash
git clone <your-repo-url>
cd <your-repo-folder>
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
 
echo "BOT_TOKEN=your-telegram-bot-token" > .env
 
# make sure PostgreSQL and Redis are running and reachable, then:
python main.py
```
 
Tables are created automatically on first run — no separate migration step needed.
 
## ✨ Features
 
- Track any OLX.ua search query from inside Telegram
- Start / stop tracking without losing saved trackers
- Remove trackers you no longer need
- Active trackers resume automatically on bot restart
- Deduplicated notifications via Redis-backed "seen" sets
## 🧱 Tech Stack
 
- **[aiogram 3](https://docs.aiogram.dev/)** — Telegram bot framework
- **SQLAlchemy 2.0 (async) + asyncpg** — stores trackers in PostgreSQL
- **Redis** — tracks which listing IDs have already been notified
- **aiohttp** — queries OLX's GraphQL search API
## 🗂️ Project Structure
 
```
.
├── main.py                        # Bot entrypoint: DB init, resumes active trackers, starts polling
├── requirements.txt
├── database/
│   ├── __init__.py                # engine / session_maker (configure your DB connection here)
│   ├── models/
│   │   ├── __init__.py            # BaseModel (SQLAlchemy declarative base)
│   │   └── tracker.py             # Tracker ORM model (id, query, chat_id, status)
│   └── repositories/
│       └── tracker.py             # TrackerRepo — CRUD for trackers
├── handlers/
│   ├── start.py                   # /start command
│   ├── tracking.py                # "+ Tracking" flow, OLX polling loop, task creation
│   ├── tracking_list.py           # "View tracker list" flow, start/stop/remove callbacks
│   └── tracker_state.py           # in-memory registry of running tracker tasks
├── keyboards/
│   ├── main.py                    # main reply keyboard
│   └── tracker.py                 # per-tracker inline keyboard (Start/Stop, Remove)
└── middlewares/
    ├── __init__.py                # middleware registration
    └── session.py                 # injects a DB session/TrackerRepo into every update
```
 
## 🔧 Setup
 
1. **Install dependencies**
```bash
   python -m venv venv
   source venv/bin/activate   # venv\Scripts\activate on Windows
   pip install -r requirements.txt
```
 
2. **Configure environment variables**
   Create a `.env` file in the project root:
```env
   BOT_TOKEN=your-telegram-bot-token
```
 
   Get a token from [@BotFather](https://t.me/BotFather). If `database/__init__.py` reads a connection string from the environment, add that variable here too (e.g. `DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname`).
 
3. **Start PostgreSQL and Redis**, locally or via Docker, reachable at the addresses your config expects (Redis defaults to `localhost:6379`).
4. **Run the bot**
```bash
   python main.py
```
 
## 🕹️ Usage
 
1. Send `/start` to the bot.
2. Tap **"+ Tracking"** and send the text you want to search for on OLX — this creates a new (inactive) tracker.
3. Tap **"View tracker list"** to see all your trackers.
4. Tap **Start** on a tracker to begin polling; tap **Stop** to pause it. Tap **Remove** to delete it entirely.
## ⚠️ Notes & Known Limitations
 
- The Redis host/port (`localhost:6379`) is hardcoded in `handlers/tracking.py` — update it if Redis runs elsewhere.
- The OLX search request includes a hardcoded `sl` location parameter, which may scope results to a specific area — adjust it if you need different geographic coverage.
- Redis "seen" sets have no expiration, so they'll grow indefinitely for long-running trackers.

