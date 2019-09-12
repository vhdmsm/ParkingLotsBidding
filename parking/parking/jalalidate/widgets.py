# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.contrib.admin.widgets import AdminTimeWidget
from django.utils.safestring import mark_safe

from libs.jalalidate.date.jalali_date import pdate_separated


class GeoToJalaliWidget(forms.DateInput):
    def render(self, name, value, attrs=None):
        input = super(GeoToJalaliWidget, self).render(name, self.get_persian_value(value), attrs)
        output = '<div class="dateinput">' + input + '</div>'
        # output = '<div class="dateinput">' + input
        # output += '<img id="id_'+name+'_btn" src="/static/JalaliJSCalendar/cal.png" />'
        # output += '<script>make_date_input("id_'+name+'","id_'+name+'_btn" )</script>'
        # output += '</div>'

        return mark_safe(output)

    def get_persian_value(self, value):
        if isinstance(value, datetime.datetime):
            date = value.date()
        elif isinstance(value, datetime.date):
            date = value
        else:
            return value

        year, month, day = pdate_separated(date)
        output = "-".join((str(year), str(month), str(day)))
        return output


class SliderTimeWidget(forms.TimeInput):
    """
    یک ویجت برای زمان است که زمان را با یک ویجت لغزنده تغییر میدهد.

    """

    def render(self, name, value, attrs=None):
        input = super(SliderTimeWidget, self).render(name, self.get_time_value(value), attrs)
        output = '<div class="timeinput">' + input + '</div>'
        return mark_safe(output)

    def get_time_value(self, value):
        if isinstance(value, datetime.datetime):
            time = value.time()
        else:
            time = value
        return time


class GeoToJalaliAdminSplitDateTimeWidget(forms.SplitDateTimeWidget):
    """
    یک ویجت است که تاریخ آن شمسی است و زمان آن به سبک زمان در قسمت ادمین است

    """

    def __init__(self, attrs=None):
        widgets = [GeoToJalaliWidget, AdminTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)


class GeoToJalaliSliderDateTimeWidget(forms.SplitDateTimeWidget):
    """
    یک ویجت است که تاریخ آن شمسی است و زمان آن به صورت لغزنده است.

    """

    def __init__(self, attrs=None):
        widgets = [GeoToJalaliWidget, SliderTimeWidget]
        forms.MultiWidget.__init__(self, widgets, attrs)
