import os, subprocess, time, random
import threading
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from lib.queue_song import Queue_song
from dotenv import load_dotenv
from pprint import pp
load_dotenv()

APP_ID = os.environ["APP_ID"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
ADMIN_ID = f'<@{os.environ["ADMIN_ID"]}>'
MAXSIZE =  int(os.environ["MAXSIZE"])
app = App(token=SLACK_BOT_TOKEN)
client_ = WebClient(token=SLACK_BOT_TOKEN)

def channel_member_rand():
    try:
        result = client_.conversations_members(channel=CHANNEL_ID).get('members')
        while True:
            users_id = random.sample(result, 2)
            user1_id = f"<@{users_id[0]}>"
            user2_id = f"<@{users_id[1]}>"
            if(user1_id != ADMIN_ID and user2_id != ADMIN_ID): break

        user1_name = client_.users_info(user=users_id[0]).get('user')['real_name']
        user2_name = client_.users_info(user=users_id[1]).get('user')['real_name']

    except SlackApiError as e:
        print("Error fetching user info: {}".format(e))
    return(user1_id, user1_name, user2_id)

@app.event("app_mention")
def handle_app_mention_events(body, logger, event, client, say):
    logger.info(body)
    song = event['text'].split(APP_ID)[1].strip()
    user = f"<@{event['user']}>"


    if(song == ""):
        say(f'''
Hy, {user}
@musicer linkin park numb -- Add song to queue
@musicer info() -- Display queue
@musicer skip() -- Skip song
        ''')

    elif(song.lower() == "info()"):
        say(":information_source: Queued Songs:\n"+str(q.info()).replace(", ", "\n"))

    elif(song.lower() == "skip()"):
        say(q.skip())
    
    else:
        if(len(q.info()) >= MAXSIZE):
            say(":interrobang: Queue Full")
        else:
            say(q.add(song, user))


if __name__ == "__main__":
    q = Queue_song(maxsize = MAXSIZE)
    def worker_q():
        while True:
            if(len(q.info()) > 0):
                title_current = q.info()[0]
                try:
                    result = client_.chat_postMessage(
                        channel=CHANNEL_ID,
                        text = ":arrow_forward: "+title_current
                    )
                except SlackApiError as e:
                    print(f"Error: {e}")
            item = q.pop()

    def worker_r():
        t_s = time.time()
        t_p = time.time()
        diff_ = (600, 900)
        tp_diff = random.randint(*diff_) 

        while True: 
            if(len(q.info())>0):
                t_s = time.time()

            if(time.time() - t_s >= 120):
                try:
                    result = client_.chat_postMessage(
                        channel=CHANNEL_ID,
                        text = q.add(q.spotify(), "- _*MR ROBOT*_") 
                    )
                except SlackApiError as e:
                    print(f"Error: {e}")

                t_s = time.time()

            if(time.time() - t_p >= tp_diff):
                pl = q.pickup(*tuple(channel_member_rand()))
                try:
                    result = client_.chat_postMessage(
                        channel=CHANNEL_ID,
                        text = pl
                    )
                except SlackApiError as e:
                    print(f"Error: {e}")
                t_p = time.time()
                tp_diff = random.randint(*diff_)

            time.sleep(5)

    threading.Thread(target=worker_q, daemon=True).start()
    threading.Thread(target=worker_r, daemon=True).start()
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

