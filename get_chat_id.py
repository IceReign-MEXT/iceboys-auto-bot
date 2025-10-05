import requests

BOT_TOKEN = "8398239711:AAEOq44XzZ5m8O3KcHXQdPAUbISjbeLCtzE"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    if "result" in data and len(data["result"]) > 0:
        for update in data["result"]:
            chat = update.get("message", {}).get("chat") or update.get("channel_post", {}).get("chat")
            if chat:
                print(f"Chat title: {chat.get('title')}")
                print(f"Chat ID: {chat.get('id')}")
                print("-" * 40)
    else:
        print("⚠️ No updates yet. Send a message to your bot or channel first.")
else:
    print("❌ Error reaching Telegram API:", response.text)
