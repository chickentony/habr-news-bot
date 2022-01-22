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
    def bot_command(self, update: Update, context: CallbackContext, url: str):
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
        empty_search_result_text = 'Статей не найдено'
        html_data = get_habr_articles_html(url)
        articles = parse_habr_articles_content(html_data)
        message = prepare_message_for_telegram(articles)
        if not message:
            logging.info('Send message with empty search result text')
            update.message.reply_text(empty_search_result_text)
        else:
            logging.info('Send message with articles to user')
            update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


class SearchCommandStrategy(BotCommandStrategy):

    @classmethod
    def bot_command(cls, update: Update, context: CallbackContext, url: str) -> None:
        empty_search_result_text = 'Ничего не найдено по вашему запросу'
        user_query_words_list = context.args
        if not user_query_words_list:
            raise AttributeError

        user_query = ' '.join(user_query_words_list)
        search_url = f'{url}{user_query}'
        html_data = get_habr_articles_html(search_url)
        articles = parse_habr_articles_content(html_data)
        message = prepare_message_for_telegram(articles)

        if not message:
            logging.info('Send message with empty search result text')
            update.message.reply_text(empty_search_result_text)
        else:
            logging.info('Send message with articles to user')
            update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)


class Bot:
    """Main bot class with all commands and actions"""

    def __init__(self, bot_token: str):
        """
        Init method.

        :param bot_token: telegram bot token. More info - https://core.telegram.org/bots/api
        """
        self.updater = Updater(bot_token)
        self.dispatcher = self.updater.dispatcher

    @staticmethod
    def start_command(update: Update, _: CallbackContext) -> None:
        """
        Text message replaying on /start command.

        :param update: telegram.ext Updater class, required param for command
        :param _: telegram.ext CallbackContext class, required param for command
        """
        logging.info('Subscribe on bot')
        update.message.reply_text(
            'Бот помогает отслеживать свежие новости на HABR.\nСписок доступных команд - /help'
        )

    @staticmethod
    def help_command(update: Update, _: CallbackContext) -> None:
        """
        Text message replaying on /help command.
        Contains all possible bot commands and there descriptions.

        :param update: telegram.ext Updater class, required param for command
        :param _: telegram.ext CallbackContext class, required param for command
        """
        logging.info('Calling "/help" command')
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
        logging.info('Start parsing habr website for testing articles')
        ReplayCommandStrategy.bot_command(
            update,
            context,
            config['habr_articles_about_testing_url']
        )
        logging.info('Finish parsing habr website')

    @staticmethod
    def get_python_articles(update: Update, context: CallbackContext) -> None:
        """
        Get fresh articles about python from habr.
        This is articles from first page https://habr.com/ru/hub/python/

        :param update: telegram.ext Updater class, required param for command
        :param context: telegram.ext CallbackContext class, required param for command
        """
        logging.info('Start parsing habr website for python articles')
        ReplayCommandStrategy.bot_command(
            update,
            context,
            config['habr_articles_about_python_url']
        )
        logging.info('Finish parsing habr website')

    @staticmethod
    def search_articles(update: Update, context: CallbackContext) -> None:
        logging.info('Start parsing habr website for searching articles')
        SearchCommandStrategy.bot_command(
            update,
            context,
            config['habr_articles_search_url']
        )
        logging.info('Finish parsing habr website')

    def start_bot(self) -> None:
        """Bot entrypoint. Add all commands and launch bot"""
        logging.info('Starting bot instance...')
        self.dispatcher.add_handler(CommandHandler('start', self.start_command))
        self.dispatcher.add_handler(CommandHandler('help', self.help_command))
        self.dispatcher.add_handler(
            CommandHandler('get_testing_news', self.get_testing_articles)
        )
        self.dispatcher.add_handler(
            CommandHandler('get_python_news', self.get_python_articles)
        )
        self.dispatcher.add_handler(
            CommandHandler('search_articles', self.search_articles)
        )
        self.updater.start_polling()
        self.updater.idle()
