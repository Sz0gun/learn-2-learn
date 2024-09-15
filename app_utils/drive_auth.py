from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Scopes define the level of access the app has to Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive(credentials_path, token_path='token.pickle'):
    """
    Authenticate and return the Google Drive service object.
    This function handles OAuth 2.0 authentication flow and manages credentials,
    using the console flow for environments like Google Colab.
    """
    creds = None

    # Check if token.pickle exists to avoid re-authentication
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are available, let the user authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Run OAuth flow using the credentials_path
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)

            # Use run_console instead of run_local_server for Colab
            creds = flow.run_console()  # This will prompt you to copy-paste the authorization code

        # Save the credentials for future use in token.pickle
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    return service
