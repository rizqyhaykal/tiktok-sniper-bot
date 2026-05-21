import requests
import re
import time
import os

username = "celanasepuluhrebu"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

url = f"https://www.tiktok.com/@{username}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

last_followers = None
target_reached = False
last_update_id = 0


def send_telegram(message):

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(telegram_url, data=payload)


def initialize_updates():

    global last_update_id

    updates_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    response = requests.get(updates_url).json()

    if "result" in response and len(response["result"]) > 0:

        last_update_id = response["result"][-1]["update_id"]


def check_stop_command():

    global last_update_id

    updates_url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}"
    )

    response = requests.get(updates_url).json()

    if "result" in response:

        for item in response["result"]:

            last_update_id = item["update_id"]

            try:

                text = item["message"]["text"]

                if text.upper() == "STOP":
                    return True

            except:
                pass

    return False


initialize_updates()

while True:

    try:

        response = requests.get(url, headers=headers)

        html = response.text

        match = re.search(r'"followerCount":(\d+)', html)

        if match:

            followers = match.group(1)

            current_time = time.strftime("%H:%M:%S")

            print(f"[{current_time}] Followers: {followers}")

            if last_followers != followers and last_followers is not None:

                alert = f"🚨 FOLLOWER COUNT CHANGED 🚨\n\n{last_followers} → {followers}"

                print(alert)

                send_telegram(alert)

            if int(followers) >= 76 and not target_reached:

                print("🚨🚨 TARGET REACHED 🚨🚨")

                while True:

                    send_telegram(
                        "🚨🚨 FOLLOWERS TARGET TERCAPAI 🚨🚨\n\nBURUAN SCREENSHOT DAN DM SEKARANG!\n\nKetik STOP untuk menghentikan spam."
                    )

                    print("SPAM SENT")

                    time.sleep(1)

                    if check_stop_command():

                        send_telegram("✅ Spam dihentikan.")

                        print("SPAM STOPPED")

                        break

                target_reached = True

            last_followers = followers

        else:
            print("Follower count not found")

    except Exception as e:

        print("ERROR:", e)

    time.sleep(4)
