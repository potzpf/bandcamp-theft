#!/usr/bin/env python3

import json
import urllib.request
import os
import sys
from pathlib import Path

class Tralbum:
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

    """copy the album to the path specified"""
    def copy (self, folder, verbose = False):
        folder = os.path.expanduser(folder)
        dir = Path(folder)
        if not dir.exists():
            if verbose: print(f"creating folder {folder}")
            os.makedirs(dir)
        if dir.exists() and not dir.is_dir():
            if verbose: print(f"{folder} is not a directory")
            raise
        
        for track in self.data['tracks']:
            if track['number'] == None:
                fname = f"{track['title']}.mp3"
            else:
                fname = f"{track['number']:02} {track['title']}.mp3"
                
            path = os.path.join(folder, fname)
            if verbose: print(f"downloading {fname} to {path}")
            
            try:
                urllib.request.urlretrieve(track['url'], path)
            except Exception as e:
                print(f"error downloading {fname}: {e}")

    @staticmethod
    def load(fp):
        data = json.load(fp)

        album = Tralbum(data['artist'],
                        data['current']['publish_date'],
                        data['current']['title'])

        for track in data['trackinfo']:
            album.addTrack(track['track_num'],
                           track['title'],
                           track['duration'],
                           track['file']['mp3-128'])

        return album

    def __str__(self):
        str  = f"Artist : {self.data['artist']}\n"
        str += f"Title  : {self.data['title']}\n"
        str += f"Date   : {self.data['date']}\n"
        str += f"Tracks : {len(self.data['tracks'])}"
        
        return str

def main():
    file = "sysin"
    verbose = False
    directory = "~/Music"

    import getopt
    (opts, args) = getopt.getopt(sys.argv[1:], "f:vd:")
    print(opts)
    print(args)

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
