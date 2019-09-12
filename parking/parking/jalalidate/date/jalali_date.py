# -*- coding: utf-8 -*-
import datetime

from parking.jalalidate.date.calverter import Calverter

__docformat__ = 'reStructuredText'

MONTHS = ("فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي", "بهمن", "اسفند")


def get_jalali(value):
    """
    :type value:datetime.date

    :rtype: jalali:tuple
    :return:jalali
    """
    cal = Calverter()
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    jalali = cal.jd_to_jalali(jd)
    return jalali


def expand_month_day(value):
    if len(str(value)) == 1:
        result = "0%s" % value
        return result
    return value


def split_date(str):
    """
    رشته ی داده شده را با
    "-"
    جدا میکند و یک تاپل شامل سه عدد سال و ماه و روز را برمیگرداند.

    :type str:str
    """
    l1 = str.split("-")
    year = int(l1[0])
    month = int(l1[1])
    day = int(l1[2])
    return year, month, day


def split_time(str):
    """
    رشته ی داده شده را با
    ":"
    جدا میکند و سه عدد ساعت ، دقیقه و ثانیه را برمیگرداند

    :type str:str
    """
    time_sep = str.split(":")
    hour = int(time_sep[0])
    minute = int(time_sep[1])
    if len(time_sep) > 2:
        second = int(time_sep[2])
    else:
        second = 0
    return hour, minute, second


def convert_stringdate_to_pythondate(str):
    """
    رشته ی داده شده که شبیه به
    "2012-1-1"
    باشد را میگیرد و تاریخ معادل را در قالب تاریخ پایتون بازمیگرداند.

    :type str:str
    :rtype datetime.date
    """
    l1 = str.split("-")
    year = int(l1[0])
    month = int(l1[1])
    day = int(l1[2])
    return datetime.date(year, month, day)


def convert_stringdatetime_to_pythondatetime(str):
    """
        رشته ی داده شده که شبیه به
   "2012-08-01 12:47:00"
    باشد را میگیرد و تاریخ و ساعت معادل را در قالب تاریخ و ساعت پایتون بازمیگرداند.
    به مثالها توجه کنید.

    example: convert_stringdatetime_to_pythondatetime("2012-08-01 12:47:00") return datetime.datetime(2012, 8, 1, 12, 47)
             convert_stringdatetime_to_pythondatetime("2012-08-01 12:47") return datetime.datetime(2012, 8, 1, 12, 47)
             convert_stringdatetime_to_pythondatetime("2012-08-01") return datetime.datetime(2012, 8, 1, 0, 0)

    :type str:str
    :rtype datetime.datetime

    """
    sep = str.split(" ")
    date = sep[0]
    if len(sep) > 1:
        time = sep[1]
        hour, minute, second = split_time(time)
    else:
        hour = minute = second = 0
    year, month, day = split_date(date)
    date_time = datetime.datetime(year, month, day, hour, minute, second)
    return date_time


def pdate_string(value, forceTime=False):
    """
    یک تاریخ و ساعت پایتون را دریافت میکند و معادل شمسی آن را در قالب رشته بازمیگرداند.
    به مثال ها توجه نمایید.

    example: if n=datetime.datetime(2012, 6, 24, 15, 48, 24, 138000)
             pdate_string(n) return '1391-04-04'
             pdate_string(n,True) return '1391/4/4 15:48:24'

    :type value: datetime.datetime
    :type forceTime:bool
    :param forceTime: تعیین میکند که آیا زمان نمایش داده شود یا خیر
    :rtype: str
    """
    try:
        date = value.date()
    except Exception:
        date = value
    jalali = get_jalali(date)
    if forceTime:
        try:
            h = value.hour
            m = value.minute
            s = value.second
            return "%s/%s/%s %s:%s:%s" % (jalali[0], jalali[1], jalali[2], h, m, s)
        except Exception:
            assert forceTime == False, 'Invalid format for time'

    return str(jalali[0]) + "-" + expand_month_day(str(jalali[1])) + "-" + expand_month_day(str(jalali[2]))


def pdate(value):
    """
    یک تاریخ میلادی را میگیرد و معادل شمسی آن را در قالب تاریخ پایتون بازمیگرداند

    :type value:datetime.date
    :rtype datetime.date
    """
    cal = Calverter()
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    y, m, d = cal.jd_to_jalali(jd)
    return datetime.date(year=y, month=m, day=d)


