from django.urls import path
from .views import list_drive_files

urlpatterns = [
    path('list-drive-files/', list_drive_files, name='list_drive_files'),
]
