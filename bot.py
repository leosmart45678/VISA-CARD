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
    # Add the rest of your cards here...
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

# Define the handle_message function to process incoming text messages
@send_typing_action
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # First menu: bank selection
    if text in BANKS:
        if text != 'GBP Visa':
            await update.message.reply_text("This card type is not currently available.")
        else:
            await show_main_menu(update, context)
        return

    # Main menu actions
    if text == "Cards":
        keyboard = [
            [
                InlineKeyboardButton(name, callback_data=name),
                InlineKeyboardButton(f"Price: {data['price']}", callback_data=f"price_{name}"),
                InlineKeyboardButton("View in Store", url=data['link'])
            ] 
            for name, data in CARDS.items()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Select a card to view details:", reply_markup=reply_markup)

    elif text == "Price Listing":
        info = "\n".join([f"{name}: {data['price']}" for name, data in CARDS.items()])
        await update.message.reply_text(f"Card Prices:\n\n{info}")

    elif text == "About":
        await update.message.reply_text(ABOUT_TEXT)

    elif text == "Purchase":
        purchase_text = (
            "To purchase a Visa card, follow these steps:\n"
            "1. Visit: https://globalbusinesspays-com.onrender.com/\n"
            "2. Select your desired card.\n"
            "3. Complete payment securely using cryptocurrencies.\n"
            "4. Submit activation details with payment receipt."
        )
        await update.message.reply_text(purchase_text)

    elif text == "Help":
        keyboard = [[InlineKeyboardButton("Contact Support on Telegram", url="https://t.me/+12136811616")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Need help?", reply_markup=reply_markup)

    else:
        await update.message.reply_text("Please select an option from the menu.")

# Handle card button clicks
@send_typing_action
async def card_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    card_name = query.data
    data = CARDS.get(card_name)
    if data:
        caption = f"{card_name}: {data['price']} - {data['desc']}\n\n"
        caption += f"View in Store: {data['link']}"
        await query.message.reply_photo(photo=data['image'], caption=caption)

# Entry point
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # This line is where the error happened
    app.add_handler(CallbackQueryHandler(card_selection))

    # Run the bot with polling
    app.run_polling()
