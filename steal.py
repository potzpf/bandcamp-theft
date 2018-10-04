#!/usr/bin/env python3

import json

def printAlbum(album):
    print('--- Album Data ---')
    print(f"Artist:  {album['artist']}")
    print(f"Title:   {album['title']}")
    print(f"Date:    {album['date']}")
    print()

    print('--- Track Data ---')
    for track in album['tracks']:
        print(f"No. {track['number']:2} - {track['title']}")
        print(f"Duration: {track['duration']}")
        print()

with open('album-data') as fp:
    data = json.load(fp)

album = {
    'artist': data['artist'],
    'title':  data['current']['title'],
    'date':   data['album_release_date'],
    'tracks': []
    }

for track in data['trackinfo']:
    album['tracks'].append({
        'title':    track['title'],
        'number':   track['track_num'],
        'duration': track['duration'],
        'url':      track['file']['mp3-128']
        })

printAlbum(album)
