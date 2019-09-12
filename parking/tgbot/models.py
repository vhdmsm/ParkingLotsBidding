from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    class Meta:
        verbose_name = 'فرد'
        verbose_name_plural = 'افراد'

    def __str__(self):
        return '%s - %s' % (self.user.get_full_name(), self.user.username)

    user = models.OneToOneField(User, related_name='person', on_delete=models.CASCADE, null=True, blank=True)
    tg_username = models.CharField(verbose_name='یوزرنیم تلگرام', max_length=100, blank=True, null=True)
    tg_id = models.CharField(verbose_name='شناسه کاربری تلگرام', max_length=200, null=True, blank=True)
    phone_number = models.CharField(verbose_name='شماره تلفن', max_length=30, blank=True, null=True)
    last_seen = models.DateTimeField(auto_now=True, verbose_name='آخرین حضور')


class Bid(models.Model):
    class Meta:
        verbose_name = 'بید'
        verbose_name_plural = 'بیدها'
        ordering = ('-bid',)

    def __str__(self):
        return '%s - %s' % (self.person, self.bid)

    person = models.ForeignKey(Person, verbose_name='کاربر', related_name='bids', null=True, blank=True)
    bid = models.IntegerField(verbose_name='بید')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')


class Pelak(models.Model):
    class Meta:
        verbose_name = 'پلاک'
        verbose_name_plural = 'پلاک‌ها'
        ordering = ('-creation_time',)

    def __str__(self):
        return '%s - %s' % (self.person, self.value)

    person = models.ForeignKey(Person, verbose_name='کاربر', related_name='pelaks', null=True, blank=True)
    value = models.CharField(verbose_name='شماره پلاک', max_length=50)
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')


class BiddingLog(models.Model):
    class Meta:
        verbose_name = 'لاگ بید'
        verbose_name_plural = 'لاگ‌های بید'
        ordering = ('-creation_time',)

    def __str__(self):
        return '%s - %s' % (self.person, self.log)

    person = models.ForeignKey(Person, verbose_name='کاربر', related_name='logs', null=True, blank=True)
    log = models.CharField(verbose_name='لاگ بید', max_length=900, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')