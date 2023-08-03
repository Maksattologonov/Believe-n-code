import logging
import os

import django
from decouple import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from telegram_app.models import TelegramMessage, ContactUsTelegram, InstallmentTelegram, TelegramGroup, TelegramUser, \
    TelegramAdmin
from payment_app.models import Webinar

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBot:
    update_user: Update

    @staticmethod
    def get_admin():
        queryset = TelegramAdmin.objects.all()
        return list(queryset.values_list('id', flat=True))

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
                context.bot.send_message(chat_id=i.user_id, text=i.webinar.text)
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
        """функия для красивого разделения кнопок"""
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, [header_buttons])
        if footer_buttons:
            menu.append([footer_buttons])
        return menu

    @classmethod
    def start(cls, update: Update, context: CallbackContext) -> None:
        """большая функция старт, принимает query params и в зависимости от них отвечает и выводит кнопки"""
        user = update.message.from_user
        cls.update_user = update
        text, manager = cls.get_message()
        text1, manager1 = cls.get_contact_message()
        text2, manager2 = cls.get_installment_message()
        logger.info("User %s started the conversation.", user.first_name)
        # if update.message.chat_id in cls.get_admin():
        #     update.message.reply_text("Напишите текст для рассылки",
        #                               reply_markup=cls.get_keyboard(update))
        # else:
        #     pass

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
            user = update.message.from_user
            keyboard = [[InlineKeyboardButton(text="Бишкек, Алматы", callback_data='Бишкек, Алматы')],
                        [InlineKeyboardButton(text="Ташкент, Душанбе", callback_data='Ташкент, Душанбе')],
                        [InlineKeyboardButton(text="Баку", callback_data='Баку')]]
            reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Здравствуйте {user.first_name}, как вам идея IT Фриланса? Готовы зажечь? 😃подключайтесь к нашему онлайн вебинару “Секреты твоего первого заказа на фрилансе”'
                                          ' Узнайте абсолютно все о карьере в IT, и том как правильно окунуться в мир фриланса с нуля до первого заказа'
                                          ' выберите ваш город',
                                     reply_markup=reply_markup)
            try:
                tg_user = TelegramUser(user_id=update.message.chat_id,
                                       username=user.username,
                                       first_name=user.first_name,
                                       location='+6',
                                       webinar=Webinar.objects.get())
                tg_user.save()
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
        """функция эхл, отвечает на сообщение и передает их администратору"""
        message = update.message
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
        """функция отправляет сообщение при добавлении в группу"""
        text = cls.get_group_message()
        new_members = update.message.new_chat_members
        for member in new_members:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=f"{text.format(update.message.from_user.first_name, update.message.chat.title)}")

    @classmethod
    def error(cls, update: Update, context: CallbackContext) -> None:
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    @classmethod
    def broadcast(cls, update, context):
        """функция рассылки работает только с админ id"""
        if update.message.from_user.id in cls.get_admin():
            update.message.reply_text("Рассылка сообщений начата!")
            cls.send_all(context)
        else:
            pass

    @classmethod
    def get_keyboard(cls, update):
        """выводим кнопку для рассылки"""
        keyboard = [["Рассылка"]] if update.message.from_user.id in cls.get_admin() else []
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    @classmethod
    def button(cls, update, context: CallbackContext):
        """Ловим ответ, какая кнопка была нажата"""
        query = update.callback_query
        variant = query.data
        time = ''
        instance = TelegramUser.objects.filter(user_id=update.callback_query.message.chat_id)
        match variant:
            case 'Бишкек, Алматы':
                instance.update(location='+6')
                time = '+6'
            case 'Ташкент, Душанбе':
                instance.update(location='+5')
                time = '5'
            case 'Баку':
                instance.update(location='+4')
                time = '+4'
            case _:
                instance.update(location='+6')
        query.answer()
        query.edit_message_text(text=f"Поздравляем вы сделали первый шаг вашего путешествия IT фриланса, "
                                     f"ваш часовой пояс {time}")


def main() -> None:
    tg_bot = TelegramBot()
    updater = Updater(config('TG_TOKEN'))
    updater.start_polling(timeout=3600)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", tg_bot.start))
    # welcome_handler = MessageHandler(Filters.status_update.new_chat_members, tg_bot.add_to_group)
    dispatcher.add_handler(CallbackQueryHandler(tg_bot.button))
    dispatcher.add_handler(MessageHandler(Filters.regex('^Рассылка$'), tg_bot.broadcast))
    dispatcher.add_error_handler(tg_bot.error)

    updater.start_polling()
    updater.idle()


main()
