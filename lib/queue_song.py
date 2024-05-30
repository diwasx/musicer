import os, subprocess, threading, sys
from queue import Queue
import lib.spotify_api as spo
import lib.pickup_lines as pl
import time, random

class Queue_song:

    def __init__(self, maxsize):
        self.q = Queue(maxsize = maxsize)
        self.spotify_auth()

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def spotify_auth(self):
        self.spotify_token = spo.get_spotify_token()

    def info(self):
        '''Return Queue list'''

        text_r = [l['title']+" - "+l['user'] for l in self.q.queue]
        return(text_r)

    def add(self, song, user):

        '''Search Yewtube for the songs and get the url'''
        p1=subprocess.Popen(["yt", f"/{song}", ",1"], start_new_session=True)

        sh_title = "playerctl metadata xesam:title"
        music_title = subprocess.run(sh_title, shell=True, capture_output=True, text=True).stdout.strip()
        time.sleep(8)
        while(music_title == "" or music_title == "No players found"):
            print(music_title)
            time.sleep(2)
            music_title = subprocess.run(sh_title, shell=True, capture_output=True, text=True).stdout.strip()

        sh_artist = "playerctl metadata xesam:artist"
        music_artist = subprocess.run(sh_artist, shell=True, capture_output=True, text=True).stdout.strip()

        sh_url = "playerctl metadata xesam:url"
        music_url = subprocess.run(sh_url, shell=True, capture_output=True, text=True).stdout.strip()

        sh_len= "playerctl metadata mpris:length"
        music_len = int(subprocess.run(sh_len, shell=True, capture_output=True, text=True).stdout)/(1000000)
        print(music_len, "\n")

        title_full = music_title+" - "+music_artist

        self.q.put({
            "title": title_full,
            "url": music_url,
            "len": music_len,
            "user": user
            }, block=False)

        '''KILL PROCESS'''
        subprocess.Popen(["kill", "-TERM -- ", f"-{p1.pid}"])

        # print(f"{title_full}\n:musical_note:ADDED TO QUEUE BY {user}")
        text_r = (f"{title_full}\n:musical_note:ADDED TO QUEUE BY {user}")
        return(text_r)

    def pop(self):
        ''' Play the next queue song '''
        item = self.q.get()

        url = item['url']
        p1=subprocess.Popen(["mpv", f"{item['url']}", "--no-video"], start_new_session=True)

        self.e = threading.Event()
        self.e.wait(timeout=item['len']+3) 

        pk = subprocess.run("killall yt mpv", shell=True, capture_output=True, text=True).stdout.strip()
        print(f"Finished {item['title']}\n")
        return(item)

    def skip(self):
        ''' Skip current song '''
        if hasattr(self, 'e'):
            self.e.set()
        else:
            print("Nothing to skip")
            self.eprint("Nothing to skip")

    def spotify(self):
        ''' GET RANDOM SONGS FROM THE SELECTED PLAYLIST '''
        songs = spo.spotify_random(self.spotify_token)
        song = random.choice(songs)
        return(song)

    def pickup(self, user1_id, user1_name, user2_id):
        ''' GET RANDOM PICKUP LINES '''
        lines = pl.pickup_random(user1_id, user1_name, user2_id)
        return(lines)

