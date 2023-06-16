import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import re

TOKEN = '5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8'

def start(update, context):
    """Handler for the /start command."""
    welcome_message = "👋 Welcome to the Location Finder Bot!\n\n" \
                      "Please enter your phone number in the following format: +123456789.\n" \
                      "For example: +15551234567"

    # Escape exclamation marks in the message
    welcome_message = welcome_message.replace('!', r'\!')

    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message, parse_mode=telegram.ParseMode.MARKDOWN_V2)


def handle_message(update, context):
    """Handle user messages."""
    message = update.message.text
    if message.startswith("01") and len(message) == 11:
        api_url = f"https://teamxfire.com/Nidinxx/Vx.php?number={message}"
        
        # Send the "Finding" message
        finding_message = context.bot.send_message(chat_id=update.effective_chat.id, text='Finding🧐')
        
        # Request the API and extract the desired tags
        api_response = requests.get(api_url).json()
        
        if '"HEY KIDS WHEY SELL FREE API":"TOR ABBA"' in api_response:
            # Send the "The bot is now having a Thai massage" message
            massage_message = '💆‍♂️🏮 The bot is now having a Thai massage, please wait for a while and will be back soon'
            context.bot.send_message(chat_id=update.effective_chat.id, text=massage_message)
        else:
            user_imei = api_response.get('User_IMEI', '')
            user_imsi = api_response.get('User_IMSI', '')
            user_last_action_date = api_response.get('User_date_last_action', '')
            user_last_action_time = api_response.get('User_time_last_action', '')
            user_sector_name = api_response.get('User_SECTOR_NAME', '')
            user_union_name = api_response.get('User_UNION_NAME', '')
            user_thana = api_response.get('User_THANA', '')
            user_district = api_response.get('User_DISTRICT', '')
            user_division = api_response.get('User_DIVISON', '')
            user_loc_long = api_response.get('User_LOC_LONG', '')
            user_loc_lat = api_response.get('User_LOC_LAT', '')
            
            # Create a formatted reply message with emojis
            reply_message = '🔍 Result:\n'
            reply_message += f'📱 User_IMEI: {user_imei}\n'
            reply_message += f'🆔 User_IMSI: {user_imsi}\n'
            reply_message += f'📅 User_last_action_date: {user_last_action_date}\n'
            reply_message += f'🕒 User_last_action_time: {user_last_action_time}\n'
            reply_message += f'📍 User_sector_name: {user_sector_name}\n'
            reply_message += f'🌐 User_union_name: {user_union_name}\n'
            reply_message += f'📍 User_thana: {user_thana}\n'
            reply_message += f'🏢 User_district: {user_district}\n'
            reply_message += f'🌍 User_division: {user_division}\n'
            reply_message += f'🗺️ User_loc_long: {user_loc_long}\n'
            reply_message += f'🗺️ User_loc_lat: {user_loc_lat}\n'

            
            # Send the reply message
            context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
        
        # Delete the "Finding" message
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=finding_message.message_id)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='⚠️ Invalid phone number format. Please provide a valid number.')

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
