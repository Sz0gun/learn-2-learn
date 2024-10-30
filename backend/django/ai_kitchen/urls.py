from django.urls import path, include
from . import views

urlpatterns = [
    path('assistant/', views.assistant, name='assistant'),
    # Other paths...
               ]