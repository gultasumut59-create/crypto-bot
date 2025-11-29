import feedparser
from telegram.ext import Application, ContextTypes
from collections import defaultdict

TOKEN = "8019801672:AAFe9ISAA4lJoEAEjYQYtQ5Fh1imJgtE_v0"
CHANNEL_ID = "@AnlikKriptoRadar"

# Her RSS kaynağı için son gönderilen haber linki
son_gonderilen_haber = defaultdict(str)

# RSS siteleri listesi
rss_listesi = [
    "https://kriptokoin.com/feed",
    "https://www.yatirimrehberi.com.tr/rss/kripto",
    "https://www.yatirimrehberi.com.tr/rss/piyasalar",
    "https://www.kriptofoni.com/altcoin-haberleri/feed/"
]

async def otomatik_haber(context: ContextTypes.DEFAULT_TYPE):
    for rss in rss_listesi:
        feed = feedparser.parse(rss)
        if feed.entries:
            latest = feed.entries[0]  # en yeni haber
            # Eğer bu haber daha önce gönderilmemişse
            if latest.link != son_gonderilen_haber[rss]:
                mesaj = f"{latest.title}\n{latest.link}"
                await context.bot.send_message(chat_id=CHANNEL_ID, text=mesaj)
                print(f"Haber gönderildi: {latest.title}")
                son_gonderilen_haber[rss] = latest.link  # kaydet
            else:
                print(f"Yeni haber yok: {rss}")
        else:
            print(f"RSS boş veya erişilemedi: {rss}")

def main():
    app = Application.builder().token(TOKEN).build()
    jq = app.job_queue
    jq.run_repeating(otomatik_haber, interval=30, first=0)  # test için 30 saniye
    app.run_polling()

if __name__ == "__main__":
    main()