def pdate_separated(value):
    """
    یک تاریخ میلادی را میگیرد و سه عدد سال، ماه و روز که معادل شمسی آن تاریخ باشد را بازمیگرداند.

    example: pdate_seperate(datetime.date(2012, 6, 24)) return (1391, 4, 4)

    :type value: datetime.date
    :rtype: tuple(int,int,int)
    """
    cal = Calverter()
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    y, m, d = cal.jd_to_jalali(jd)
    return y, m, d


def pdate_with_separator(value, seperator):
    """
    یک تاریخ میلادی را میگرد و معادل شمسی آن را در قالب رشته ای که به
    seperator
    جدا شده باشد برمیگرداند.
    example: '1391/4/4'

    :type value: datetime.date
    :type seperator:str
    :rtype: str
    """
    jalali = get_jalali(value)
    return str(jalali[0]) + seperator + str(jalali[1]) + seperator + str(jalali[2])


def pdate_persian_month(value):
    """
    یک تاریخ میلادی را میگیرد و معادل شمسی را مانند زیر برمیگرداند.

    example: 1 تير 1391

    :type value: datetime.date
    :rtype: str
    """
    jalali = get_jalali(value)
    return str(jalali[2]) + " " + MONTHS[jalali[1] - 1] + " " + str(jalali[0])


def pdate_persian_month_weekday(value):
    """
        یک تاریخ میلادی را میگیرد و معادل شمسی را مانند زیر برمیگرداند.

    example: پنجشنبه 1 تير 1391

    :type value:datetime.date
    :rtype:unicode
    """
    cal = Calverter()
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    jalali = cal.jd_to_jalali(jd)
    return cal.JALALI_WEEKDAYS[cal.jwday(jd)] + "، " + str(jalali[2]) + " " + MONTHS[jalali[1] - 1] + " " + str(
        jalali[0])


def pdate_from_miladi_str(value):
    """
    یک رشته که تاریخ میلادی را نشان میدهد میگیرد و معادل شمسی آن را
    در قالب یک رشته برمیگرداند

    example: pdate_from_miladi_str("2012-10-15") return '1391-7-24'


    :type value:str
    :return: persian date in string
    :rtype:str
    """
    date = convert_stringdate_to_pythondate(value)
    return pdate_with_separator(date, '-')


def pdate_time(value):
    """
    یک تاریخ و ساعت میلادی را میگیرد و معادل شمسی آن را در قالب تاریخ و ساعت پایتون برمیگرداند.

    example: pdate_time(datetime.datetime.now()) return datetime.datetime(1391, 4, 4, 15, 20, 27)

    :type value: datetime.datetime
    :rtype: datetime.datetime
    """
    cal = Calverter()
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    y, m, d = cal.jd_to_jalali(jd)
    return datetime.datetime(year=y, month=m, day=d, hour=value.hour, minute=value.minute, second=value.second)

def pdatetime_separated(value):
    """
    یک تاریخ میلادی را میگیرد و شش عدد سال، ماه، روز، ساعت، دقیقه و ثانیه را که معادل شمسی آن تاریخ باشد را بازمیگرداند.

    example: pdate_seperate(datetime.date(2012, 6, 24)) return (1391, 4, 4 ,1 ,1 ,1)

    :type value: datetime.date
    :rtype: tuple(int,int,int,int,int,int)
    """
    cal = Calverter()
    jd = cal.gregorian_to_jd(value.year, value.month, value.day)
    y, m, d = cal.jd_to_jalali(jd)
    return y, m, d,value.hour, value.minute,value.second


def pdate_time_persian_month(value):
    """
    یک تاریخ و ساعت میلادی را میگیرد و معادل شمسی آن را در قالب رشته ای مانند مثال زیر  برمیگرداند.

    example: '4 تير 1391 14:5:14'
    :type value:datetime.datetime
    :rtype str
    """
    jalali = get_jalali(value)
    hour = str(value.hour) if value.hour>9 else "0%d" % value.hour
    minute = str(value.minute) if value.minute>9 else "0%d" % value.minute
    second = str(value.second) if value.second>9 else "0%d" % value.second

    return str(jalali[2]) + " " + MONTHS[jalali[1] - 1] + " " + str(jalali[0]) + " " + "%s:%s:%s" % (
        hour, minute, second)


