from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def telegram_webhook(request):

    if request.method == "POST":
        try:
            data = json.loads(request)
            # Przetwarzaj dane z Telegrama tutaj
            print(data)  # Debugowanie: sprawdź, co przychodzi z Telegrama
            return JsonResponse({"status": "ok"}, status=200)
        except Exception as e:
            context = {
        'message': e
    }
            return render(request, 'index.html', context)
            # print(f"Błąd: {e}!!!")  # Logowanie błędu
            # return JsonResponse({"status": "error"}, status=500)
    # return JsonResponse({"status": "bad request"}, status=400)
    else:
        context = {
        'message': '!' e
    }
    # print("ok")
    return render(request, 'index.html', context)

def my_page_view(request):
    # Możesz przekazać zmienne do szablonu, korzystając z kontekstu
    context = {
        'message': 'Witamy na naszej stronie!'
    }
    print("ok")
    return render(request, 'index.html', context)