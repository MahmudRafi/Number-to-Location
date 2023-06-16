import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

TOKEN = '5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8'

def start(update, context):
    welcome_message = '''🤖📱 Welcome! I'm the "Number Locator" Bot! Please provide a phone number for investigation like "01*********".
Remember, the number should be from Airtel, Banglalink, or Robi. Let's uncover its location! 🌍🔍
Developer @Mahmud_Rafi'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

def handle_message(update, context):
    phone_number = update.message.text.strip()
    if phone_number.startswith('01') and len(phone_number) == 11:
        api_url = f'https://teamtasik.xyz/api/siminfo.php?key=free&phone={phone_number}'
        response = requests.get(api_url)
        api_result = response.text
        context.bot.send_message(chat_id=update.effective_chat.id, text=api_result)
    else:
        error_message = 'Invalid phone number! Please provide a valid Bangladeshi number starting with "01" and consisting of 11 digits.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
