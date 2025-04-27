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

# Bank options including Visa-branded banks and GBP Visa
BANKS = [
    'Bank of America Visa',
    'Chase Bank Visa',
    'Wells Fargo Visa',
    'Royal Bank of Canada Visa',
    'Toronto-Dominion Bank Visa',
    'GBP Visa'
]

# Card images, prices, descriptions, and links
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
    "Platinum Visa": {
        "image": "https://i.imgur.com/egjhEpm.png", 
        "price": "$1500", 
        "desc": "Exclusive access to premium services.",
        "link": "https://globalbusinesspays-com.onrender.com/card/3"
    },
    "World Visa": {
        "image": "https://i.imgur.com/u8Q6OlU.png", 
        "price": "$2000", 
        "desc": "Designed for frequent travelers and business users.",
        "link": "https://globalbusinesspays-com.onrender.com/card/4"
    },
    "World Elite Visa": {
        "image": "https://i.imgur.com/hZMQes2.png", 
        "price": "$2500", 
        "desc": "VIP support and top-tier benefits.",
        "link": "https://globalbusinesspays-com.onrender.com/card/5"
    },
    "Business Visa": {
        "image": "https://i.imgur.com/BXk3lZ8.jpg", 
        "price": "$3000", 
        "desc": "Tailored for entrepreneurs and high-volume users.",
        "link": "https://globalbusinesspays-com.onrender.com/card/6"
    }
}

# About text as triple-quoted string
ABOUT_TEXT = """
GlobalBusinessPay (GBP) portal. Please allow us to clarify everything for you with full transparency and professionalism.

Why You Can Trust This Platform

Our website is directly connected with GlobalBusinessPay. While it may have a separate interface, all VISA card activations and payment operations are securely processed through GBP’s official system.

Payments are made securely using cryptocurrencies for fast, safe, and borderless transactions.

Steps for Activating Your VISA Card

Once you choose your desired VISA card and complete the payment, you will be asked to submit:
- Your GlobalBusinessPay account number
- Your registered GBP email address
- Your full name (as registered)
- A clear copy of your payment receipt

This ensures correct linking of your payment to your GBP account and enables a smooth activation process.

Exclusive Platform Access

This dedicated card activation portal was kept confidential by GBP for years. After extensive effort, it is now available to assist users like you. Its secure infrastructure, ease of use, and fast processing make it a top choice for verified GBP users.
"""

# Typing action decorator

def send_typing_action(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        return await func(update, context)
    return wrapper

# /start handler: show bank options
@send_typing_action
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton(bank)] for bank in BANKS]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Welcome! Please select your bank to proceed:",
        reply_markup=reply_markup
    )

# Show main menu after GBP Visa selected
@send_typing_action
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Cards"), KeyboardButton("Price Listing")],
        [KeyboardButton("About"), KeyboardButton("Purchase")],
        [KeyboardButton("Help")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "You selected GBP Visa. Choose an option:",
        reply_markup=reply_markup
    )

# Handle all text messages
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
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(card_selection))
    app.run_polling()
