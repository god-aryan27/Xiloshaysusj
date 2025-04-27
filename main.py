from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your bot token
TOKEN = '7405631437:AAGz6S5JJsZSECM9-Q6L7h4OG5gv0Z1vocs'

# Dictionary to store delay time (in seconds)
delete_delay = 5 * 60  # Default 5 minutes

# Handle /setDela command
def set_dela(update: Update, context: CallbackContext):
    global delete_delay
    try:
        minutes = int(context.args[0])
        delete_delay = minutes * 60  # Convert minutes to seconds
        update.message.reply_text(f"Messages will now be deleted after {minutes} minute(s).")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /setDela <minutes>")

# Handle new channel messages
def handle_new_message(update: Update, context: CallbackContext):
    message = update.message
    chat_id = message.chat_id
    message_id = message.message_id

    # Schedule deletion after the set delay
    context.job_queue.run_once(delete_post, delete_delay, context=(chat_id, message_id))

# Delete the message
def delete_post(context: CallbackContext):
    chat_id, message_id = context.job.context
    try:
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Add command and message handlers
    dispatcher.add_handler(CommandHandler("setDela", set_dela))
    dispatcher.add_handler(MessageHandler(Filters.chat_type.channel, handle_new_message))

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
