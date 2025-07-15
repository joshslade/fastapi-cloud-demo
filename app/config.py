from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def generate_token_from_credentials(credential_path, token_path):

    flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
    credentials = flow.run_local_server(port=0)
    with open(token_path, "w") as token:
        token.write(credentials.to_json())


def main():
    credential_path = Path("credentials.json")
    token_path = Path("token.json")
    generate_token_from_credentials(credential_path,token_path)
     


if __name__ == "__main__":
    main()
