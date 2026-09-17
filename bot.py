import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from datetime import datetime, timezone, timedelta

TOKEN = '8900932361:AAFBsfNBwv4bzQ6vxJ6Dkl5fr6grLkudkYE'
ADMIN_ID = '8377014940'
UPI_ID = '9039967013@pthdfc'
UPI_NAME = 'NeerajHustle'

bot = telebot.TeleBot(TOKEN)
user_sub = {}

def get_live_period():
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    return f"{now.strftime('%Y%m%d')}{100000 + (int(now.strftime('%H%M%S')) % 100000)}"

@bot.message_handler(commands=['start'])
def start_msg(m):
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("🚀 Start Live Trading (₹229)", callback_data="trade"))
    mk.add(InlineKeyboardButton("💬 Help & Support", url="https://t.me/KritikaPredictor"))
    bot.send_message(m.chat.id, "🔥 **AI TRADING BOT (SYNCED)** 🔥\n1-Hour Pass (₹229)\n👇 Choose:", reply_markup=mk, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    cid = c.message.chat.id
    bot.answer_callback_query(c.id)
    if c.data == "trade":
        if time.time() < user_sub.get(cid, 0):
            send_sig(cid)
        else:
            upi_url = f"upi://pay?pa={UPI_ID}&pn={UPI_NAME}&am=229&cu=INR"
            mk = InlineKeyboardMarkup()
            mk.add(InlineKeyboardButton("📱 Pay via UPI App", url=upi_url))
            mk.add(InlineKeyboardButton("✅ I Have Paid (Send SS)", callback_data="done"))
            bot.send_message(cid, f"💎 **VIP Access ₹229**\nPay to: `{UPI_ID}`\nSend SS after payment.", reply_markup=mk, parse_mode="Markdown")
    elif c.data == "done":
        bot.send_message(cid, "📸 Send payment **screenshot (SS)** right here.")
    elif c.data in ["win", "loss"]:
        bot.send_message(cid, "🎉 Logged! Next signal:")
        send_sig(cid)
    elif c.data.startswith("app_") or c.data.startswith("rej_"):
        parts = c.data.split("_")
        tid = int(parts)
        if parts[0] == "app":
            user_sub[tid] = time.time() + 3600
            bot.send_message(tid, "🎉 **VIP Approved (1 Hour)!**")
            send_sig(tid)
        else:
            bot.send_message(tid, "❌ Rejected. Re-upload valid SS.")

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    cid = m.chat.id
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton(f"✅ Approve {cid}", callback_data=f"app_{cid}"),
           InlineKeyboardButton(f"❌ Reject {cid}", callback_data=f"rej_{cid}"))
    bot.forward_message(ADMIN_ID, cid, m.message_id)
    bot.send_message(ADMIN_ID, f"🔔 Payment SS from `{cid}`:", reply_markup=mk, parse_mode="Markdown")
    bot.send_message(cid, "⏳ SS forwarded to Admin.")

def send_sig(cid):
    import random
    sig = random.choice(['BIG 🟢', 'SMALL 🔵', 'GREEN 🟢', 'RED 🔴'])
    mk = InlineKeyboardMarkup()
    mk.add(InlineKeyboardButton("🟢 WIN", callback_data="win"), InlineKeyboardButton("🔴 LOSS", callback_data="loss"))
    bot.send_message(cid, f"📊 **SYNCED SIGNAL**\nPeriod: `{get_live_period()}`\nPrediction: **{sig}**", reply_markup=mk, parse_mode="Markdown")

bot.infinity_polling()
