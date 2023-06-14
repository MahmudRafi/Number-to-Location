import logging
import requests
from telegram import Emoji
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the welcome message
welcome_message = '''🤖📱 Welcome! I'm the "Number Locator" Bot! Please provide a phone number for investigation like "01*********".
Remember, the number should be from Airtel, Banglalink, or Robi. Let's uncover its location! 🌍🔍
Developer @Mahmud_Rafi'''

# Define the start command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

# Define the message handler
def handle_message(update, context):
    phone_number = update.message.text
    api_url = f"https://teamxfire.com/Nidinxx/Vx.php?number={phone_number}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data:
            imei = data.get("User_IMEI", "")
            imsi = data.get("User_IMSI", "")
            last_action = data.get("User_time_last_action", "")
            region = data.get("User_REGION", "")
            division = data.get("User_DIVISON", "")
            district = data.get("User_DISTRICT", "")
            thana = data.get("User_THANA", "")
            union_name = data.get("User_UNION_NAME", "")
            loc_long = data.get("User_LOC_LONG", "")
            loc_lat = data.get("User_LOC_LAT", "")

            response_message = f"📞 Number: {phone_number}\n\n"
            response_message += f"{Emoji.CHECK_MARK_BUTTON} IMEI: {imei}\n"
            response_message += f"{Emoji.CHECK_MARK_BUTTON} IMSI: {imsi}\n"
            response_message += f"{Emoji.CHECK_MARK_BUTTON} Last Action: {last_action}\n"
            response_message += f"{Emoji.GLOBE_WITH_MERIDIANS} Region: {region}\n"
            response_message += f"{Emoji.GLOBE_WITH_MERIDIANS} Division: {division}\n"
            response_message += f"{Emoji.GLOBE_WITH_MERIDIANS} District: {district}\n"
            response_message += f"{Emoji.GLOBE_WITH_MERIDIANS} Thana: {thana}\n"
            response_message += f"{Emoji.GLOBE_WITH_MERIDIANS} Union Name: {union_name}\n"
            response_message += f"{Emoji.WORLD_MAP} Location Longitude: {loc_long}\n"
            response_message += f"{Emoji.WORLD_MAP} Location Latitude: {loc_lat}\n"

        else:
            response_message = "❌ No data found for the provided number."

    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to the API: {e}")
        response_message = "❌ An error occurred while processing the request. Please try again later."

    context.bot.send_message(chat_id=update.effective_chat.id, text=response_message)

# Set up the bot and handlers
def main():
    # Set up the Telegram bot token
    token = "5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8"

    # Create the Updater and pass in the bot token
    updater = Updater(token=token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the start command handler
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Register the message handler
    message_handler = MessageHandler(Filters.text & ~Filters.command, handle_message)
    dispatcher.add_handler(message_handler)

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C to stop it
    updater.idle()

if __name__ == '__main__':
    main()
