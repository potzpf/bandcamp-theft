#!/usr/bin/env python3

import json
import urllib.request
import os
import sys
from pathlib import Path

class Album:
    def __init__(self, artist, date, title):
        self.data = {
            'artist': artist,
            'date':   date,
            'title':  title,
            'tracks': []
        }
        
    def addTrack(self, number, title, duration, url):
        self.data['tracks'].append({
            'number':   number,
            'title':    title,
            'duration': duration,
            'url':      url
        })

    """download the album to the folder specified"""
    def download(self, folder):
        dir = Path(folder)
        if not dir.exists():
            os.makedirs(dir)
        if dir.exists() and not dir.is_dir():
            raise
        
        for track in self.data['tracks']:
            if track['number'] == None:
                fname = f"{track['title']}.mp3"
            else:
                fname = f"{track['number']:02} {track['title']}.mp3"
                
            path = os.path.join(folder, fname)
            print(fname)
            
            try:
                urllib.request.urlretrieve(track['url'], path)
            except Exception as e:
                print(f"error downloading {fname}: {e}")

            
        

    def __str__(self):
        str  = f"Artist : {self.data['artist']}\n"
        str += f"Title  : {self.data['title']}\n"
        str += f"Date   : {self.data['date']}\n"
        str += f"Tracks : {len(self.data['tracks'])}"
        
        return str

def main():
    data = json.load(sys.stdin)

    album = Album(data['artist'],
                  data['current']['publish_date'],
                  data['current']['title'])

    for track in data['trackinfo']:
        album.addTrack(track['track_num'],
                       track['title'],
                       track['duration'],
                       track['file']['mp3-128'])

    print(album)
    album.download("dl/")

if __name__ == '__main__': main()
