import telebot
import requests
import time

# 🔴 REPLACE THESE WITH YOUR NEW KEYS (DO NOT SHARE THEM)
BOT_TOKEN = "7908025680:AAE9UbmSlQKSPzixHIBZa0Bs0rTvAC2R_EI"
OPENAI_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)

# Function to get AI responses from OpenAI
def get_ai_response(user_message):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_message}]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()
        if "error" in response_json:
            return f"⚠️ OpenAI Error: {response_json['error']['message']}"
        return response_json["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"⚠️ Network Error: {e}"
    except Exception as e:
        return "⚠️ Sorry, I couldn't process that right now."

# Welcome new users
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for new_member in message.new_chat_members:
        bot.reply_to(message, f"🎉 Welcome {new_member.first_name} to the group!")

# AI Chat Handler
@bot.message_handler(func=lambda message: True)
def chat_with_users(message):
    user_text = message.text
    reply = get_ai_response(user_text)
    bot.reply_to(message, reply)
    time.sleep(1)  # Prevents Telegram rate limits

# Keep bot running, restart if it crashes
while True:
    try:
        print("🚀 Bot is running with AI...")
        bot.infinity_polling(timeout=3, long_polling_timeout=3)
    except Exception as e:
        print(f"⚠️ Bot crashed: {e}")
        time.sleep(5)  # Wait before restarting
