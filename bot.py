import os
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton
)
from telegram.constants import ChatAction
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

TOKEN = '7048206915:AAFsiN7crlNiADwGj1BhCAxjptvZh4x7yqM'

BANKS = [
    'Bank of America Visa',
    'Chase Bank Visa',
    'Wells Fargo Visa',
    'Royal Bank of Canada Visa',
    'Toronto-Dominion Bank Visa',
    'GBP Visa'
]

CARDS = {
    "Basic Premium Card": {
        "image": "https://i.imgur.com/MxMIwJb.png", 
        "price": "$500", 
        "desc": "Great starter option for easy transactions.",
        "link": "https://globalbusinesspays-com.onrender.com/card/1"
    },
    "Gold Visa": {
        "image": "https://i.imgur.com/ZKlpSSb.jpg", 
        "price": "$1000", 
        "desc": "Higher limits and extra cashback rewards.",
        "link": "https://globalbusinesspays-com.onrender.com/card/2"
    },
    # Additional cards...
}

ABOUT_TEXT = """
GlobalBusinessPay (GBP) portal. Please allow us to clarify everything for you with full transparency and professionalism.
"""

def send_typing_action(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        return await func(update, context)
    return wrapper

@send_typing_action
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(bank)] for bank in BANKS]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Welcome! Please select your bank to proceed:",
        reply_markup=reply_markup
    )

# Further handlers...

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Adding handlers to the app
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(card_selection))

    # If you want to use webhooks, you would bind the app to a specific port here
    # For now, we are using polling
    app.run_polling()  # Polling works fine, no need to specify a port for this
