from lib.queue_song import Queue_song
import threading
import os, subprocess
import sys, time
from pprint import pp



# if __name__ == "__main__":
q = Queue_song(maxsize = 5)

def worker():
    while True:
        q.pop()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()


song = 'greenday oh love'
user = 'Diwash Ale'

'''ADD the songs to the queue'''
q.add(song, user)
# q.add("sataranga", user)
# q.add("illenium gorgeous", user)
# q.add("surface aero cord", user)
