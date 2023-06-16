import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import re

TOKEN = '5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8'

def start(update, context):
    """Handle the /start command."""
    welcome_message = '🤖📱 Welcome! I\'m the "Number Locator" Bot! Please provide a phone number for investigation like "01*********".\n' \
                      'Remember, the number should be from *Airtel*, *Banglalink*, or *Robi*. Let\'s uncover its location! 🌍🔍\n' \
                      'Developer @Mahmud_Rafi'
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message, parse_mode=telegram.ParseMode.MARKDOWN_V2)

def handle_message(update, context):
    """Handle user messages."""
    message = update.message.text
    if message.startswith("01") and len(message) == 11:
        api_url = f"https://teamtasik.xyz/api/siminfo.php?key=free&phone={message}"
        
        # Send the "Finding" message
        finding_message = context.bot.send_message(chat_id=update.effective_chat.id, text='Finding🧐')
        
        # Request the API and extract the desired tags
        api_response = requests.get(api_url).text
        
        # Check if the API response contains a specific message
        if '"HEY KIDS WHEY SELL FREE API":"TOR ABBA"' in api_response:
            # Send the "The bot is now on honeymoon" message
            honeymoon_message = '💆‍♂️🏮 The bot is now having a Thai massage, please wait for a while and will be back soon'
            context.bot.send_message(chat_id=update.effective_chat.id, text=honeymoon_message)
        else:
            # Extract the desired tags
            user_imei = re.findall(r'"User_IMEI":"([^"]*)"', api_response)[0]
            user_imsi = re.findall(r'"User_IMSI":"([^"]*)"', api_response)[0]
            user_last_action_date = re.findall(r'"User_time_last_action":"([^"]*)"', api_response)[0]
            user_last_action_time = re.findall(r'"User_TIME_LAST_ACTION":"([^"]*)"', api_response)[0]
            user_sector_name = re.findall(r'"User_SECTOR_NAME":"([^"]*)"', api_response)[0]
            user_union_name = re.findall(r'"User_UNION_NAME":"([^"]*)"', api_response)[0]
            user_thana = re.findall(r'"User_THANA":"([^"]*)"', api_response)[0]
            user_district = re.findall(r'"User_DISTRICT":"([^"]*)"', api_response)[0]
            user_division = re.findall(r'"User_DIVISON":"([^"]*)"', api_response)[0]
            user_loc_long = re.findall(r'"User_LOC_LONG":"([^"]*)"', api_response)[0]
            user_loc_lat = re.findall(r'"User_LOC_LAT":"([^"]*)"', api_response)[0]
            
            # Create a formatted reply message with emojis
            reply_message = '🔍 Result:'
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
