from abc import ABC, abstractmethod
import logging

from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update
from telegram import ParseMode

from app.articles_parser import parse_habr_articles_content, get_habr_articles_html
from app.article import prepare_message_for_telegram

HABR_BASE_URL = 'https://habr.com'
HABR_QA_ARTICLES_URL = f'{HABR_BASE_URL}/ru/hub/it_testing/'


class BotCommandStrategy(ABC):
    @abstractmethod
    def bot_command(self, update: Update, context: CommandHandler, url: str):
        raise NotImplementedError


class ReplayCommand(BotCommandStrategy):
    @classmethod
    def bot_command(cls, update: Update, context: CallbackContext, url: str) -> None:
        html_data = get_habr_articles_html(url)
        articles = parse_habr_articles_content(html_data)
        message = prepare_message_for_telegram(articles)
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


class Bot:
    def __init__(self, bot_token: str):
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )
        logging.getLogger(__name__)
        self.updater = Updater(bot_token)
        self.dispatcher = self.updater.dispatcher

    @staticmethod
    def start_command(update: Update, _: CallbackContext) -> None:
        update.message.reply_text(
            'Бот помогает отслеживать свежие новости на HABR.\nСписок доступных команд - /help'
        )

    @staticmethod
    def help_command(update: Update, _: CallbackContext) -> None:
        update.message.reply_text(
            '/help - показать это сообщение'
        )

    @staticmethod
    def get_daily_testing_articles(update: Update, context: CallbackContext) -> None:
        ReplayCommand.bot_command(update, context, HABR_QA_ARTICLES_URL)

    def start_bot(self) -> None:
        self.dispatcher.add_handler(CommandHandler('start', self.start_command))
        self.dispatcher.add_handler(CommandHandler('help', self.help_command))
        self.dispatcher.add_handler(
            CommandHandler('get_daily_testing_news', self.get_daily_testing_articles)
        )
        self.updater.start_polling()
        self.updater.idle()
