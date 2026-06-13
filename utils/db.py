import json, os
from datetime import datetime
from config import SHOP_ITEMS

DB_FILE = "data/bank.json"

def load_db():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user(db, uid: str):
    if uid not in db:
        db[uid] = {
            "balance":          5000,
            "bank":             0,
            "xp":               0,
            "level":            1,
            "streak":           0,
            "last_daily":       None,
            "total_earned":     0,
            "total_lost":       0,
            "games_played":     0,
            "wins":             0,
            "losses":           0,
            "married_to":       None,
            "protection_until": None,
            "inventory":        {k: 0 for k in SHOP_ITEMS},
            "cooldowns":        {},
            "rob_success":      0,
            "joined":           datetime.now().isoformat(),
        }
        save_db(db)
    return db[uid]
