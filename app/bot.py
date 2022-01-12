import logging

from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update

from app.articles_parser import parse_habr_articles_content, get_habr_articles_html
from app.article import prepare_message_for_telegram


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
    def process_habr_articles_parsing(context: CallbackContext):
        html_data = get_habr_articles_html(context.job.context['url'])
        articles = parse_habr_articles_content(html_data)
        message = prepare_message_for_telegram(articles)
        # print(message)
        context.bot.send_message(chat_id=context.job.context['chat_id'], text=message)

    @staticmethod
    def get_daily_news(update: Update, context: CallbackContext) -> None:
        # command_args = context.args
        context_args_dict = {
            'chat_id': update.effective_chat.id,
            'url': 'https://habr.com/ru/hub/python/'
        }
        context.job_queue.run_repeating(
            Bot.process_habr_articles_parsing,
            interval=30,
            context=context_args_dict
        )

    def start_bot(self) -> None:
        self.dispatcher.add_handler(CommandHandler('start', self.start_command))
        self.dispatcher.add_handler(CommandHandler('help', self.help_command))
        self.dispatcher.add_handler(CommandHandler('get_daily_news', self.get_daily_news))
        self.updater.start_polling()
        self.updater.idle()
