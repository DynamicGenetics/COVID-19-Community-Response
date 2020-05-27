"""
Summary:

1. Get up-to-date data using police_coders_scrape() method
2. Clean into format the data pipeline is expecting
3. Save data as csv (overwriting old data if necessary)


Methods:


police_coders_scrape(filename, root_path)

Description:
Downloads police coders community support group list and saves as CSV

Parameters:
filename = File path to raw data output location root_path = File path to folder containing this script


filter_welsh_groups(input_path, polygon)

Description:
Return a csv list of groups which are located in Wales, as well as the last row which is used as a header.

Parameters:
input_path = File path to raw data location polygon= Polygon object of Welsh country boundary


write_data_to_CSV(output, row, out_path)

Description:
Writes data to csv

Parameters:
output= csv list of groups row= Row to be used as header out_path= File path to cleaned data output location


get_welsh_boundary(fileNm_Wales)

Description:
Returns a polygon shape containing the Welsh boundary

Parameters:
fileNm_Wales= File path to Welsh geojson boundary file

"""

import pickle
import os.path
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def police_coders_scrape(filename, root_path):

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = "1iqOvNjRlHIpoRzd61BcBLVkSxGvbta6vrzH2Jgc50aY"
    SAMPLE_RANGE_NAME = "Support groups v2"

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

        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
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
