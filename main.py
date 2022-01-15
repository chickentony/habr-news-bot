import os

from app.bot import Bot

if __name__ == '__main__':
    habr_news_bot = Bot(os.environ['BOT_TOKEN'])
    habr_news_bot.start_bot()
