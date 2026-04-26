import time
import requests

BOT_TOKEN = "6470289113:AAEe6xqDZV_2iP4R8Pap7o0Z18hBd8W5KA0"
CHAT_ID = "6356683286"
UID = "u-s4t2ud-15be722c3ec86325e5c83f46aad08d5b77a044be10e2a9ec87c76770fbedb31e"
SECRET = "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"


access_token = None
expires_at = 0

def get_access_token():
    global access_token, expires_at
    url = "https://api.intra.42.fr/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": UID,
        "client_secret": SECRET
    }
    r = requests.post(url, data=data)
    j = r.json()
    access_token = j["access_token"]
    expires_at = time.time() + j["expires_in"] - 30

def api_get_pending():
    global access_token, expires_at
    if access_token is None or time.time() >= expires_at:
        get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(
        "https://api.intra.42.fr/v2/me/scale_teams?filter[status]=waiting",
        headers=headers
    )
    return len(r.json())

def send_msg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

last = -1

while True:
    try:
        count = api_get_pending()
        if last != -1 and count > last:
            send_msg(f"Новая pending evaluation! Сейчас их: {count}")
        last = count
    except Exception as e:
        print("Ошибка:", e)
    time.sleep(30)
