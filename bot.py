from telegram.ext import Updater, CommandHandler

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a simple Telegram bot.")

def main():
    updater = Updater(token='5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
