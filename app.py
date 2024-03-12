from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os, subprocess
import re

from dotenv import load_dotenv
load_dotenv()

APP_ID = os.environ["APP_ID"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
app = App(token=SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_app_mention_events(body, logger, event, client, say):
#   @musicer linkin park numb
    logger.info(body)
    song = event['text'].split(APP_ID)[1].strip()

    if(song == ""):
        say(" @musicer linkin park numb\n@musicer /linkin park numb\n@musicer stop")

    elif(song.lower() == "stop"):
        cmd_yt = f"yt_select.sh ''"
        say(f"Stopped :musical_note:")
        subprocess.run(cmd_yt, shell=True)
    
    elif("/" in song):
        cmd_yt = f"yt_select.sh '/{song}'"
        song = song.replace('/', '')
        # print(cmd_yt, "\n")
        say(f"Playing playlist :musical_note: - {song.upper()}")
        subprocess.run(cmd_yt, shell=True,
            # check=True, text=True
        )

    else:
        cmd_yt = f"yt_select.sh '{song}'"
        # print(cmd_yt, "\n")
        say(f"Playing song :musical_note: - {song.upper()}")
        subprocess.run(cmd_yt, shell=True,
        )

# @app.command("/musicer")
# def repeat_text(ack, respond, command):
#     ack()
#     # /musicer linkin park numb
#     song = command['text'] 
#     respond(f"Playing {song}")
#     cmd_yt = f"yt_select.sh '{song}'"
#     subprocess.run(cmd_yt, shell=True)

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
