from django.http import JsonResponse

def status(request):
    return JsonResponse({"status": "REST Fabric Control is operational"})
