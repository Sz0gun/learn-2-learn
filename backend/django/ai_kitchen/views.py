from django.http import JsonResponse
from .bot import get_response

def assistant(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        response = get_response(user_input)
        return JsonResponse({'response': response})
    else:
        return JsonResponse({'response': 'Invalid request method'}, status=400)