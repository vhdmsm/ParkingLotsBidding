import logging
from uuid import uuid4
from django.db.models import Max
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.error import BadRequest, TelegramError, Unauthorized
from parking.constants import MIN_BID_VALUE, BID_STEP, AVAILABLE_PARKING_LOTS, END_TIME, MIN_BID_DB_ID, \
    PARKING_CHANNEL_USERNAME
from parking.utils import Utils
from tgbot.annotators import user_annotator
from tgbot.models import Person, Bid, Pelak
is_done = False
logger = logging.getLogger(__name__)


@user_annotator
def guide_msg(bot, update, **kwargs):
    person = kwargs.pop('person')
    chat_id = update.message.chat_id

    msg = '🔹 پلاکتون رو با استفاده از کامند /add_pelak به این صورت به سیستم وارد کنید:' \
          '\n' \
          '/add_pelak ۹۹ص۳۹۹' \
          '\n' \
          '❗️ شماره پلاک رو کامل با کیبورد ‌فارسی بنویسید و اگه تلگرام چپ و راست نشون داد مهم نیست.' \
          '\n' \
          '🛎 واسه خبر دادن به صاحاب ماشین برای جابجایی ماشین هم کافیه داخل بات بزنید @parking_pegahbot و بعدش لیست افرادی که شماره پلاکشون رو داخل سیستم ثبت کردن باز میشه و می‌تونید از داخل لیست انتخابشون کنید تا بهشون خبر داده بشه 😃' \
          '\n' \
          ''
    send_tg_text_message(bot, chat_id, msg)


@user_annotator
def auction_msg(bot, update, **kwargs):
    person = kwargs.pop('person')
    chat_id = update.message.chat_id
    from_user = update.message.from_user

    msg = '🔹 برای وارد شدن به مزایده عددی بالاتر از 49,000 تومن و بخش‌پذیر بر 5000 وارد نمایید.'
    '\n'
    '🔹 به عنوان مثال عددهای 105,000، ,110,000، 115,000 و ...'
    '\n‌‌'
    send_tg_text_message(bot, chat_id, msg)


def send_tg_text_message(bot, chat_id, msg):
    try:
        bot.sendMessage(
            text=msg,
            chat_id=chat_id)
    except BadRequest as err:
        print("Error in sending bot message: %s" % err)
    except Unauthorized as err:
        print("Error in sending bot message: %s" % err)
    except TelegramError as err:
        print('chat_id: %s, msg: %s' % (chat_id, msg))
        print("Telegram error: %s" % err)


@user_annotator
def my_position(bot, update, **kwargs):
    person = kwargs.pop('person')
    chat_id = update.message.chat_id
    from_user = update.message.from_user

    msg = ''
    send_tg_text_message(bot, chat_id, msg)


def get_lowest_bid(bot):
    persons_with_bid = Person.objects.filter(bids__bid__isnull=False)
    if persons_with_bid.count() < AVAILABLE_PARKING_LOTS:
        lowest_bid = MIN_BID_VALUE
    else:
        try:
            lowest_bid = persons_with_bid.annotate(last_bid=Max('bids__bid')).order_by('-last_bid')[
                AVAILABLE_PARKING_LOTS - 1].last_bid
        except IndexError:
            lowest_bid = MIN_BID_VALUE
    try:
        min_bid_obj = Bid.objects.get(id=MIN_BID_DB_ID)
    except Bid.DoesNotExist:
        min_bid_obj = Bid.objects.create(id=MIN_BID_DB_ID, bid=lowest_bid)

    if min_bid_obj.bid != lowest_bid:
        min_bid_obj.bid = lowest_bid
        min_bid_obj.save()
        msg = '👈 کف مقدار بید: %s‌‌' % lowest_bid
        send_tg_text_message(bot, PARKING_CHANNEL_USERNAME, msg)

    return int(lowest_bid)


