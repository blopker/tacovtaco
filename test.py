from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/photoslibrary.readonly'

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-croQ-emhyaPbo_6kez2jgn-SIjkon5gAI0EHAK1-FE'
ALBUM_ID = 'AIp8kB8tYBMn-4fShHPDQ08uIpttQ2SgWKtT1kFGOqpaAQtdlvWmuoilhdXQWM7KvQf4aCSLQKta'
SAMPLE_RANGE_NAME = 'A2:E'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    photos_service = build('photoslibrary', 'v1', http=creds.authorize(Http()))
    results = photos_service.mediaItems().search(
        body={'albumId': ALBUM_ID}).execute()
    print(results)

    # # Call the Sheets API
    # sheet = service.spreadsheets()
    # values = {'values': [['taco', 'is', 'best']]}
    # result = sheet.values().append(
    #     spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
    #     valueInputOption='RAW', body=values).execute()
    # values = result.get('values', [])

    # print(values)

if __name__ == '__main__':
    main()

