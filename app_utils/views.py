from django.http import JsonResponse
from app_utils.drive_auth import authenticate_drive

def list_drive_files(request):
    """
    View that authenticates with Google Drive and list files
    """

    # Authenticate and get the Google Drive service object
    drive_service = authenticate_drive()

    # List the first 10 files in Google Drive
    result = drive_service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)"
    ).execute()

    items = results.get('files', [])

    if not items:
        return JsonResponse({"message": "No files found in Google Drive."})
    else:
        return JsonResponse({"files": items})