@user_annotator
def start(bot, update, **kwargs):
    person = kwargs.pop('person')
    from_user = update.message.from_user
    chat_id = update.message.chat_id
    if is_done:
        send_tg_text_message(bot, chat_id, 'مزایده به پایان رسیده است')
        return

    msg = '👈 کف مقدار بید: %s‌‌' % get_lowest_bid(bot)

    # msg = '🔹 پلاکتون رو با استفاده از کامند /add_pelak به این صورت به سیستم وارد کنید:' \
    #       '\n' \
    #       '/add_pelak ۹۹ص۳۹۹' \
    #       '\n' \
    #       '❗️ شماره پلاک رو کامل با کیبورد ‌فارسی بنویسید و اگه تلگرام چپ و راست نشون داد مهم نیست.' \
    #       '\n' \
    #       '🛎 واسه خبر دادن به صاحاب ماشین برای جابجایی ماشین هم کافیه داخل بات بزنید @parking_pegahbot و بعدش لیست افرادی که شماره پلاکشون رو داخل سیستم ثبت کردن باز میشه و می‌تونید از داخل لیست انتخابشون کنید تا بهشون خبر داده بشه 😃' \
    #       '\n' \
    #       ''
    send_tg_text_message(bot, chat_id, msg=msg)


@user_annotator
def add_pelak(bot, update, **kwargs):
    person = kwargs.pop('person')
    args = kwargs.pop('args')
    chat_id = update.message.chat_id
    from_user = update.message.from_user
    if not args:
        bot.sendMessage(chat_id, text='پلاک رو نفرستادی که :/')

    pelak = Utils.engishize(args[0])
    import re
    if not re.match('(([1-9]){2}([^0-9]){1}([1-9]){3})', pelak):
        bot.sendMessage(chat_id, text='فرمت پلاک رو درست وارد نکردی. شماره پلاک رو فارسی و پشت سرهم بنویس مثل:'
                                      '\n'
                                      '۹۹ص۳۹۹'
                                      '\n‌')
        return
    if Pelak.objects.filter(value=pelak).exists():
        send_tg_text_message(bot, chat_id, '❗️ شماره پلاکت قبلا ثبت شده!')
        return

    Pelak.objects.create(person=person, value=pelak)
    send_tg_text_message(bot, chat_id, '✅ شماره پلاکت اضافه شد')
    return


@user_annotator
def inform_pelak(bot, update, **kwargs):
    person = kwargs.pop('person')
    args = kwargs.pop('args')
    chat_id = update.message.chat_id
    from_user = update.message.from_user

    if not args:
        send_tg_text_message(bot, chat_id, '❗️ پلاک رو نفرستادی که :/')
    pelak = args[0]
    try:
        pelak = Pelak.objects.get(value=pelak)
        pelak_chat_id = pelak.person.user.username
        send_tg_text_message(bot, pelak_chat_id, '🛎 دوست عزیز بیا ماشینت رو جابجا کن.')
    except Pelak.DoesNotExist:
        send_tg_text_message(bot, chat_id, '❗️ همچین پلاکی تو سیستم نیست!')


@user_annotator
def inlinequery_handler(bot, update, **kwargs):
    person = kwargs.pop('person')
    query = update.inline_query.query
    requester = update.inline_query.from_user
    results = list()
    if not query or query == 'pelaks':
        for pelak in Pelak.objects.all():
            pelak = InlineQueryResultArticle(id=uuid4(),
                                            hide_url=True,
                                            title='%s - %s' % (pelak.person.user.get_full_name(), pelak.value),
                                            input_message_content=InputTextMessageContent('/inform %s' % pelak.value),
                                            description='')
            results.append(pelak)
        bot.answerInlineQuery(update.inline_query.id, results=results, cache_time=0)
    return


