import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

path = current_dir = os.path.dirname(__file__)
DIRECTORY = os.path.join(path, "Files", "APIs", "secrets", "GoogleCalendar")

def main():
    creds = None
    
    if os.path.exists(os.path.join(DIRECTORY, 'token.json')):
        creds = Credentials.from_authorized_user_file(os.path.join(DIRECTORY, 'token.json'), SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(DIRECTORY, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=8080)
        
        with open(os.path.join(DIRECTORY, 'token.json'), 'w') as token:
            token.write(creds.to_json())

    print(f"Token saved to {os.path.join(DIRECTORY, 'token.json')}")

if __name__ == '__main__':
    main()