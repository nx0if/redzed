import telebot
import requests
import time
from datetime import datetime

TOKEN = "7186315620:AAHcMIVq8u0y9HpqmoBGjAKGuLyosO68A3c"
bot = telebot.TeleBot(TOKEN)

admins = [6033616268]
group_active = {}
user_spam_counts = {}
user_like_counts = {}
user_last_used = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        """🤔 Bot commands:

-/spam <uid> : Send friend invites
-/like <uid> : Send likes
-/visit <uid> : Send visitors
-/search <name> : Search account by name
-/info <uid> : Get player info

💡 EXAMPLES:

/spam 12345678
/like 12345678
/visit 12345678
/search mohp4
/info 12345678

Bot Developer : @mohp4

https://t.me/xiters911group"""
    )

@bot.message_handler(commands=['spam'])
def handle_spam(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not group_active.get(chat_id, False):
        bot.reply_to(message, "The bot is not activated in this group. Use /RED to activate it.")
        return

    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "Please provide the player ID after the /spam command")
        return

    player_ids = parts[1:]

    if user_id not in admins:
        if user_id not in user_spam_counts:
            user_spam_counts[user_id] = 0

        if user_spam_counts[user_id] + len(player_ids) > 999:
            bot.reply_to(message, "You can enter only 999 player IDs per day.")
            return

        user_spam_counts[user_id] += len(player_ids)

    waiting_message = bot.reply_to(message, f"Sending friend requests to player IDs: {', '.join(player_ids)}...")

    # Start spam process
    number_of_invites = 5
    for player_id in player_ids:
        for i in range(number_of_invites):
            api_url = f"https://mr3skr-friend-api-l3x3.onrender.com/request?api_key=DHDH3SKR555SShqQryykeyfff&uid={player_id}"
            try:
                response = requests.get(api_url)
                if response.status_code != 200:
                    bot.reply_to(message, f"Failed to send friend request to {player_id} number {i + 1}. Please try again.")
            except requests.exceptions.RequestException as e:
                bot.reply_to(message, f"Connection error: {str(e)}")

            time.sleep(1)

        # Get player info after spam
        info_api_url = f"https://mr-3skr-api-info.onrender.com/{player_id}"
        try:
            info_response = requests.get(info_api_url)
            if info_response.status_code == 200:
                data = info_response.json()
                basicinfo = data.get("basicinfo", [{}])[0]

                # Create the message to reply to the user
                player_info_message = (
                    f"NAME: {basicinfo.get('username', 'Unknown')}\n"
                    f"UID: {player_id}\n"
                    f"LVL: {basicinfo.get('level', 'N/A')}\n"
                    f"REGION: {basicinfo.get('region', 'N/A')}\n\n"
                    "Bot Developer : @mohp4\n\n"
                    "https://t.me/+0x64vi41KVdlODc0"
                )
                # Reply to the user with the player info
                bot.reply_to(message, player_info_message)
            else:
                bot.reply_to(message, "Failed to retrieve player info.")
        except requests.exceptions.RequestException as e:
            bot.reply_to(message, f"Error fetching player info: {str(e)}")

    bot.delete_message(chat_id, waiting_message.message_id)



@bot.message_handler(commands=['like'])
def handle_like(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not group_active.get(chat_id, False):
        bot.reply_to(message, "The bot is not activated in this group. Use /RED to activate it.")
        return

    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "Please enter the command correctly: /like [player_id]")
        return

    player_id = parts[1]
    current_date = datetime.now().date()

    if user_id not in admins:
        if user_id not in user_like_counts:
            user_like_counts[user_id] = 0
            user_last_used[user_id] = current_date

        if user_last_used[user_id] != current_date:
            user_like_counts[user_id] = 0
            user_last_used[user_id] = current_date

        if user_like_counts[user_id] >= 100:
            bot.reply_to(message, "You can send likes to only 100 player IDs per day.")
            return

        user_like_counts[user_id] += 1

    waiting_message = bot.reply_to(message, f"Sending likes to player ID: {player_id}...")

    api_url = f"https://likes-new-api-mr-3skr.onrender.com/like?uid={player_id}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data.get('likes_added') == 0:
            	bot.reply_to(message, ('You Can Send Likes Only Every 24hours..'))
            else:
            	bot.reply_to(message, (
                f"🎉 Likes Sent Successfully!\n\n"
                f"Account Name: {data.get('name', 'Unknown')}\n"
                f"UID: {data.get('uid')}\n"
                f"Level: {data.get('level', 'N/A')}\n"
                f"Likes Before: {data.get('likes_before', 'N/A')}\n"
                f"Likes After: {data.get('likes_after', 'N/A')}\n"
                f"Likes Added: {data.get('likes_added', 'N/A')}\n"
                f"Region: {data.get('failed_likes_region', 'N/A')}\n"
                "--------------------\n\n"
                "لتفعيل البوت في مجموعتك، تواصل مع:\n\n"
                "@mohp4\n"
                "https://t.me/xiters911group"))
        else:
            bot.reply_to(message, "Failed to send likes. Please try again.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Connection error: {str(e)}")

    bot.delete_message(chat_id, waiting_message.message_id)

