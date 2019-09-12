# -*- coding: utf-8 -*-
from libs.jalalidate.date.jalali_date import pdate_separate_to_miladi, pdate_time_to_miladi


__docformat__ = 'reStructuredText'

from django.core import validators
from django.core.exceptions import ValidationError

from libs.jalalidate.widgets import *


class JalaliDateField(forms.DateField):
    widget = GeoToJalaliWidget
    default_error_messages = {'invalid': u"یک تاریخ معتبر وارد نمایید."}

    #    def __init__(self, input_formats=None, *args, **kwargs):
    #        super(ShamsiDateField,self).__init__(input_formats=None, *args, **kwargs)
    #        if kwargs.has_key('initial'):
    #            new_initial = pdate_string(kwargs.get('initial'))
    #            kwargs.update({'initial':new_initial})

    # def validate(self, value):
    # super(JalaliDateField, self).validate(value)
    #

    def to_python(self, value):
        """
        Validates that the input can be converted to a date. Returns a Python
        datetime.date object.
        """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        try:
            l1 = value.split("-")
            year = int(l1[0])
            month = int(l1[1])
            day = int(l1[2])
            return pdate_separate_to_miladi(year, month, day)
        except Exception:
            raise ValidationError(self.default_error_messages['invalid'])


class JalaliAdminSplitDateTimeField(forms.MultiValueField):
    """
    a form field that its date is  ShamsiDateField and its time is
    TimeField and its widget is ShamsiAdminSplitDateTimeWidget.
    this field is suitable for admin
    """
    widget = GeoToJalaliAdminSplitDateTimeWidget
    default_error_messages = {
        'invalid_date': (u'یک تاریخ معتبر وارد نمایید.'),
        'invalid_time': (u'یک زمان معتبر وارد نمایید.'),
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages
        localize = kwargs.get('localize', False)
        fields = (
            JalaliDateField(error_messages={'invalid': errors['invalid_date']}, localize=localize),
            forms.TimeField(error_messages={'invalid': errors['invalid_time']}, localize=localize),
        )
        super(JalaliAdminSplitDateTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_date'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_time'])
            return datetime.datetime.combine(*data_list)
        return None


class JalaliDateTimeField(forms.MultiValueField):
    """
    a form field that its date is  ShamsiDateField and its time is
    TimeField and its widget is ShamsiSliderDateTimeWidget.

    """
    widget = GeoToJalaliSliderDateTimeWidget
    default_error_messages = {
        'invalid_date': (u'یک تاریخ معتبر وارد نمایید.'),
        'invalid_time': (u'یک زمان معتبر وارد نمایید.'),
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages
        localize = kwargs.get('localize', False)
        fields = (
            JalaliDateField(error_messages={'invalid': errors['invalid_date']}, localize=localize),
            forms.TimeField(error_messages={'invalid': errors['invalid_time']}, localize=localize),
        )

        fields[0].widget.attrs['placeholder'] = 'تاریخ'
        fields[1].widget.attrs['placeholder'] = 'ساعت'


        super(JalaliDateTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):

        if data_list:
            if data_list[0] in validators.EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_date'])
            if data_list[1] in validators.EMPTY_VALUES:

                raise ValidationError(self.error_messages['invalid_time'])
            return datetime.datetime.combine(*data_list)
        return None

    def to_python(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a Python
        datetime.datetime object.
            """
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            value = datetime.datetime(value.year, value.month, value.day, 0, 0, 0)
            return value
        try:
            date_time = pdate_time_to_miladi(value)
            return date_time
        except ValidationError:
            raise ValidationError(self.default_error_messages['invalid_date'])
