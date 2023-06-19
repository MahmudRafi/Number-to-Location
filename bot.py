import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json
import time

TOKEN = '5933571161:AAHjX1sBG0mlEwQXVXFJUxoQwEGtkotW-J8'
FREE_REQUEST_DURATION = 12 * 60 * 60  # 12 hours in seconds
PREMIUM_CHAT_IDS_URL = 'https://raw.githubusercontent.com/MahmudRafi/hudaihudai/main/chat_ids.txt'

class User:
    def __init__(self, chat_id, is_premium, last_request_time, request_count):
        self.chat_id = chat_id
        self.is_premium = is_premium
        self.last_request_time = last_request_time
        self.request_count = request_count

users = {}

def fetch_premium_chat_ids():
    response = requests.get(PREMIUM_CHAT_IDS_URL)
    chat_ids = response.text.strip().split('\n')
    return chat_ids

def start(update, context):
    welcome_message = '''🤖📱 Welcome! I'm the "Number Locator" Bot! Please provide a phone number for investigation like "01*********".
Remember, the number should be from Airtel or Robi. Let's uncover its location! 🌍🔍
Developer @Mahmud_Rafi'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

def handle_message(update, context):
    phone_number = update.message.text.strip()
    if phone_number.startswith('01') and len(phone_number) == 11:
        chat_id = str(update.effective_chat.id)

        current_time = time.time()

        if chat_id in users:
            user = users[chat_id]

            if not user.is_premium and user.request_count >= 2 and current_time - user.last_request_time < FREE_REQUEST_DURATION:
                # Calculate the time left until the user can make another request
                seconds_left = int(FREE_REQUEST_DURATION - (current_time - user.last_request_time))
                hours_left = seconds_left // 3600
                minutes_left = (seconds_left % 3600) // 60

                # Send a message with countdown animation
                countdown_animation = f"⏳ Please wait for {hours_left} hours and {minutes_left} minutes before making another request."

                # Send the waiting message
                waiting_message = context.bot.send_message(chat_id=update.effective_chat.id, text=countdown_animation)

                # Animate the countdown message
                for minutes in range(int(hours_left * 60 + minutes_left), 0, -1):
                    minutes_left = minutes % 60
                    hours_left = minutes // 60
                    countdown_animation = f"⏳ Please wait for {hours_left} hours and {minutes_left} minutes before making another request."
                    context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=waiting_message.message_id, text=countdown_animation)
                    time.sleep(60)

                # Delete the countdown animation message
                context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

            # Update the user's last request time and request count
            user.last_request_time = current_time
            user.request_count += 1
        else:
            is_premium = chat_id in premium_chat_ids
            # Create a new user entry
            user = User(chat_id, is_premium=is_premium, last_request_time=current_time, request_count=1)
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

        if not user.is_premium:
            # Send the chat ID message
            chat_id_message = f"This is your Chat ID: {chat_id}, copy this chat ID and send this to @Mahmud_Rafi to be premium."
            context.bot.send_message(chat_id=update.effective_chat.id, text=chat_id_message)
    else:
        error_message = 'Invalid phone number! Please provide a valid Bangladeshi number starting with "01" and consisting of 11 digits. Ex. 01000000000'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

def format_api_result(api_result, is_premium):
    if 'siminfo' in api_result:
        sim_info = api_result['siminfo']

        number = sim_info.get('number', 'Not available')
        imei = sim_info.get('imei', 'Not available')
        imsi = sim_info.get('imsi', 'Not available')
        division = sim_info.get('division', 'Not available')
        district = sim_info.get('district', 'Not available')
        region = sim_info.get('region', 'Not available')
        thana = sim_info.get('thana', 'Not available')
        union = sim_info.get('union', 'Not available')
        sector = sim_info.get('sector', 'Not available')
        lat = sim_info.get('lat', 'Not available')
        lon = sim_info.get('lon', 'Not available')
        coverage = sim_info.get('coverage', 'Not available')
        update = sim_info.get('update', 'Not available')

        google_maps_link = get_google_maps_link(lat, lon)

        # Add premium user indication
        if is_premium:
            user_type = 'Premium User 🌟'
        else:
            user_type = 'Free User'

        formatted_result = f'''📱 Number: {number}
🌟 User Type: {user_type}
🆔 IMEI: {imei}
🆔 IMSI: {imsi}
🌍 Division: {division}
🏢 District: {district}
🌐 Region: {region}
📍 Thana: {thana}
🌆 Union: {union}
🏙️ Sector: {sector}
🌍 Coverage: {coverage}
🕒 Update: {update}
🗺️ Google Maps: {google_maps_link}'''

        return formatted_result

    return 'No information available for the provided number.'

def get_google_maps_link(lat, lon):
    return f'https://google.com/maps/search/?api=1&query={lat},{lon}'

def main():
    global premium_chat_ids
    premium_chat_ids = fetch_premium_chat_ids()

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Define handlers
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)

    # Add handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(message_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
