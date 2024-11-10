from flask import Flask, request
import telebot

app = Flask(__name__)

# Directly use the token (be cautious with sensitive data in production)
bot = telebot.TeleBot("7186315620:AAFVqu98eT-7ivNGaTZVxeQgaXg8NeGxM_M")

@app.route('/set_app', methods=['GET'])
def set_app():
    # Optional route if you need to set up the webhook for production use
    bot.remove_webhook()
    webhook_url = "https://" + request.host + "/bot_webhook"
    bot.set_webhook(url=webhook_url)
    return f'Webhook set to {webhook_url}', 200

@bot.message_handler(func=lambda message: True)
def Myfunc(message):
    bot.send_message(message.chat.id, "Hi, what's happening?")

if __name__ == '__main__':
    # Remove the webhook and switch to polling
    bot.remove_webhook()
    print("Starting bot with long polling...")
    bot.infinity_polling()  # Bot will continuously poll for new updates
