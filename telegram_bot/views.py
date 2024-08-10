from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # Tutaj przetwarzaj dane otrzymane od Telegrama
        print(data)  # Logowanie danych w konsoli
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "not allowed"}, status=405)
