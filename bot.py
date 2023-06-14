import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import re

TOKEN = '5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8'

def start(update, context):
    """Handle the /start command."""
    welcome_message = '''🤖📱 Welcome! I'm the "Number Locator" Bot! Please provide a phone number for investigation like "01*********".
    Remember, the number should be from Airtel, Banglalink, or Robi. Let's uncover its location! 🌍🔍
    Developer @Mahmud_Rafi'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

def handle_message(update, context):
    """Handle user messages."""
    message = update.message.text
    if message.startswith("01") and len(message) == 11:
        api_url = f"https://teamxfire.com/Nidinxx/Vx.php?number={message}"
        api_response = requests.get(api_url).text
        
        # Extract the desired tags from the API response
        extracted_tags = re.findall(r'"(User_IMEI|User_IMSI|User_time_last_action|User_REGION|User_DIVISON|User_DISTRICT|User_THANA|User_UNION_NAME|User_LOC_LONG|User_LOC_LAT)":"([^"]*)"', api_response)
        
        # Create a formatted reply message
        reply_message = "API Result:\n"
        for tag, value in extracted_tags:
            reply_message += f"{tag}: {value}\n"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid phone number format. Please provide a valid number.")

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
