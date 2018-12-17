from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import random
import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets https://www.googleapis.com/auth/photoslibrary.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1-croQ-emhyaPbo_6kez2jgn-SIjkon5gAI0EHAK1-FE'
ALBUM_ID = 'AIp8kB8tYBMn-4fShHPDQ08uIpttQ2SgWKtT1kFGOqpaAQtdlvWmuoilhdXQWM7KvQf4aCSLQKta'
RANGE_NAME = 'Votes!A2:E'
PHOTOS_CACHE_LOCATION = 'storage/photos.json'

photos_cache = []
photos_service = None
sheets_service = None


def init():
    global photos_service, sheets_service, photos_cache
    if photos_service is not None:
        return
    store = file.Storage('storage/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('storage/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    sheets_service = build('sheets', 'v4', http=creds.authorize(Http()))
    photos_service = build('photoslibrary', 'v1', http=creds.authorize(Http()))

    with open(PHOTOS_CACHE_LOCATION) as f:
        photos_cache = json.loads(f.read())


def get_photos():
    a = random.choice(photos_cache)
    b = random.choice(photos_cache)
    while a == b:
        b = random.choice(photos_cache)
    results = photos_service.mediaItems().batchGet(mediaItemIds=[a, b]).execute()['mediaItemResults']
    return [results[0]['mediaItem'], results[1]['mediaItem']]


def generate_photos():
    results = photos_service.mediaItems().search(body={'albumId': ALBUM_ID}).execute()
    yield results
    while results.get('nextPageToken'):
        results = photos_service.mediaItems().search(body={'albumId': ALBUM_ID, 'pageToken': results['nextPageToken']}).execute()
        yield results


def add_vote(winner_id, loser_id):
    photo_url = f'https://photos.google.com/lr/album/{ALBUM_ID}/photo/{winner_id}'
    sheet = sheets_service.spreadsheets()
    values = {'values': [[winner_id, loser_id, photo_url]]}
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='RAW', body=values).execute()
