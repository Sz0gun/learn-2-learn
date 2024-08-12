from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from django.views.decorators.csrf import csrf_exempt
import json

# @csrf_exempt
# def telegram_webhook(request):

#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             print(data)
#             return JsonResponse({"status": "ok"}, status=200)
#         except json.JSONDecodeError as e:
#             print(f"Decode json error: {e}")
#             return JsonResponse({
#                                 "satatus": "error", 
#                                 "message": "Invalid JSON"
#                                 }, status=400)
#         except Exeption as e:
#             print (f"Unexpected error: {e}")
#             return JsonResponse({
#                                 "satatus": "error", 
#                                 "message": "Internal Server Error"
#                                 }, status=500)
#     return JsonResponse({"status": "bad request"}, status=400)
    # elif request.method == 'GET':
    #     context = {
    #     'message': '!!!GET'
    # }
    #     return render(request, 'index.html', context)
    # else:
    #     context = {
    #     'message': '!'
    # }
    # return render(request, 'index.html', context)

# def my_page_view(request):
#     # Możesz przekazać zmienne do szablonu, korzystając z kontekstu
#     context = {
#         'message': 'Witamy na naszej stronie!'
#     }
#     print("ok")
#     return render(request, 'index.html', context)