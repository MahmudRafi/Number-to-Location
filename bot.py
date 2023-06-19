import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import time

TOKEN = '5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8'
FREE_REQUEST_LIMIT = 2
FREE_REQUEST_DURATION = 12 * 60 * 60  # 12 hours in seconds

class User:
    def __init__(self, chat_id, is_premium=False, last_request_time=0, request_count=0):
        self.chat_id = chat_id
        self.is_premium = is_premium
        self.last_request_time = last_request_time
        self.request_count = request_count

users = {}

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
        user = users.get(chat_id)
        if user:
            if not user.is_premium and user.request_count >= FREE_REQUEST_LIMIT:
                # Send a message to get premium subscription
                message = f"⚠️ You have reached the limit of {FREE_REQUEST_LIMIT} free requests within {FREE_REQUEST_DURATION // 3600} hours. To continue using the service, please contact @Mahmud_Rafi to upgrade to premium subscription. You can request again after {time_left(user.last_request_time)} hours."
                context.bot.send_message(chat_id=update.effective_chat.id, text=message)
                return

            # Check the request time limit
            current_time = time.time()
            if current_time - user.last_request_time < FREE_REQUEST_DURATION:
                # Send a message indicating the remaining time
                message = f"⏳ You have recently made a request. Please wait for {time_left(user.last_request_time)} hours before making another request."
                context.bot.send_message(chat_id=update.effective_chat.id, text=message)
                return

            # Update the user's request count and time
            user.request_count += 1
            user.last_request_time = current_time
        else:
            # Create a new user entry
            user = User(chat_id, False, time.time(), 1)
            users[chat_id] = user

        api_url = f'https://api.cybersh.xyz/siminfo.php?key=ST&number={phone_number}'

        # Send the waiting message
        waiting_message = context.bot.send_message(chat_id=update.effective_chat.id, text="Finding 🧐")

        # Fetch the API response without SSL verification
        response = requests.get(api_url, verify=False)
        api_result = response.json()
        formatted_result = format_api_result(api_result, user.is_premium)

        # Delete the waiting message
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

        # Send the formatted result
        context.bot.send_message(chat_id=update.effective_chat.id, text=formatted_result)
    else:
        error_message = 'Invalid phone number! Please provide a valid Bangladeshi number starting with "01" and consisting of 11 digits. Ex. 01000000000'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

def format_api_result(api_result, is_premium):
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

    result_message = f'''📱 Number: {number}
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

    if is_premium:
        result_message = "🌟 Premium User 🌟\n\n" + result_message

    return result_message

def time_left(last_request_time):
    remaining_time = FREE_REQUEST_DURATION - (time.time() - last_request_time)
    hours = int(remaining_time // 3600)
    return hours

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
