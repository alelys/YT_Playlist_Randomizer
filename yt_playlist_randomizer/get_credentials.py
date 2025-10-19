"""
get_credentials.py
Handles OAuth2 authentication for the YouTube Data API (for a desktop application).
Saves the access token to a token.json file so you don’t have to log in again.
"""

from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/youtube"]
BASE_DIR = Path(__file__).resolve().parent
CLIENT_SECRETS = BASE_DIR / "data" / "client_secrets.json"
TOKEN_FILE = BASE_DIR / "data" / "token.json"


def get_credentials():
    """Retrieves or refreshes the OAuth2 token."""
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRETS),
                SCOPES
            )
            creds = flow.run_local_server(port=8080)

        TOKEN_FILE.write_text(creds.to_json())

    return creds


if __name__ == "__main__":                  
    credentials = get_credentials()
    print("Successfully logged in:", credentials.valid)
