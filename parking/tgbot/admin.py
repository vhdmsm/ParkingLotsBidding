from django.contrib import admin
from django.db.models import *
from django.db.models.functions import Coalesce
from tgbot.models import Person, Bid, Pelak, BiddingLog


class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'tg_username', 'full_name', 'last_seen', )
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'tg_username']
    readonly_fields = ('last_seen',)

    def get_queryset(self, request):
        qs = super(PersonAdmin, self).get_queryset(request)
        qs = qs.annotate(total_bid=Coalesce(Count('bids'), 0))
        return qs

    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'نام کامل'


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'bid', 'creation_time', )
    readonly_fields = ('creation_time',)
    list_filter = ('creation_time', )
    search_fields = ['id', 'person__user__username', 'bid']


class LogAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'log', 'creation_time', )
    readonly_fields = ('creation_time',)
    list_filter = ('creation_time', )
    search_fields = ['id', 'person__user__username', 'log']


class PelakAdmin(admin.ModelAdmin):
    list_display = ('id', 'person', 'value', 'creation_time', )
    readonly_fields = ('creation_time',)
    list_filter = ('creation_time', )
    search_fields = ['id', 'person__user__username', 'value']


admin.site.register(Person, PersonAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Pelak, PelakAdmin)
admin.site.register(BiddingLog, LogAdmin)
