from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Scoopes define the level of accesss the app has to Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    """
    Authenticate and return the Google Drive service object.
    This function handles OAuth 2.0 authentication flow and manages credentials.
    """
    creds = None
    token_path = 'credentials/token.pickle'

    # Check if tocken.pickle exists to avoid re-authentication
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are available, let the user authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Run OAuth flow for the first time
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    return service