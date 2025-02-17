import telegram
from telegram.ext import Application, CommandHandler
import requests
from bs4 import BeautifulSoup
import time
import asyncio

# Dein Telegram Bot-Token
TOKEN = "7675408964:AAGnnUsKLJ29B_FzMtQ8WsUksmiIKgWS9bw"

# Deine Telegram-Chat-ID
CHAT_ID = "5738627127"

# Die richtige Login-URL von BullXNeo (die immer gleich bleibt)
LOGIN_URL = "https://neo.bullx.io/login?address=0x07db81bf8159654acb168a18afdc2e994db4e4f8&signature=0x926203b961ce5d1f7669e08898ebdd3743f5d303f2647d406ee953a8d1fd9c5675821626677fbd187d1a4994"

# Telegram-Bot initialisieren
bot = telegram.Bot(token=TOKEN)

# Funktion zum Abrufen von Trend-MemeCoins
def get_trending_coins():
    response = requests.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    coins = []
    
    # 🔹 Anpassung: Suche nach Coin-Daten im HTML (Je nach Struktur evtl. ändern)
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
