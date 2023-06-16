import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import json

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

        # Send the waiting message
        waiting_message = context.bot.send_message(chat_id=update.effective_chat.id, text="Finding 🧐")

        # Fetch the API response
        response = requests.get(api_url)
        api_result = response.json()
        formatted_result = format_api_result(api_result)

        # Delete the waiting message
        context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

        # Send the formatted result
        context.bot.send_message(chat_id=update.effective_chat.id, text=formatted_result)
    else:
        error_message = 'Invalid phone number! Please provide a valid Bangladeshi number starting with "01" and consisting of 11 digits.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)


def format_api_result(api_result):
    if 'User_IMEI' in api_result:
        imei = api_result['User_IMEI']
    else:
        imei = 'Not available'

    if 'User_IMSI' in api_result:
        imsi = api_result['User_IMSI']
    else:
        imsi = 'Not available'

    if 'User_date_last_action' in api_result:
        last_action_date = api_result['User_date_last_action']
    else:
        last_action_date = 'Not available'

    if 'User_time_last_action' in api_result:
        last_action_time = api_result['User_time_last_action']
    else:
        last_action_time = 'Not available'

    if 'User_SECTOR_NAME' in api_result:
        sector_name = api_result['User_SECTOR_NAME']
    else:
        sector_name = 'Not available'

    if 'User_UNION_NAME' in api_result:
        union_name = api_result['User_UNION_NAME']
    else:
        union_name = 'Not available'

    if 'User_THANA' in api_result:
        thana = api_result['User_THANA']
    else:
        thana = 'Not available'

    if 'User_DISTRICT' in api_result:
        district = api_result['User_DISTRICT']
    else:
        district = 'Not available'

    if 'User_DIVISON' in api_result:
        division = api_result['User_DIVISON']
    else:
        division = 'Not available'

    if 'User_LOC_LONG' in api_result:
        loc_long = api_result['User_LOC_LONG']
    else:
        loc_long = 'Not available'

    if 'User_LOC_LAT' in api_result:
        loc_lat = api_result['User_LOC_LAT']
    else:
        loc_lat = 'Not available'

    formatted_result = f'''📱 User_IMEI: {imei}
🆔 User_IMSI: {imsi}
📅 User_last_action_date: {last_action_date}
🕒 User_last_action_time: {last_action_time}
📍 User_sector_name: {sector_name}
🌐 User_union_name: {union_name}
📍 User_thana: {thana}
🏢 User_district: {district}
🌍 User_division: {division}
🗺️ User_loc_long: {loc_long}
🗺️ User_loc_lat: {loc_lat}'''

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
