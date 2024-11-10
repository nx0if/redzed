from flask import Flask, request
import telebot

app = Flask(__name__)

# Directly use the token (be cautious with sensitive data in production)
bot = telebot.TeleBot("7186315620:AAFVqu98eT-7ivNGaTZVxeQgaXg8NeGxM_M")

@app.route('/bot_webhook', methods=['POST'])
def bot_webhook():
    json_data = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return 'OK', 200

@app.route('/set_app', methods=['GET'])
def set_app():
    bot.remove_webhook()
    webhook_url = "https://" + request.host + "/bot_webhook"
    bot.set_webhook(url=webhook_url)
    return f'Webhook set to {webhook_url}', 200

@bot.message_handler(func=lambda message: True)
def Myfunc(message):
    bot.send_message(message.chat.id, "Hi, what's happening?")

if __name__ == '__main__':
    # Enable threading for handling multiple requests
    app.run(debug=True, threaded=True)
