from django.conf.urls import url
import tgbot.views

urlpatterns = [
    url(r'^webhook/123$', tgbot.views.webhook, name='webhook'),
]