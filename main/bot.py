import logging
import os
import django

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from main.settings import TG_TOKEN

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from tariff.models import Telegram

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    record = Telegram.objects.all().first()
    print(record)
    logger.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("Связаться с нами", url=str(record)),
            InlineKeyboardButton("Программа рассрочки", url=str(record))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"{record.text.format(user.first_name) if user.name else ''}!", reply_markup=reply_markup)


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    updater = Updater(TG_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
