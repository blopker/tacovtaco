from src import api
import json


def main():
    ids = []
    api.init()
    for a in api.generate_photos():
        for m in a['mediaItems']:
            if 'video' not in m['mimeType']:
                ids.append(m['id'])
    with open('storage/photos.json', 'w') as f:
        f.write(json.dumps(ids))


if __name__ == "__main__":
    main()
