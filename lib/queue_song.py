import os, subprocess, threading
from queue import Queue
import time

class Queue_song:

    def __init__(self, maxsize):
        self.q = Queue(maxsize = maxsize)


    def info(self):
        '''Return Queue list'''

        text_r = [l['title']+" - "+l['user'] for l in self.q.queue]
        return(text_r)

    def add(self, song, user):

        '''Search Yewtube for the songs and get the url'''
        p1=subprocess.Popen(["yt", f"/{song}", ",1"], start_new_session=True)

        sh_title = "playerctl metadata xesam:title"
        tmp_title = music_title = subprocess.run(sh_title, shell=True, capture_output=True, text=True).stdout.strip()
        time.sleep(8)
        # while(music_title == "" or music_title==tmp_title):
        while(music_title == ""):
            print(music_title)
            time.sleep(2)
            music_title = subprocess.run(sh_title, shell=True, capture_output=True, text=True).stdout.strip()

        sh_artist = "playerctl metadata xesam:artist"
        music_artist = subprocess.run(sh_artist, shell=True, capture_output=True, text=True).stdout.strip()

        sh_url = "playerctl metadata xesam:url"
        music_url = subprocess.run(sh_url, shell=True, capture_output=True, text=True).stdout.strip()

        sh_len= "playerctl metadata mpris:length"
        music_len = int(subprocess.run(sh_len, shell=True, capture_output=True, text=True).stdout)/(1000000)

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
        self.e.wait(timeout=item['len']) 

        pk = subprocess.run("killall mpv", shell=True, capture_output=True, text=True).stdout.strip()
        print(f"Finished {item['title']}\n")
        return(item)

    def skip(self):
        ''' Skip current song '''
        self.e.set()
