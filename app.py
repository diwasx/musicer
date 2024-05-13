import os, subprocess
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
CHANNEL_ID =  os.environ["CHANNEL_ID"]
app = App(token=SLACK_BOT_TOKEN)
client_ = WebClient(token=SLACK_BOT_TOKEN)
maxsize = 5

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
        if(len(q.info()) >= maxsize):
            say(":interrobang: Queue Full")
        else:
            say(q.add(song, user))


if __name__ == "__main__":
    q = Queue_song(maxsize = maxsize)
    def worker():
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

    threading.Thread(target=worker, daemon=True).start()
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

