import logging

from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update


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

    def start_bot(self) -> None:
        self.dispatcher.add_handler(CommandHandler('start', self.start_command))
        self.dispatcher.add_handler(CommandHandler('help', self.help_command))
        self.updater.start_polling()
        self.updater.idle()
