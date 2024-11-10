from flask import Flask
import telebot

app = Flask(__name__)

# Directly use the token (ensure it's accurate)
bot = telebot.TeleBot("7186315620:AAFVqu98eT-7ivNGaTZVxeQgaXg8NeGxM_M")

# Function to handle incoming messages
@bot.message_handler(func=lambda message: True)
def Myfunc(message):
    print(f"Received message from {message.chat.id}: {message.text}")  # Log received messages
    bot.send_message(message.chat.id, "Hi, what's happening?")

if __name__ == '__main__':
    # Remove webhook and start polling
    bot.remove_webhook()
    print("Starting bot with long polling...")
    bot.infinity_polling()  # Bot will continuously poll for new updates
