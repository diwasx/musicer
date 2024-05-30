from lib.queue_song import Queue_song
import threading
import os, subprocess
import sys, time, random
from pprint import pp
from pprint import pp
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
load_dotenv()

CHANNEL_ID = os.environ["CHANNEL_ID"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
client_ = WebClient(token=SLACK_BOT_TOKEN)
ADMIN_ID = f'<@{os.environ["ADMIN_ID"]}>'
MAXSIZE =  int(os.environ["MAXSIZE"])
q = Queue_song(maxsize = MAXSIZE)
print(ADMIN_ID)

def channel_member_rand():
    try:
        result = client_.conversations_members(channel=CHANNEL_ID).get('members')
        while True:
            users_id = random.sample(result, 2)
            user1_id = f"<@{users_id[0]}>"
            user2_id = f"<@{users_id[1]}>"
            print(user1_id==ADMIN_ID, user2_id==ADMIN_ID)
            if(user1_id != ADMIN_ID and user2_id != ADMIN_ID): break

        user1_name = client_.users_info(user=users_id[0]).get('user')['real_name']
        user2_name = client_.users_info(user=users_id[1]).get('user')['real_name']

    except SlackApiError as e:
        print("Error fetching user info: {}".format(e))
    return(user1_id, user1_name, user2_id)

def worker_q():
    while True:
        q.pop()

def worker_r():
    t_sp_refresh = time.time()
    t_s = time.time()
    t_p = time.time()
    tp_diff = random.randint(300, 600)
    # print(tp_diff)

    while True: 
        # print(len(q.info()),", T_S ==>", round(time.time() - t_s))

        if(len(q.info())>0):
            t_s = time.time()

        if(time.time() - t_s >= 120):

            ''' Refresh Spotify Token because it expire after 1 hour'''
            if(time.time() - t_sp_refresh >= 150):
                q.spotify_auth()
                t_sp_refresh = time.time()

            q.add(q.spotify(), "MR ROBOT")
            t_s = time.time()

        # print("T_P ==> ", round(time.time() - t_p))
        if(time.time() - t_p >= tp_diff):
            pl = q.pickup(*tuple(channel_member_rand()))
            # say(pl, user)
            # print(pl)
            t_p = time.time()
            tp_diff = random.randint(300, 600)
            # print(tp_diff)
        # print()

        time.sleep(5)

# Turn-on the queue worker thread.
threading.Thread(target=worker_q, daemon=True).start()
user = 'Diwash Ale'
'''ADD the songs to the queue'''
# q.add(song, user)
# q.add("sataranga", user)
# q.add("illenium gorgeous", user)
# q.add("surface aero cord", user)

# Turn-on the random genenrator worker thread.
threading.Thread(target=worker_r, daemon=True).start()
