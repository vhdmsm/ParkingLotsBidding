from django.contrib.auth.models import User
from tgbot.models import Person


def user_annotator(func):
    def inner(*args, **kwargs):
        bot, update = args[0], args[1]
        from_user = update.message.from_user
        chat_id = str(update.message.chat_id)
        tg_first_name = from_user.first_name if from_user.first_name else ""
        tg_last_name = from_user.last_name if from_user.last_name else ""
        tg_username = from_user.username
        if not Person.objects.filter(tg_id=chat_id).exists():
            person = Person.objects.create(tg_id=chat_id, tg_username=tg_username)
            if not person.user or not User.objects.filter(username=chat_id).exists():
                user = User.objects.create(username=chat_id, first_name=tg_first_name, last_name=tg_last_name)
                person.user = user
                person.save()
        else:
            person = Person.objects.get(tg_id=chat_id)
            if tg_first_name != person.user.first_name or tg_last_name != person.user.last_name or \
                    tg_username != person.user.username:
                person.user.first_name = tg_first_name
                person.user.last_name = tg_last_name
                person.user.username = tg_username
                person.save()
        kwargs['person'] = person
        func(*args, **kwargs)
    return inner