@bot.message_handler(commands=['visit'])
def handle_visit(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not group_active.get(chat_id, False):
        bot.reply_to(message, "The bot is not activated in this group. Use /RED to activate it.")
        return

    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "Please enter the command correctly: /visit [player_id]")
        return

    player_id = parts[1]
    api_url = f"https://mr-3skr-api-x-3.onrender.com/visit/uid={player_id}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            bot.reply_to(message, f"Visitors sent to UID: {player_id}")
        else:
            bot.reply_to(message, "Failed to send visitors. Please try again.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Connection error: {str(e)}")

@bot.message_handler(commands=['search'])
def handle_search(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "Please enter the command correctly: /search [name]")
        return

    name = parts[1]
    api_url = f"https://mr-3skr-api-ofc.onrender.com/search?name={name}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            bot.reply_to(message, f"Search Results:\n\n\n\n{data.get('result', 'No results found')}")
        else:
            bot.reply_to(message, "Failed to search. Please try again.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Connection error: {str(e)}")

@bot.message_handler(commands=['info'])
def handle_info(message):
    chat_id = message.chat.id
    if not group_active.get(chat_id, False):
        bot.reply_to(message, "The bot is not activated in this group. Use /RED to activate it.")
        return

    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "Please enter the command correctly: /info [uid]")
        return

    uid = parts[1]
    api_url = f"https://mr-3skr-api-info.onrender.com/{uid}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            basicinfo = data.get("basicinfo", [{}])[0]
            clanadmin = data.get("clanadmin", [{}])[0]
            claninfo = data.get("claninfo", [{}])[0]

            account_created = datetime.utcfromtimestamp(basicinfo.get("createat", 0)).strftime('%Y-%m-%d %H:%M:%S')
            last_login = datetime.utcfromtimestamp(basicinfo.get("lastlogin", 0)).strftime('%Y-%m-%d %H:%M:%S')
            admin_last_login = datetime.utcfromtimestamp(clanadmin.get("lastlogin", 0)).strftime('%Y-%m-%d %H:%M:%S')

            message_text = (
                f"📋 Basic Info:\n"
                f" - Username: {basicinfo.get('username', 'N/A')}\n"
                f" - Level: {basicinfo.get('level', 'N/A')}\n"
                f" - Exp: {basicinfo.get('Exp', 'N/A')}\n"
                f" - Badge Count: {basicinfo.get('BadgeCount', 'N/A')}\n"
                f" - OB: {basicinfo.get('OB', 'N/A')}\n"
                f" - Avatar ID: {basicinfo.get('avatar', 'N/A')}\n"
                f" - Banner ID: {basicinfo.get('banner', 'N/A')}\n"
                f" - Bio: {basicinfo.get('bio', 'N/A')}\n"
                f" - Rank Points (BR): {basicinfo.get('brrankpoint', 'N/A')}\n"
                f" - Rank Score (BR): {basicinfo.get('brrankscore', 'N/A')}\n"
                f" - Rank Points (CS): {basicinfo.get('csrankpoint', 'N/A')}\n"
                f" - Rank Score (CS): {basicinfo.get('csrankscore', 'N/A')}\n"
                f" - Likes: {basicinfo.get('likes', 'N/A')}\n"
                f" - Region: {basicinfo.get('region', 'N/A')}\n"
                f" - Account Created At: {account_created}\n"
                f" - Last Login: {last_login}\n\n"

                f"👥 Clan Admin:\n"
                f" - Admin Name: {clanadmin.get('adminname', 'N/A')}\n"
                f" - Level: {clanadmin.get('level', 'N/A')}\n"
                f" - BR Points: {clanadmin.get('brpoint', 'N/A')}\n"
                f" - CS Points: {clanadmin.get('cspoint', 'N/A')}\n"
                f" - Experience: {clanadmin.get('exp', 'N/A')}\n"
                f" - Admin ID: {clanadmin.get('idadmin', 'N/A')}\n"
                f" - Last Login: {admin_last_login}\n\n"

                f"🏆 Clan Info:\n"
                f" - Clan ID: {claninfo.get('clanid', 'N/A')}\n"
                f" - Clan Name: {claninfo.get('clanname', 'N/A')}\n"
                f" - Clan Level: {claninfo.get('guildlevel', 'N/A')}\n"
                f" - Live Members: {claninfo.get('livemember', 'N/A')}\n"
            )

            bot.reply_to(message, message_text)
        else:
            bot.reply_to(message, "Failed to retrieve information. Please try again.")
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, f"Connection error: {str(e)}")

@bot.message_handler(commands=['RED'])
def amin_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id in admins:
        group_active[chat_id] = True
        bot.reply_to(message, "Bot activated in this group. You can now use commands.")
    else:
        bot.reply_to(message, "This command is only available to admins.")

while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"Bot polling encountered an error: {e}")
        time.sleep(15)
