 from pymongo import MongoClient
import datetime

MONGO_URL = "mongodb+srv://your_mongo_url"

client = MongoClient(MONGO_URL)
db = client["wordgrid"]

users = db["users"]


def get_user(uid):
    u = users.find_one({"_id": uid})
    if not u:
        u = {"_id": uid, "score": 0, "coins": 0, "last_daily": None}
        users.insert_one(u)
    return u


def update_score(uid, score):
    users.update_one({"_id": uid}, {"$inc": {"score": score}}, upsert=True)


def add_coins(uid, coins):
    users.update_one({"_id": uid}, {"$inc": {"coins": coins}}, upsert=True)


def claim_daily(uid):
    user = get_user(uid)
    today = str(datetime.date.today())

    if user["last_daily"] == today:
        return "❌ Already claimed today"

    users.update_one(
        {"_id": uid},
        {"$set": {"last_daily": today}, "$inc": {"coins": 100}}
    )

    return "🎁 Daily reward: +100 coins"


def leaderboard():
    top = users.find().sort("score", -1).limit(10)

    out = ""
    i = 1
    for u in top:
        out += f"{i}. {u['_id']} - ⭐{u['score']} 💎{u['coins']}\n"
        i += 1

    return out


def live_rank():
    top = users.find().sort("score", -1).limit(5)

    out = "🔥 LIVE RANKING 🔥\n\n"
    i = 1
    for u in top:
        out += f"{i}. {u['_id']} → {u['score']}\n"
        i += 1

    return out
