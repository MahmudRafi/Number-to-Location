import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json

TOKEN = '5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8'

def start(update, context):
    welcome_message = '''🤖📱 Welcome! I'm the "Number Locator" Bot! Please provide a phone number for investigation like "01*********".
Remember, the number should be from Airtel or Robi. Let's uncover its location! 🌍🔍
Developer @Mahmud_Rafi'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

    # Send the permission request message with the chat ID
    permission_message = f'📢 To use this bot, please copy this chat ID: {update.effective_chat.id} and send it to @Mahmud_Rafi.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=permission_message)

def handle_message(update, context):
    chat_id = str(update.effective_chat.id)

    # Fetch the allowed chat IDs from the GitHub repository
    response = requests.get('https://raw.githubusercontent.com/MahmudRafi/hudaihudai/main/chat_ids.txt')
    allowed_chat_ids = response.text.strip().split('\n')

    if chat_id not in allowed_chat_ids:
        # Send a message indicating the user doesn't have permission
        permission_denied_message = f"⛔️ Oops! You don't have permission to use this bot. But don't worry, there's a way to gain access! ✨✉️\n\nTo unlock the power of this bot, all you need to do is copy your Chat ID:\n\n{chat_id}\n\nand send it to @Mahmud_Rafi. Once @Mahmud_Rafi accepts you, magic will happen, and you'll receive access to use this bot's hidden secrets! 🗝️🔓💫"
        context.bot.send_message(chat_id=update.effective_chat.id, text=permission_denied_message)
        return

    phone_number = update.message.text.strip()
    if phone_number.startswith('01') and len(phone_number) == 11:
        api_url = f'https://api.cybersh.xyz/siminfo.php?key=ST&number={phone_number}'

        # Send the waiting message
        waiting_message = context.bot.send_message(chat_id=update.effective_chat.id, text="Finding 🧐")

        # Fetch the API response
        response = requests.get(api_url)
        api_result = response.json()["siminfo"]
        formatted_result = format_api_result(api_result)

        # Delete the waiting message
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

        # Send the formatted result
        context.bot.send_message(chat_id=update.effective_chat.id, text=formatted_result)
    else:
        error_message = 'Invalid phone number! Please provide a valid Bangladeshi number starting with "01" and consisting of 11 digits. Ex. 01000000000'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)


def format_api_result(api_result):
    number = api_result["number"]
    imei = api_result["imei"]
    imsi = api_result["imsi"]
    division = api_result["division"]
    district = api_result["district"]
    region = api_result["region"]
    thana = api_result["thana"]
    union = api_result["union"]
    sector = api_result["sector"]
    lat = api_result["lat"]
    lon = api_result["lon"]
    coverage = api_result["coverage"]
    update = api_result["update"]
    loc = api_result["loc"]

    formatted_result = f'''📱 Number: {number}
🆔 IMEI: {imei}
📇 IMSI: {imsi}
🌍 Division: {division}
🏢 District: {district}
🗺️ Region: {region}
📍 Thana: {thana}
🌐 Union: {union}
🔍 Sector: {sector}
🗺️ Latitude: {lat}
🗺️ Longitude: {lon}
📡 Coverage: {coverage}
⏰ Last Update: {update}
🌍 Location: {loc}'''

    return formatted_result

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
