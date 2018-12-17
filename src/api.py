from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import random

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/photoslibrary.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1-croQ-emhyaPbo_6kez2jgn-SIjkon5gAI0EHAK1-FE'
ALBUM_ID = 'AIp8kB8tYBMn-4fShHPDQ08uIpttQ2SgWKtT1kFGOqpaAQtdlvWmuoilhdXQWM7KvQf4aCSLQKta'
RANGE_NAME = 'Votes!A2:E'

photos_service = None
sheets_service = None


def init():
    global photos_service, sheets_service
    if photos_service is not None:
        return
    store = file.Storage('storage/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('storage/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    sheets_service = build('sheets', 'v4', http=creds.authorize(Http()))
    photos_service = build('photoslibrary', 'v1', http=creds.authorize(Http()))


def get_photos():
    results = photos_service.mediaItems().search(body={'albumId': ALBUM_ID}).execute()
    all_photos = results['mediaItems']
    random.shuffle(all_photos)
    return all_photos[:2]


def add_winner(photo_id):
    photo_url = f'https://photos.google.com/lr/album/{ALBUM_ID}/photo/{photo_id}'
    sheet = sheets_service.spreadsheets()
    values = {'values': [[photo_id, photo_url]]}
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='RAW', body=values).execute()