def pdate_to_miladi(value):
    """
    یک تاریخ شمسی را در قالب تاریخ پایتون میگیرد و معادل میلادی آن را  برمیگرداند.

    example: datetime.date(1391, 4, 4) convert to datetime.date(2012, 6, 24)

    :type value:datetime.date
    :rtype:datetime.date
    """
    cal = Calverter()
    jd = cal.jalali_to_jd(value.year, value.month, value.day)
    y, m, d = cal.jd_to_gregorian(jd)
    return datetime.date(year=y, month=m, day=d)


def pdate_separate_to_miladi(year, month, day):
    """
    سه عدد که نشان دهنده ی یک تاریخ شمسی باشند را میگیرد و معادل تاریخ میلادی آن را برمیگرداند
    به مثال توجه کنید.

    example: pdate_separate_to_miladi(1391,4,4) return datetime.date(2012, 6, 24)

    :type year:int
    :type month:int
    :type day:int
    :rtype date:datetime.date
    """
    cal = Calverter()
    jd = cal.jalali_to_jd(year, month, day)
    y, m, d = cal.jd_to_gregorian(jd)
    return datetime.date(year=y, month=m, day=d)


def pdate_str_to_miladi(value):
    """
    یک رشته که تاریخ شمسی را نشان میدهد میگیرد و تاریخ معادل میلادی را در قالب تاریخ پایتون برمیگرداند
    example: pdate_str_to_miladi("1391-7-24") return datetime.date(2012, 10, 15)


    :type value:str
    :return:
    """
    year, month, day = split_date(value)
    return pdate_separate_to_miladi(year, month, day)


def format_relative_date(d):
    #TODO: convert to farsi date
    #TODO: rewrite with more care
    now = datetime.datetime.utcnow()
    diff = now - d
    year = d.strftime('%y')
    days_dic = {'Sunday': u'یکشنبه', 'Monday': u'دوشنبه', 'Tuesday': u'سه شنبه', 'Wednesday': u'چهارشنبه',
                'Thursday': u'پنجشنبه', 'Friday': u'جمعه', 'Saturday': u'شنبه'}
    day_of_week = days_dic[d.strftime('%A')]
    date = d.strftime('%y/%m/%d')
    time = d.strftime('%H:%M')

    if year == now.strftime('%y'):
        if diff.days < 7:
            if diff.days < 1:
                if diff.seconds < 60:
                    a = u'چند لحظه قبل'
                else:
                    a = u"ساعت " + time
            else:
                a = day_of_week + u" ساعت " + time
        else:
            a = date + day_of_week
    else:
        a = date + day_of_week
    return a


def pdate_time_to_miladi(value):
    """
    یک رشته که تاریخ شمسی است را میگیرد و معادل میلادی آن را در قالب تاریخ و ساعت پایتون برمیگرداند.
    به مثال ها توجه کنید.

    example: pdate_time_to_miladi("1391-5-11 12:54") return datetime.datetime(2012, 8, 1, 12, 54)
             pdate_time_to_miladi("1391-5-11") return  datetime.datetime(2012, 8, 1, 0, 0)
    :type value:str
    :rtype datetime.datetime

    """
    sep = value.split(" ")
    date = sep[0]
    if len(sep) > 1:
        time = sep[1]
        hour, minute, second = split_time(time)
    else:
        hour = minute = second = 0
    year, month, day = split_date(date)
    md = pdate_separate_to_miladi(year, month, day)
    date_time = datetime.datetime(md.year, md.month, md.day, hour, minute, second)
    return date_time


def date_time_to_miladi(value):
    """
    یک رشته که تاریخ شمسی است را میگیرد و معادل میلادی آن را در قالب تاریخ و ساعت پایتون برمیگرداند.
    به مثال ها توجه کنید.

    example: pdate_time_to_miladi("1391-5-11 12:54") return datetime.datetime(2012, 8, 1, 12, 54)
             pdate_time_to_miladi("1391-5-11") return  datetime.datetime(2012, 8, 1, 0, 0)
    :type value:str
    :rtype datetime.datetime

    """
    sep = value.split(" ")
    date = sep[0]
    if len(sep) > 1:
        time = sep[1]
        hour, minute, second = split_time(time)
    else:
        hour = minute = second = 0
    year, day, month = split_date(date)
    date_time = datetime.datetime(year, month, day, hour, minute, second)
    return date_time