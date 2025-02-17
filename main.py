import telegram
from telegram.ext import Application, CommandHandler
import requests
from bs4 import BeautifulSoup
import time
import asyncio

# Dein Telegram Bot-Token (von BotFather)
TOKEN = "7675408964:AAGnnUsKLJ29B_FzMtQ8WsUksmiIKgWS9bw"

# Deine Telegram-Chat-ID
CHAT_ID = "5738627127"

# Die richtige Login-URL von BullXNeo (bleibt immer gleich)
LOGIN_URL = "https://neo.bullx.io/login"

# Dein BullX-Session-Cookie (aus den Entwicklertools ausgelesen)
SESSION_COOKIE = "eyJhbGciOiJIUz1NilsinR5cCI6IkpXVCJ9.eyJ1c2VySWQiOilw..."  # Hier den echten Wert einfügen

# Telegram-Bot initialisieren
bot = telegram.Bot(token=TOKEN)

# Funktion zum Abrufen von Trend-MemeCoins
def get_trending_coins():
    headers = {
        "Cookie": f"bullx-session-t={SESSION_COOKIE}".encode("utf-8").decode("utf-8"),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    
    response = requests.get(LOGIN_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    coins = []
    for coin in soup.find_all("div", class_="coin-card"):  # Falls die Klasse anders heißt, anpassen!
        name = coin.find("h2").text.strip()  # Coin-Name
        price_change = coin.find("span", class_="price-change").text.strip("%")  # Preisänderung

        if float(price_change) > 20:  # Falls der Coin stark ansteigt (>20%)
            coins.append(f"{name} 🚀 +{price_change}%")

    return coins

# Telegram-Benachrichtigung senden (asynchron)
async def send_alert():
    coins = get_trending_coins()
    if coins:
        message = "🚀 Neue Trend-MemeCoins:\n" + "\n".join(coins)
    else:
        message = "❌ Keine neuen Trend-Coins gefunden."
    
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Automatische Überprüfung alle 5 Minuten
async def main():
    while True:
        await send_alert()
        await asyncio.sleep(300)  # Alle 5 Minuten prüfen

if __name__ == "__main__":
    asyncio.run(main())
