import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1DSePdMY4cepwktfjd7PD7oHIt3w5V6kQ36-vd4QRYLU"
token_path = Path("gcreds.json")


def get_credentials():
    credentials = None
    # if os.path.exists("token.json"):
    if os.path.exists(token_path):
        credentials = Credentials.from_authorized_user_file(token_path, SCOPES)
       
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            with open(token_path, "w") as token:
                token.write(credentials.to_json())

    return credentials


def duplicate_data_in_sheet():
    """
    Appends rows from a pandas DataFrame to a Google Sheet.
    Assumes the sheet already has a header row matching df.columns.
    """
    spreadsheet_id = os.getenv("SHEET_ID")
    sheet_name = "Sheet1"
    
    try:
        credentials = get_credentials()
    except RuntimeError as e:
        return {"error": str(e)}

    try:
        # Find the next empty row
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()

        # Get current data to find where to append
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}"
        ).execute()
        existing_rows = result.get("values", [])
        start_row = len(existing_rows) + 1  # 1-based indexing

        # Prepare range for appending
        range_name = f"{sheet_name}!A{start_row}"

        body = {"values": existing_rows}
        response = sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        print(f"Appended {len(existing_rows)} rows {sheet_name}")
        return response
    except HttpError as e:
        return {"error": f"Google Sheets API error: {e}"}

if __name__ == "__main__":
    duplicate_data_in_sheet()