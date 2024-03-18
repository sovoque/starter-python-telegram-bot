# Import necessary libraries
import os
import time
import telebot
from telebot import types

# Load bot token from bot_token.txt
with open("bot_token.txt", "r") as token_file:
    BOT_TOKEN = token_file.read().strip()

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Define a dictionary to store user messages and their corresponding photos
user_messages = {}

# Handle incoming photos, videos, and gifs
@bot.message_handler(content_types=["photo", "video", "document"])
def handle_media(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Store the message and its media in the dictionary
    user_messages[user_id] = message

    # Ask the user if they want to add text to the media
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Yes"), types.KeyboardButton("No"))
    bot.send_message(chat_id, "Do you want to add text to this media?", reply_markup=markup)

# Handle user response for adding text
@bot.message_handler(func=lambda message: message.text in ["Yes", "No"])
def handle_text_response(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id in user_messages:
        if message.text == "Yes":
            bot.send_message(chat_id, "Please type the text you want to add:")
        else:
            bot.send_message(chat_id, "Okay, I will publish the media without any additional text.")
            publish_media(user_id)

# Handle user response with text
@bot.message_handler(func=lambda message: user_id in user_messages and message.text)
def handle_text(message):
    user_id = message.from_user.id
    user_messages[user_id].caption = message.text
    bot.send_message(user_id, "I will publish the media with the added text in 1 minute.")
    publish_media(user_id)

# Publish media after 1 minute delay
def publish_media(user_id):
    chat_id = user_messages[user_id].chat.id
    media = user_messages[user_id].media
    bot.send_chat_action(chat_id, "upload_photo")
    time.sleep(60)  # 1 minute delay
    bot.send_media_group(chat_id, [media])
    bot.send_message(user_id, "Now she belongs to everyone in this group ;)")

# Ignore messages from specified chat_id
@bot.message_handler(func=lambda message: message.chat.id != 1001780824924)
def ignore_messages(message):
    pass

# Start the bot
if __name__ == "__main__":
    bot.polling(none_stop=True)
