import logging
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
    # Implement your logic to process the phone number and uncover its location
    # Here, you can use APIs or other methods to determine the location of the phone number
    # Once you have the location, you can send it back to the user using context.bot.send_message()

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
