import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import re
import time

TOKEN = '5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8'

def start(update, context):
    """Handle the /start command."""
    welcome_message = '🤖📱 Welcome! I\'m the "Number Locator" Bot! Please provide a phone number for investigation like "01*********".\n' \
                      'Remember, the number should be from Airtel, Banglalink, or Robi. Let\'s uncover its location! 🌍🔍\n' \
                      'Developer @Mahmud_Rafi'
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

def handle_message(update, context):
    """Handle user messages."""
    message = update.message.text
    if message.startswith("01") and len(message) == 11:
        api_url = f"https://teamxfire.com/Nidinxx/Vx.php?number={message}"
        
        # Send the waiting animation message
        waiting_message = 'Finding🧐'
        animation = '|'
        reply_message = context.bot.send_message(chat_id=update.effective_chat.id, text=waiting_message)
        
        # Add the waiting animation frames
        for _ in range(10):
            time.sleep(0.5)
            animation += '='
            reply_message.edit_text(f'{waiting_message} {animation} |')
        
        # Request the API and extract the desired tags
        api_response = requests.get(api_url).text
        extracted_tags = re.findall(r'"(User_IMEI|User_IMSI|User_time_last_action|User_REGION|User_DIVISON|User_DISTRICT|User_THANA|User_UNION_NAME|User_LOC_LONG|User_LOC_LAT)":"([^"]*)"', api_response)
        
        # Create a formatted reply message with emojis
        reply_message.edit_text('🔍 API Result:')
        for tag, value in extracted_tags:
            reply_message.edit_text(reply_message.text + f'\n✅ {tag}: {value}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='⚠️ERROR⚠️ || The following reasons can cause the error: \n Wrong mobile number\n Not of Banglalink/ Airtel/ Robi operators\n The number is out of service')

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
