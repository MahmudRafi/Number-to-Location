import logging
import requests
import time
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the welcome message
welcome_message = '🤖📱 Welcome! I\'m the "Number Locator" Bot! Please provide a phone number for investigation like "01*********". \n Remember, the number should be from Airtel, Banglalink, or Robi. Let\'s uncover its location! 🌍🔍 \n Developer @Mahmud_Rafi'

# Handler for the /start command
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

# Handler for all other messages
def process_number(update: Update, context: CallbackContext):
    number = update.message.text.replace('num', '').strip()  # Remove 'num' prefix and strip spaces
    api_url = f'https://teamxfire.com/Nidinxx/Vx.php?number={number}'
    
    try:
        # Set the timeout for the API request
        timeout = 25  # 10 seconds
        start_time = time.time()
        response = requests.get(api_url, timeout=timeout)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200 and response.json()['status'] == 'success':
            data = response.json()
            
            user_imei = data['User_IMEI']
            user_imsi = data['User_IMSI']
            user_last_action = data['User_time_last_action']
            user_region = data['User_REGION']
            user_division = data['User_DIVISON']
            user_district = data['User_DISTRICT']
            user_thana = data['User_THANA']
            user_union_name = data['User_UNION_NAME']
            user_loc_long = data['User_LOC_LONG']
            user_loc_lat = data['User_LOC_LAT']
            
            # Format the response with emojis
            response_text = f'✅ Here is the information for number {number}:\n\n' \
                            f'📱 User IMEI: {user_imei}\n' \
                            f'📲 User IMSI: {user_imsi}\n' \
                            f'⏰ User Last Action Time: {user_last_action}\n' \
                            f'🗺️ User Region: {user_region}\n' \
                            f'🌍 User Division: {user_division}\n' \
                            f'🏢 User District: {user_district}\n' \
                            f'🏪 User Thana: {user_thana}\n' \
                            f'🏘️ User Union Name: {user_union_name}\n' \
                            f'📍 User Location Longitude: {user_loc_long}\n' \
                            f'📍 User Location Latitude: {user_loc_lat}'
            
            if elapsed_time >= timeout:
                response_text += '\n\n⚠️ The API response took longer than expected.'
        else:
            response_text = '❌ Sorry, unable to fetch data for the provided number.'
    except requests.Timeout:
        response_text = '⌛ The API request timed out. Please try again later.'
    except requests.RequestException:
        response_text = '❌ An error occurred while making the API request. Please try again later.'
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

def main():
    # Create the Updater and pass in your bot's token
    updater = Updater(token='5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_number))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
