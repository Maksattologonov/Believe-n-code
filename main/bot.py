import logging
import os

import django
from decouple import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from telegram_app.models import TelegramMessage, ContactUsTelegram, InstallmentTelegram, TelegramGroup, TelegramUser
from payment_app.models import Webinar

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBot:
    update_user: Update

    @staticmethod
    def get_message():
        record = TelegramMessage.objects.get()
        return record.text, record.manager_id

    @staticmethod
    def get_contact_message():
        record = ContactUsTelegram.objects.get()
        return record.text, record.manager_id

    @staticmethod
    def get_installment_message():
        record = InstallmentTelegram.objects.get()
        return record.text, record.manager_id

    @staticmethod
    def send_all(context: CallbackContext):
        users = TelegramUser.objects.all()

        for i in users:
            try:
                context.bot.send_message(chat_id=i.user_id, text=str(i.webinar__text))
            except Exception as ex:
                pass

    @staticmethod
    def get_group_message():
        record = TelegramGroup.objects.filter().first()
        return record.text

    @staticmethod
    def build_menu(buttons, n_cols,
                   header_buttons=None,
                   footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            menu.append([footer_buttons])
        return menu

    @classmethod
    def start(cls, update: Update, context: CallbackContext) -> None:
        user = update.message.from_user
        cls.update_user = update
        text, manager = cls.get_message()
        text1, manager1 = cls.get_contact_message()
        text2, manager2 = cls.get_installment_message()
        logger.info("User %s started the conversation.", user.first_name)

        if update.message.chat_id == 504416149:
            keyboard1 = [[
                InlineKeyboardButton('Отправить рассылку', callback_data='sendall')]]
            reply_markup1 = InlineKeyboardMarkup(keyboard1)
            update.message.reply_text(
                text="Выберите удобное вам время", reply_markup=reply_markup1)

        keyboard = [[
            InlineKeyboardButton("Перейти к пользователю", url=f'https://t.me/{user.username}')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        if update.message.text == '/start installments':
            context.bot.send_message(chat_id=int(manager2),
                                     text=f'Пользователь {user.username} обратился с программой рассрочки')
            context.bot.send_message(update.message.chat_id, text=text2)
        elif update.message.text == '/start contact_us':
            context.bot.send_message(chat_id=int(manager1), text=f'Пользователь {user.username} хочет связаться',
                                     reply_markup=reply_markup)
            context.bot.send_message(update.message.chat_id, text=text1)
        elif update.message.text == '/start supply':
            context.bot.send_message(chat_id=int(manager1), text=f'Пользователь {user.username} нуждается в поддержке',
                                     reply_markup=reply_markup)
            context.bot.send_message(update.message.chat_id,
                                     text="Добро пожаловать в Believe'n'code, чем я могу вам помочь?")
        elif update.message.text == '/start webinar':
            location = [
                [InlineKeyboardButton("Бишкек GMT+6", callback_data='Бишкек')],
                [InlineKeyboardButton("Алматы GMT+6", callback_data='Алматы')],
                [InlineKeyboardButton("Ташкент GMT+5", callback_data='Ташкент')],
                [InlineKeyboardButton("Душанбе GMT+5", callback_data='Душанбе')],
                [InlineKeyboardButton("Баку GMT+4", callback_data='Баку')]]
            reply_location = InlineKeyboardMarkup(location)
            update.message.reply_text(
                text="Выберите удобное вам время", reply_markup=reply_location
            )
            button = [[
                InlineKeyboardButton("Перейти", url=Webinar.objects.get().group_url)]]
            button_link = InlineKeyboardMarkup(button)
            context.bot.send_message(chat_id=update.message.chat_id, text='Перейти в группу',
                                     reply_markup=button_link)
            try:
                object = TelegramUser(user_id=update.message.chat_id, username=update.message.from_user.username,
                                      first_name=update.message.from_user.first_name,
                                      webinar=Webinar.objects.all().first())
                object.save()
            except Exception as ex:
                pass
        elif not update.message['chat']['type'] == 'supergroup':
            context.bot.send_message(chat_id=int(manager), text=f'Пользователь {user.username} начал общение',
                                     reply_markup=reply_markup)
            context.bot.send_message(update.message.chat_id, text=text)
        else:
            context.bot.send_message(update.message.chat_id,
                                     text="Добро пожаловать в Believe'n'code, чем я могу вам помочь?")

    @classmethod
    def handle_message(cls, update, context):
        text = update.message.text
        message = update.message
        user = message.from_user
        reply_to_message = message.reply_to_message
        text, manager = cls.get_message()
        if reply_to_message:
            context.bot.send_message(chat_id=reply_to_message['forward_from']['id'],
                                     text=text)
        else:
            context.bot.forward_message(chat_id=manager, from_chat_id=message.chat_id,
                                        message_id=message.message_id)
            context.bot.send_message(update.message.chat_id,
                                     text='Ваше обращение было принято, в ближайшее время'
                                          ' с вами свяжется ваш личный менеджер, и полностью вас проконсультирует.')

    @classmethod
    def add_to_group(cls, update: Update, context: CallbackContext) -> None:
        text = cls.get_group_message()
        new_members = update.message.new_chat_members
        for member in new_members:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"{text.format(update.message.from_user.first_name, update.message.chat.title)}")

    @classmethod
    def error(cls, update: Update, context: CallbackContext) -> None:
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    @classmethod
    def button(cls, update, context: CallbackContext):

        query = update.callback_query
        variant = query.data
        instance = TelegramUser.objects.filter(user_id=update.callback_query.message.chat_id)
        match variant:
            case 'Бишкек':
                instance.update(location='Бишкек')
            case 'Алматы':
                instance.update(location='Алматы')
            case 'Ташкент':
                instance.update(location='Ташкент')
            case 'Душанбе':
                instance.update(location='Душанбе')
            case 'Баку':
                instance.update(location='Баку')
            case 'sendall':
                cls.send_all(context)
            case _:
                instance.update(location='Бишкек')
        query.answer()
        query.edit_message_text(text=f"Ответ записан")


def main() -> None:
    tg_bot = TelegramBot
    updater = Updater(config('TG_TOKEN'))
    updater.start_polling(timeout=3600)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", tg_bot.start))
    welcome_handler = MessageHandler(Filters.status_update.new_chat_members, tg_bot.add_to_group)
    message_handler = MessageHandler(Filters.text, tg_bot.handle_message)
    dispatcher.add_handler(
        CallbackQueryHandler(TelegramBot.button, pass_update_queue=True, pass_user_data=False, pass_chat_data=False))
    dispatcher.add_handler(welcome_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_error_handler(tg_bot.error)

    updater.start_polling()
    updater.idle()


main()
