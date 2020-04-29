import pickle
import os.path

#DEBUG: Current working directory
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
print("Directory = ", dir_path)

import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

def googleScrape(filename):

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1iqOvNjRlHIpoRzd61BcBLVkSxGvbta6vrzH2Jgc50aY'
    SAMPLE_RANGE_NAME = 'Support groups v2'

    def main():
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('backend/scrapers/police_coders_groups/token.pickle'):
            with open('backend/scrapers/police_coders_groups/token.pickle', "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('backend/scrapers/police_coders_groups/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('backend/scrapers/police_coders_groups/token.pickle', "wb") as token:
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
            return("No data found.")
        else:
            print("Data found:")

            # To CSV Operations

            f = open("{}_{}.csv".format(filename,datetime.today().strftime('%Y_%m_%d')), "w", encoding="utf-8")

            with f:
                writer = csv.writer(f)
                for row in values:
                    writer.writerow(row)
                    print("Writing (CSV): ", row[0])

            f = open("{}_raw.csv".format(filename), "w", encoding="utf-8")
            with f:
                writer = csv.writer(f)
                for row in values:
                    writer.writerow(row)

        return(len(values))    
    
    return(main())