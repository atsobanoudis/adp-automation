import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google_calendar():
    creds = None
    credentials_file = 'credentials.json'

    # Check if the credentials file exists
    if not os.path.exists(credentials_file):
        print(f"Error: The file {credentials_file} was not found in the current directory.")
        print("Please ensure the credentials.json file is present and try again.")
        exit(1)  # Exits the script with an error status

    # Attempt to load existing tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing access token: {e}")
                exit(1)
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Failed to complete the authentication process: {e}")
                print("Please check your credentials.json file and try again.")
                exit(1)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return creds
