from django.core.management.base import NoArgsCommand
from telegram.error import BadRequest
from telegram.error import Unauthorized
from telegram import *
from django.conf import settings


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        counter = 0
        bot = Bot(settings.BOT_TOKEN)
        parking_winners = []
        msg = '✋️ سلام' \
                    '\n' \
                    '✅ با توجه به اینکه در مزایده پارکینگ برنده شدید، جهت هماهنگی‌های لازم  به آقا/خانم x مراجعه کنید.' \
                  '\n' \
                  'ممنون از شما 🙏' \
                  '\n‌'

        for chat_id in parking_winners:
            try:
                bot.sendMessage(chat_id=chat_id, text=msg)
                counter += 1
                print('sent message to: %s' % chat_id)
            except (Unauthorized, BadRequest) as err:
                print(err)
            except TelegramError as err:
                print(err)
        bot.sendMessage('191322468', text='Sent news to %s persons!' % counter)
