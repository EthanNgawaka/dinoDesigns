import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

ID = "1h72EMpxbpnBPsyGRuaACVipCjezudQkoP7a4lXfdEVw"


def searchSheet(sheets, tLeft, bRight, sheetName="Sheet1"):
    result = (
        sheets.values()
        .get(spreadsheetId=ID, range=f"{sheetName}!{tLeft}:{bRight}")
        .execute()
    )

    values = result.get("values", [])
    return values


def editSheet(sheets, tLeft, bRight, valueArray, sheetName="Sheet1"):
    sheets.values().update(
        spreadsheetId=ID,
        range=f"{sheetName}!{tLeft}:{bRight}",
        valueInputOption="USER_ENTERED",
        body={"values": valueArray},
    ).execute()

    print(f"updated {sheetName}!{tLeft}:{bRight} with {valueArray}")
    return


def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        print(searchSheet(sheets, "B2", "C7"))
        editSheet(
            sheets,
            "D2",
            "E7",
            [
                ["10", "A"],
                ["20", "B"],
                ["30", "C"],
                ["40", "D"],
                ["50", "E"],
                ["60", "F"],
            ],
        )

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
