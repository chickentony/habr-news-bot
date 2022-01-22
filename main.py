import os
import logging

from app.bot import Bot

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    logging.getLogger(__name__)
    habr_news_bot = Bot(os.environ['BOT_TOKEN'])
    habr_news_bot.start_bot()
