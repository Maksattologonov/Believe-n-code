import datetime
import logging
import os
import django

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

from main.settings import TG_TOKEN

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from telegram_app.models import Telegram
from payment_app.models import TemporaryAccess

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_latest_record():
    record = Telegram.objects.all().first()
    return record.chat_welcome_text, record.group_welcome_text, record.direction, record.installment_program, \
        record.manager_telegram_id


class TelegramBot:
    update_user: Update

    @classmethod
    def start(cls, update: Update, context: CallbackContext) -> None:
        user = update.message.from_user

        cls.update_user = update
        text_1, text_2, direction, installment_program, manager_telegram_id = get_latest_record()
        logger.info("User %s started the conversation.", user.first_name)
        keyboard = [
            [
                InlineKeyboardButton("Связаться с нами", url=str(direction)),
                InlineKeyboardButton("Программа рассрочки", url=str(installment_program))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f"{text_1.format(user.first_name)}", reply_markup=reply_markup)
        print(manager_telegram_id, type(manager_telegram_id))
        context.bot.send_message(chat_id=manager_telegram_id, text=f'Пользователь {user.username} начал общение')

    @classmethod
    def handle_message(cls, update, context):
        text = update.message.text
        message = update.message
        user = message.from_user
        reply_to_message = message.reply_to_message
        text_1, text_2, direction, installment_program, manager_telegram_id = get_latest_record()

        if reply_to_message:
            context.bot.send_message(chat_id=reply_to_message['forward_from']['id'],
                                     text=text)
        else:
            context.bot.forward_message(chat_id=manager_telegram_id, from_chat_id=message.chat_id,
                                        message_id=message.message_id)

    @classmethod
    def add_to_group(cls, update: Update, context: CallbackContext) -> None:
        text_1, text_2, direction, installment_program, manager_telegram_id = get_latest_record()

        new_members = update.message.new_chat_members
        for member in new_members:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"{text_2.format(update.message.from_user.first_name)}")

    @classmethod
    def error(cls, update: Update, context: CallbackContext) -> None:
        logger.warning('Update "%s" caused error "%s"', update, context.error)


def main() -> None:
    tg_bot = TelegramBot
    updater = Updater('6241290167:AAGTyfCUyXU0Qsv_Sfkx55-tGMANqRfgcO0')
    updater.start_polling(timeout=3600)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", tg_bot.start))
    welcome_handler = MessageHandler(Filters.status_update.new_chat_members, tg_bot.add_to_group)
    message_handler = MessageHandler(Filters.text, tg_bot.handle_message)
    dispatcher.add_handler(welcome_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_error_handler(tg_bot.error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
