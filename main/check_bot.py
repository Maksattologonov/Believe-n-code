import datetime

from payment_app.models import TemporaryAccess


def check_date(update, context):
    current_date = datetime.datetime.now().date()
    date_in_database = TemporaryAccess.objects.values()
    date_diff = current_date - date_in_database

    if date_diff.days > 1:
        message = "Разница между датой в базе данных и текущей датой больше одного дня!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)



