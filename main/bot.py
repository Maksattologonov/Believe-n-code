import json
import logging
import os
import django

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from telegram_app.models import Telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_latest_record():
    record = Telegram.objects.all().first()
    return record.text, record.direction, record.group_link


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    text, direction, group_link = get_latest_record()
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("Связаться с нами", url=str(direction)),
            InlineKeyboardButton("Программа рассрочки", url=str(group_link))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"{text.format(user.first_name)}", reply_markup=reply_markup)


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    updater = Updater('6241290167:AAGTyfCUyXU0Qsv_Sfkx55-tGMANqRfgcO0')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
