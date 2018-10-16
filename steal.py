#!/usr/bin/env python3

import json
import urllib.request
import os
import sys
import re
from pathlib import Path
from mp3_tagger import MP3File

class Track:
    def __init__(self, url, title, number, album = None):
        self.data = {
            'url': url,
            'title': title,
            'number' : number
        }

        if album:
            album.addTrack(self)
            self.album = album


    def copy(self, path, verbose):
        if  self.data['number'] == None:
            name = f"{self.data['title']}.mp3"
        else:
            name = f"{self.data['number']:02} {self.data['title']}.mp3"

        path = os.path.join(path, name)
        if verbose: print(f"downloading {name} to {path}")

        try:
            urllib.request.urlretrieve(self.data['url'], path)
            self.writeTags(path)
        except Exception as e:
            print(f"error downloading {name}: {e}")

    def writeTags(self, path):
        mp3 = MP3File(path)
        mp3.song  = self.data['title']
        mp3.track = self.data['number']

        if self.album:
            mp3.artist = self.album.data['artist']
            mp3.album  = self.album.data['title']
            mp3.year   = self.album.data['year']

        mp3.save()


class Tralbum:
    def __init__(self, artist, year, title):
        self.data = {
            'artist': artist,
            'year':   year,
            'title':  title,
            'tracks': []
        }
        
    def addTrack(self, track):
        self.data['tracks'].append(track)

    """copy the album to the path specified"""
    def copy (self, path, verbose = False):
        path = os.path.expanduser(path)
        dir = Path(path)
        if not dir.exists():
            if verbose: print(f"creating folder {folder}")
            os.makedirs(dir)
        if dir.exists() and not dir.is_dir():
            if verbose: print(f"{folder} is not a directory")
            raise
        
        for track in self.data['tracks']:
            track.copy(path, verbose)


    @staticmethod
    def load(fp):
        data = json.load(fp)
        year = re.search("\d{4}", data['current']['publish_date'])
        album = Tralbum(data['artist'],
                        year,
                        data['current']['title'])

        for track in data['trackinfo']:
            Track(track['file']['mp3-128'],
                  track['title'],
                  track['track_num'],
                  album)

        return album

    def __str__(self):
        str  = f"Artist : {self.data['artist']}\n"
        str += f"Title  : {self.data['title']}\n"
        str += f"Year   : {self.data['year']}\n"
        str += f"Tracks : {len(self.data['tracks'])}"
        
        return str

def main():
    file = "sysin"
    verbose = False
    directory = "~/Music"

    import getopt
    (opts, args) = getopt.getopt(sys.argv[1:], "f:vd:")

    for (k, v) in opts:
        if k == '-f': file = v
        if k == '-v': verbose = True
        if k == '-d': directory = v

    if file == "sysin":
        album = Tralbum.load(sys.stdin)
    else:
        with open(file) as fp:
            album = Tralbum.load(fp)

    if verbose:
        print(album)
        print(f"copying album to {directory}")

    album.copy(directory, verbose)

if __name__ == '__main__': main()
