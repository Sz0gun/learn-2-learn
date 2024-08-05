import functions_framework

@functions_framework.http
def telegram_bot(request):
    # Here goes the logic of your Telegram bot
    return "Hello, Telegram Bot!"
