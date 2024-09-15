from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Define the scope for Google Drive access
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive(credentials_path, token_path='token.pickle'):
    """
    Authenticate and return the Google Drive service object.
    This function handles OAuth 2.0 authentication flow manually 
    for environments like Google Colab.
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
            # Manual OAuth flow using InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)

            # Instead of run_local_server or run_console, we manually generate the URL
            auth_url, _ = flow.authorization_url(prompt='consent')

            print(f"Please go to this URL: {auth_url}")

            # Ask the user to paste the authorization code
            code = input("Enter the authorization code: ")

            # Complete the flow with the code provided by the user
            creds = flow.fetch_token(code=code)

        # Save the credentials for future use in token.pickle
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    return service
