from __future__ import print_function
import pickle
import os.path
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def googleScrape(URL, SpreadsheetID, SpreadsheetRange):

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = [URL]

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = SpreadsheetID
    SAMPLE_RANGE_NAME = SpreadsheetRange

    def main():
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Data found:')
            #To CSV Operation
            f = open('groups.csv', 'w', encoding="utf-8")
            with f:
                writer = csv.writer(f)
                for row in values:
                    writer.writerow(row)
                    # Print column A, which correspond to index 0.
                    print("Writing (CSV): ", row[0])

#    if __name__ == '__main__':
#        main()