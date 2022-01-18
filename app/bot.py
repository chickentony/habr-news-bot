from abc import ABC, abstractmethod
import logging

from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update
from telegram import ParseMode

from app.articles_parser import parse_habr_articles_content, get_habr_articles_html
from app.article import prepare_message_for_telegram
from app.helpers import parse_config

PATH_TO_CONFIG_FILE = 'config.yaml'
config = parse_config(PATH_TO_CONFIG_FILE)


class BotCommandStrategy(ABC):
    """Strategy pattern class for different bot commands"""

    @abstractmethod
    def bot_command(self, update: Update, context: CommandHandler, url: str):
        raise NotImplementedError


class ReplayCommandStrategy(BotCommandStrategy):
    """Strategy for prompt reaction"""

    @classmethod
    def bot_command(cls, update: Update, context: CallbackContext, url: str) -> None:
        """
        Command realisation. Takes habr page with provided url, parse it and prepare message with
        articles data: title, link, views and rating

        :param update: telegram.ext Updater class
        :param context: telegram.ext CallbackContext class
        :param url: url to habr section
        """
        html_data = get_habr_articles_html(url)
        articles = parse_habr_articles_content(html_data)
        message = prepare_message_for_telegram(articles)
        update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


class Bot:
    """Main bot class with all commands and actions"""

    def __init__(self, bot_token: str):
        """
        Init method.

        :param bot_token: telegram bot token. More info - https://core.telegram.org/bots/api
        """
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
        """
        Text replaying on /start command.

        :param update: telegram.ext Updater class, required param for command
        :param _: telegram.ext CallbackContext class, required param for command
        """
        update.message.reply_text(
            'Бот помогает отслеживать свежие новости на HABR.\nСписок доступных команд - /help'
        )

    @staticmethod
    def help_command(update: Update, _: CallbackContext) -> None:
        """
        Text replaying on /help command. Contains all possible bot commands and there descriptions.

        :param update: telegram.ext Updater class, required param for command
        :param _: telegram.ext CallbackContext class, required param for command
        """
        update.message.reply_text(
            '/help - показать это сообщение\n'
            '/get_testing_news - получить список свежих статей про тестирование\n'
            '/get_python_news - получить список свежих статей про python\n'
        )

    @staticmethod
    def get_testing_articles(update: Update, context: CallbackContext) -> None:
        """
        Get fresh articles about testing from habr.
        This is articles from first page https://habr.com/ru/hub/it_testing/

        :param update: telegram.ext Updater class, required param for command
        :param context: telegram.ext CallbackContext class, required param for command
        """
        ReplayCommandStrategy.bot_command(
            update,
            context,
            config['habr_articles_about_testing_url']
        )

    @staticmethod
    def get_python_articles(update: Update, context: CallbackContext) -> None:
        """
        Get fresh articles about python from habr.
        This is articles from first page https://habr.com/ru/hub/python/

        :param update: telegram.ext Updater class, required param for command
        :param context: telegram.ext CallbackContext class, required param for command
        """
        ReplayCommandStrategy.bot_command(
            update,
            context,
            config['habr_articles_about_python_url']
        )

    def start_bot(self) -> None:
        """Bot entrypoint. Add all commands and launch bot"""
        self.dispatcher.add_handler(CommandHandler('start', self.start_command))
        self.dispatcher.add_handler(CommandHandler('help', self.help_command))
        self.dispatcher.add_handler(
            CommandHandler('get_testing_news', self.get_testing_articles)
        )
        self.dispatcher.add_handler(
            CommandHandler('get_python_news', self.get_python_articles)
        )
        self.updater.start_polling()
        self.updater.idle()
