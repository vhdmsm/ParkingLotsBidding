#coding=utf-8
import datetime

from django.template import Library
from django.utils import timezone

from parking.jalalidate.date.jalali_date import pdate_persian_month, get_jalali, pdate_persian_month_weekday, \
    pdate_with_separator, pdate_time

__docformat__ = 'reStructuredText'

MONTHS = (
    "فروردين", "ارديبهشت", "خرداد", "تير", "مرداد", "شهريور", "مهر", "آبان", "آذر", "دي", "بهمن", "اسفند")

register = Library()

@register.simple_tag
def pdate(value):
    """
    example : 1 تير 1391

    :type value:datetime.date
    """
    if value is None:
        return '-'
    return pdate_persian_month(value)

@register.simple_tag
def pdate_from_str(value):
    parts = value.split('-')
    if len(parts) == 3:
        D = datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
        return pdate(D)
    else:
        return value

@register.simple_tag
def pdatetime(value):
    """
    show persian date and time.
    example: 1 تير 1391 17:41:45
    :type value: datetime.datetime
    """

    if value is None or value is "":
        return '-'
    jalali = get_jalali(value)
    return str(jalali[2]) + " " + MONTHS[jalali[1] - 1] + " " + str(jalali[0]) + " " + "%d:%d:%d" % (
        value.hour, value.minute, value.second)

@register.simple_tag
def pdate_f(value):
    """
    show persian date and time.
    example: 1394-1-1 23:58:21
    :type value: datetime.datetime
    """

    if value is None or value is "":
        return '-'
    jalali = get_jalali(value)
    return str(jalali[0]) + "-" + str(jalali[1]) + "-" + str(jalali[2]) + " " + "%d:%d:%d" % (
        value.hour, value.minute, value.second)


@register.simple_tag
def pdatetime_long(value):
    """
    show persian date and time.
    example: 5 تير 1391 ساعت 14:0:0
    :type value: datetime.datetime
    """
    if value is None:
        return '-'
    jalali = get_jalali(value)
    return str(jalali[2]) + " " + MONTHS[jalali[1] - 1] + " " + str(jalali[0]) + " ساعت " + "%d:%d:%d" % (
        value.hour, value.minute, value.second)

@register.simple_tag
def pdate_weekday(value):
    """
    example: پنجشنبه 1 تير 1391

    :type value:datetime.date
    """
    if value is None:
        return '-'
    return pdate_persian_month_weekday(value)


@register.simple_tag
def pdate_weekday_today():
    """
    represent today persian datetime.
    example: پنجشنبه 1 تير 1391
    """
    return pdate_persian_month_weekday(timezone.now())


@register.simple_tag
def pdate_string_with_dash(value):
    """
    represent value persian datetime.
    example: '1391-4-4'
    """
    return pdate_with_separator(value,"-")


@register.simple_tag
def pdate_time_normal(value):
    return pdate_time(value)
