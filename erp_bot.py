from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    CallbackQueryHandler, MessageHandler, filters,
    ConversationHandler
)
import requests
import json
from datetime import date, datetime, timedelta

# === Initial Setup ===
today = date.today()
from_date = today - timedelta(days=1)  # Make to_date > from_date
to_date = today 

# === Config ===
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ERP_URL = "http://your-local-erp-instance/"
ERP_API_KEY = "your-api-key"
ERP_API_SECRET = "your-api-secret"

HEADERS = {
    "Authorization": f"token {ERP_API_KEY}:{ERP_API_SECRET}",
    "Content-Type": "application/json"
}

# === Helper function ===
def get_employee_by_telegram_id(telegram_id):
    filters = json.dumps([["custom_telegram_id", "=", str(telegram_id)]])
    params = {
        "filters": filters,
        "fields": json.dumps(["name", "custom_telegram_id"])
    }
    res = requests.get(f"{ERP_URL}/api/resource/Employee", headers=HEADERS, params=params)
    data = res.json().get("data", [])
    if data:
        return data[0]["name"]
    return None

# === Command Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I'm your ERPNext Bot. Type /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Commands:\n"
        "/id - Show your Telegram ID\n"
        "/punch_in - Mark attendance (Checkin IN)\n"
        "/punch_out - Mark exit (Checkin OUT)\n"
    )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    await update.message.reply_text(f"👤 Your Telegram ID is: {telegram_id}")

async def punch_in(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    employee = get_employee_by_telegram_id(telegram_id)

    if not employee:
        await update.message.reply_text("❌ You're not linked to an Employee in ERPNext.")
        return

    payload = {
        "employee": employee,
        "log_type": "IN",
        "time": datetime.now().isoformat()
    }

    res = requests.post(f"{ERP_URL}/api/resource/Employee Checkin", headers=HEADERS, json=payload)

    if res.status_code == 200:
        await update.message.reply_text("✅ You've been punched in!")
    else:
        await update.message.reply_text("❌ Failed to punch in.")

async def punch_out(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    employee = get_employee_by_telegram_id(telegram_id)

    if not employee:
        await update.message.reply_text("❌ You're not linked to an Employee in ERPNext.")
        return

    payload = {
        "employee": employee,
        "log_type": "OUT",
        "time": datetime.now().isoformat()
    }

    res = requests.post(f"{ERP_URL}/api/resource/Employee Checkin", headers=HEADERS, json=payload)

    if res.status_code == 200:
        await update.message.reply_text("✅ You've been punched out!")
    else:
        await update.message.reply_text("❌ Failed to punch out.")


# === Run Bot ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("id", id_command))
app.add_handler(CommandHandler("punch_in", punch_in))
app.add_handler(CommandHandler("punch_out", punch_out))
app.run_polling()
