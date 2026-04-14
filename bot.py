from pyrogram import Client, filters
from pyrogram.types import Message

from game_engine import WordGridGame
from database import get_user, claim_daily, leaderboard, live_rank, update_score, add_coins

API_ID = 1234567
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Client("wordgrid", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

games = {}

def get_game(uid):
    if uid not in games:
        games[uid] = WordGridGame("easy")
    return games[uid]


@app.on_message(filters.command("start"))
def start(_, msg: Message):
    msg.reply_text(
        "🎮 WORDGRID BOT\n\n"
        "/new - new game\n"
        "/guess <word>\n"
        "/score\n"
        "/daily\n"
        "/leaderboard\n"
        "/rank"
    )


@app.on_message(filters.command("new"))
def new(_, msg):
    games[msg.from_user.id] = WordGridGame("easy")
    msg.reply_text("🔥 New game started!")


@app.on_message(filters.command("guess"))
def guess(_, msg):
    game = get_game(msg.from_user.id)

    try:
        word = msg.text.split(" ", 1)[1]
    except:
        msg.reply_text("Usage: /guess CAT")
        return

    if game.check_word(word):
        score = game.add_score(word)

        update_score(msg.from_user.id, score)
        add_coins(msg.from_user.id, 10)

        msg.reply_text(f"✅ Correct +{score} score & 💎10 coins")
    else:
        msg.reply_text("❌ Wrong word")


@app.on_message(filters.command("score"))
def score(_, msg):
    user = get_user(msg.from_user.id)
    msg.reply_text(f"⭐ Score: {user['score']} | 💎 Coins: {user['coins']}")


@app.on_message(filters.command("daily"))
def daily(_, msg):
    msg.reply_text(claim_daily(msg.from_user.id))


@app.on_message(filters.command("leaderboard"))
def lb(_, msg):
    msg.reply_text("🏆 LEADERBOARD\n\n" + leaderboard())


@app.on_message(filters.command("rank"))
def rank(_, msg):
    msg.reply_text(live_rank())


app.run()
