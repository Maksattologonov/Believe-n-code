import logging
import os
import django

from datetime import datetime, timedelta
from decouple import config
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler, \
    ConversationHandler
from common.services import convert_and_subtract_hours

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from telegram_app.models import TelegramMessage, ContactUsTelegram, InstallmentTelegram, TelegramGroup, TelegramUser, \
    TelegramAdmin
from payment_app.models import Webinar

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramBot:
    update_user: Update
    btn_pressed = False
    webinar = None

    def __init__(self):
        self.webinar = Webinar.objects.get()

    @staticmethod
    def get_admin():
        queryset = TelegramAdmin.objects.all()
        return list(queryset.values_list('id', flat=True))

    @staticmethod
    def get_users():
        queryset = TelegramUser.objects.all()
        return list(queryset.values_list('user_id', flat=True))

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
    def present(cls, update, context):
        users = TelegramUser.objects.all()
        for i in users:
            try:
                keyboard = [
                    [InlineKeyboardButton("Получить бесплатный доступ", callback_data='one_day_free')],
                    [InlineKeyboardButton("Получить скидку на курсы", callback_data='discount')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                context.bot.send_message(chat_id=i.user_id, text='Пожалуйста, выберите один из подарков:',
                                         reply_markup=reply_markup)
            except Exception as ex:
                pass

    def start(self, update: Update, context: CallbackContext) -> None:
        """большая функция старт, принимает query params и в зависимости от них отвечает и выводит кнопки"""
        user = update.message.from_user
        self.update_user = update
        text, manager = self.get_message()
        text1, manager1 = self.get_contact_message()
        text2, manager2 = self.get_installment_message()
        logger.info("User %s started the conversation.", user.first_name)
        # update.message.reply_text(text="Для связи с менеджером оставьте ваш номер телефона",
        #                           reply_markup=InlineKeyboardMarkup(
        #                               [[InlineKeyboardButton("Оставить",
        #                                                      callback_data='request_contact', request_contact=True)]],
        #                               resize_keyboard=True, one_time_keyboard=True))

        if update.message.chat_id in self.get_admin():
            keyboard = [
                [InlineKeyboardButton("Рассылка", callback_data='send_all')],
                [InlineKeyboardButton("Отправить подарки", callback_data='present')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

        else:
            pass
        context.bot.send_message(update.message.chat_id, text=text, reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton(text="Поделиться номером телефона", request_contact=True)]], resize_keyboard=True,
            one_time_keyboard=True))
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
                                     text=str(self.webinar.welcome_text).format(user.first_name),
                                     reply_markup=reply_markup)
            try:
                tg_user = TelegramUser(user_id=update.message.chat_id,
                                       username=user.username,
                                       first_name=user.first_name,
                                       location='+6',
                                       webinar=self.webinar)
                tg_user.save()
            except Exception as ex:
                pass

        elif not update.message['chat']['type'] == 'supergroup':
            context.bot.send_message(chat_id=int(manager), text=f'Пользователь {user.username} начал общение',
                                     reply_markup=reply_markup)
        else:
            context.bot.send_message(update.message.chat_id, text=text, reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(text="Поделиться номером телефона", request_contact=True)]], resize_keyboard=True,
                one_time_keyboard=True))
            context.bot.send_message(update.message.chat_id,
                                     text="Добро пожаловать в Believe'n'code, чем я могу вам помочь?")

    @classmethod
    def handle_message(cls, update, context):
        """функция эхo, отвечает на сообщение и передает их администратору"""
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
        if update.callback_query.message.chat_id in cls.get_admin() and cls.btn_pressed:
            update.callback_query.message.reply_text("Рассылка сообщений начата!")
            cls.send_all(context)
        else:
            pass

    @staticmethod
    def delete_message(context: CallbackContext, chat_id, message_id):
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    @classmethod
    def directions(cls, update, context):
        keyboard = [[InlineKeyboardButton(
                        text="Front-End",
                        url='https://believencode.zenclass.ru/public/t/41ab81ec-85a9-4a67-a756-6328352adf9c')],
                    [InlineKeyboardButton(
                        text="Графический Дизайн",
                        url='https://believencode.zenclass.ru/public/t/bd92a0c8-f7fa-4e08-9304-2324d7ff6adb')],
                    [InlineKeyboardButton(
                        text="UX/UI",
                        url='https://believencode.zenclass.ru/public/t/69e08e7e-72b3-4ff4-a6f8-90773861bcc0')]]
        reply_markup = InlineKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        update.callback_query.message.reply_text(text='Выберите направление:',
                                                 reply_markup=reply_markup)
        update.callback_query.message.delete_message(context=context, chat_id=update.callback_query.message.chat_id,
                                                     message_id=update.callback_querymessage.message_id)

    @classmethod
    def get_keyboard(cls, update):
        """выводим кнопку для рассылки"""
        keyboard = [["Рассылка"], ["Отправить подарок"]] if update in cls.get_admin() else []
        return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    def get_phone_number(self, update: Update, context: CallbackContext) -> None:
        try:
            user = TelegramUser.objects.get(user_id=update.message.chat_id)
            user.phone_number = update.message.contact.phone_number
            user.save()
        except TelegramUser.DoesNotExist:
            TelegramUser.objects.create(user_id=update.message.chat_id,
                                        phone_number=update.message.contact.phone_number,
                                        first_name=update.message.from_user.first_name,
                                        location='+6',
                                        webinar=self.webinar
                                        )
        update.message.reply_text(f"Спасибо! Вы поделились номером телефона")

    def button(self, update, context: CallbackContext):
        """Ловим ответ, какая кнопка была нажата"""
        try:
            query = update.callback_query
            variant = query.data
            instance = TelegramUser.objects.filter(user_id=update.callback_query.message.chat_id)
            time = self.webinar.date_time
            text = str(self.webinar.choose_text).format(time)
            match variant:
                case 'Бишкек, Алматы':
                    instance.update(location='+6')
                    query.edit_message_text(text=text)
                case 'Ташкент, Душанбе':
                    instance.update(location='+5')
                    query.edit_message_text(text=str(self.webinar.choose_text).format(self.webinar.date_time - timedelta(hours=1)))
                case 'Баку':
                    instance.update(location='+4')
                    query.edit_message_text(text=str(self.webinar.choose_text).format(self.webinar.date_time - timedelta(hours=2)))
                case 'discount':
                    context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                             text='https://believencode.io/#billing-rate-promocode')
                    query.message.delete()
                case 'one_day_free':
                    self.directions(update, context)
                case 'present':
                    self.present(update, context)
                case 'send_all':
                    self.btn_pressed = True
                    self.broadcast(update, context)
                # case 'request_contact':
                #     reply_markup = InlineKeyboardMarkup(
                #         [[InlineKeyboardButton("Поделиться контактом", callback_data='request_contact', request_contact=True)]])
                #     query.edit_message_text("Нажмите на кнопку, чтобы поделиться контактом:", reply_markup=reply_markup)
        except Exception as ex:
            pass


def main() -> None:
    tg_bot = TelegramBot()
    updater = Updater(config('TG_TOKEN'))
    while True:
        try:
            updater.start_polling()
        except Exception as e:
            pass
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", tg_bot.start))
        dispatcher.add_handler(CallbackQueryHandler(tg_bot.button))
        dispatcher.add_handler(MessageHandler(Filters.regex('^Рассылка$'), tg_bot.broadcast))
        dispatcher.add_handler(MessageHandler(Filters.regex('^Отправить подарок'), tg_bot.present))
        dispatcher.add_error_handler(tg_bot.error)
        dispatcher.add_handler(MessageHandler(Filters.contact, tg_bot.get_phone_number))
        updater.start_polling()
        updater.idle()


main()
