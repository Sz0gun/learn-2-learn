from django.urls import path
from telegram_bot.views import my_page_view, telegram_webhook

urlpatterns = [
    # path('telegram/webhook/', telegram_webhook, name='telegram_webhook'),
    # path('page/', my_page_view, name='my_page'),
]