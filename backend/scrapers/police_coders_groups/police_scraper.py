"""Main worker module for collecing the Police Rewired data from Google Sheets."""

import logging
import pickle
import os.path
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)


def police_coders_scrape(filename, root_path):
    """Downloads police coders community support group list and saves as CSV.

    Parameters
    -------
    filename: str
        File path to raw data output location
    root_path: str
        File path to folder containing this script
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # The ID and range of the spreadsheet.
    SPREADSHEET_ID = "1iqOvNjRlHIpoRzd61BcBLVkSxGvbta6vrzH2Jgc50aY"
    RANGE_NAME = "Support groups v2"

    def scrape():
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(root_path, "token.pickle")):
            with open(os.path.join(root_path, "token.pickle"), "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(root_path, "credentials.json"), SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(root_path, "token.pickle"), "wb") as token:
                pickle.dump(creds, token)

        service = build("sheets", "v4", credentials=creds, cache_discovery=False)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        )
        values = result.get("values", [])

        if not values:
            logger.warn("No data found.")
            return "No data found."

        else:

            # To CSV Operation

            f = open(filename, "w", encoding="utf-8")
            with f:
                writer = csv.writer(f)
                for row in values:
                    writer.writerow(row)

        return len(values)

    return scrape()
