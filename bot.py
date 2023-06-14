import logging
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
def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='I\'m sorry, I don\'t understand that command.')

def main():
    # Create the Updater and pass in your bot's token
    updater = Updater(token='5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8', use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
