import os, requests, sys
from dotenv import load_dotenv
from pprint import pp
import time, random, ast
load_dotenv()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_spotify_token():
    ''' GET RANDOM SONGS FROM THE SELECTED PLAYLIST '''
    SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

    auth_url = 'https://accounts.spotify.com/api/token'

    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }

    auth_response = requests.post(auth_url, data=data)
    print("SPOTIFY TOKEN REFRESHED")
    eprint("SPOTIFY TOKEN REFRESHED")
    access_token = auth_response.json().get('access_token')
    return(access_token)



def spotify_random(token):
    ''' GET RANDOM SONGS FROM THE SELECTED PLAYLIST '''
    base_url = 'https://api.spotify.com/v1/playlists/'
    headers = {
        'Authorization': 'Bearer {}'.format(token)
    }
    playlists = ast.literal_eval(os.environ["SPOTIFY_PLAYLIST"])
    pl_endpoint = random.choice(playlists)
    pl_url = ''.join([base_url,pl_endpoint])

    try:
        response = requests.get(pl_url,headers=headers)
    except requests.exceptions as e: 
        print(e)

    songs = []
    for r in response.json()['tracks']['items']:
        s = r['track']['name'] + " - " + r['track']['artists'][0]['name']
        songs.append(s)

    return(songs)

