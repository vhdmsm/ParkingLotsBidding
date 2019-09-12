from django.core.management.base import NoArgsCommand
from telegram.ext import InlineQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from django.conf import settings

from tgbot.bot_handler import start, handle_text, error, guide_msg, add_pelak, inlinequery_handler, inform_pelak, \
    auction_msg


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        print("Polling started...")
        updater = Updater(settings.BOT_TOKEN)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
        dispatcher.add_handler(CommandHandler('guide', guide_msg))
        dispatcher.add_handler(CommandHandler('auction', auction_msg))
        dispatcher.add_handler(CommandHandler('add_pelak', add_pelak, pass_args=True))
        dispatcher.add_handler(CommandHandler('inform', inform_pelak, pass_args=True))
        dispatcher.add_handler(CommandHandler('home', start))
        dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
        dispatcher.add_handler(MessageHandler(Filters.photo, handle_text))
        dispatcher.add_handler(InlineQueryHandler(inlinequery_handler))

        dispatcher.add_error_handler(error)

        updater.start_polling()

        updater.idle()