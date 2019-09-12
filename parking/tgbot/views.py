import json
from queue import Queue
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.bot import Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher, InlineQueryHandler


@csrf_exempt
def webhook(request):
    from tgbot.bot_handler import start, handle_text, error, guide_msg, add_pelak, inlinequery_handler, inform_pelak
    bot = Bot(settings.BOT_TOKEN)

    dispatcher = Dispatcher(bot, Queue(), workers=4)
    # The command
    dispatcher.add_handler(InlineQueryHandler(inlinequery_handler))
    dispatcher.add_handler(CommandHandler('guide', guide_msg))
    dispatcher.add_handler(CommandHandler('add_pelak', add_pelak, pass_args=True))
    dispatcher.add_handler(CommandHandler('inform_pelak', add_pelak, pass_args=True))
    dispatcher.add_handler(CommandHandler('home', start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_text))
    dispatcher.add_error_handler(error)

    update = Update.de_json(json.loads(request.body.decode("utf-8")), bot)

    dispatcher.process_update(update)

    return HttpResponse(status=200)