def check_other_bids(bot):
    persons_with_bid = Person.objects.filter(bids__bid__isnull=False)
    top_twenty_persons = persons_with_bid.annotate(last_bid=Max('bids__bid')).order_by('-last_bid').values_list('id', flat=True)[:AVAILABLE_PARKING_LOTS]
    print('tops: %s' % top_twenty_persons)
    sent_messages_ids = []
    for person in persons_with_bid:
        if person.id not in top_twenty_persons and person.id not in sent_messages_ids:
            chat_id = person.user.username
            lowest_bid = get_lowest_bid(bot)
            msg = '❗️ به علت کمتر بودن بید شما، از لیست برنده‌ها خارج شدید. بید بالاتری بکنید تا مجدد وارد لیست شوید' \
                '\n' \
                'کف بید: %s' \
                '\n‌' % lowest_bid

            admin_msg = 'فرد: %s' \
                        '\nبا' \
                        'کف بید: %s' \
                        '\n' \
                        'افتاد بیرون!' \
                        '\n‌' % (person, lowest_bid)
            send_tg_text_message(bot, chat_id, msg=msg)
            send_tg_text_message(bot, '191322468', msg=admin_msg)
            # Log.objects.crate(person=person, log=msg)
            sent_messages_ids.append(person.id)
            print(admin_msg)


def handle_photo(bot, update):
    print(update)


@user_annotator
def handle_text(bot, update, **kwargs):
    person = kwargs.pop('person')
    chat_id = update.message.chat_id
    text = update.message.text
    print(update)

    if update.message.date > END_TIME:
        send_tg_text_message(bot, chat_id,
                             msg='❗️ زمان مزایده تموم شده!')
        return
    lowest_bid = get_lowest_bid(bot)
    text = Utils.engishize(text)
    if not text.isdigit():
        send_tg_text_message(bot, chat_id,
                             msg='❗️ تنها عدد بید خود را به صورت 50,000، 55,000 و غیره وارد نمایید.')
        return
    try:
        bid_value = int(text)
        if bid_value > MIN_BID_VALUE:
            send_tg_text_message(bot, chat_id, msg='❗️ تو که اینقد پول داری با اسنپ بیا دیگه 😁 ماکس قیمت 700,000 تومنه!')
            return
        if not bid_value > MIN_BID_VALUE:
            send_tg_text_message(bot, chat_id, msg='❗️ عدد ورودی بید باید بزرگتر از 49,000 باشد')
            return
        if not (bid_value / 1000) % BID_STEP == 0:
            send_tg_text_message(bot, chat_id, msg='❗️ عدد ورودی بید باید بخش‌پذیر بر 5000 باشد')
            return
        if not bid_value > lowest_bid:
            send_tg_text_message(bot, chat_id, msg='❗️ بید شما باید بیشتر از کف مقدار بید %s باشد' % lowest_bid)
            return
        person_last_bid = 0
        if person.bids.count():
            try:
                person_last_bid = int(Person.objects.filter(id=person.id).annotate(max_bid=Max('bids__bid'))[0].max_bid)
            except IndexError:
                person_last_bid = 0
        if bid_value < person_last_bid:
            send_tg_text_message(bot, chat_id, msg='❗️ بید شما نمی‌تونه کمتر از بید قبلی‌تون که %s بود باشه!' % person_last_bid)
            return
        Bid.objects.get_or_create(person=person, bid=bid_value)
        check_other_bids(bot)
        send_tg_text_message(bot, chat_id, msg='✅ بید %s شما ثبت شد'
                                 '\n'
                                '💎 پارکینگ گیرت اومده ولی حواست باشه از دستش ندی!'
                                '\n'
                                 '👈 کف مقدار بید: %s'
                                 '\n‌‌' % (bid_value, lowest_bid))

        return
    except ValueError as err:
        print('in exception: %s' % err)
        send_tg_text_message(bot, chat_id, msg='❗️ تنها عدد بید خود را به صورت 100,000، 115,000 و غیره وارد نمایید.')
        return


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))
