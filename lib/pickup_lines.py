import os, requests
from pprint import pp
import time, random, ast
from dotenv import load_dotenv
load_dotenv()

gajal = ast.literal_eval(os.environ["GAJAL"])

def pickup_random(user1_id, user1_name, user2_id):
    ''' GET RANDOM PICKUP LINES '''

    text = ""
    while(text == ""):
        if(random.randint(0,1) == 0):
            for x in gajal.keys():
                if(x in user1_name.lower()):
                    text = random.choice(gajal[x])
        else:
            texts = []
            with open('lib/pickup_lines.txt', 'r') as fh:
                for line in fh:
                    texts.append(line)
            text = random.choice(texts)

        if(random.randint(0,1) == 0):
            text_f = user2_id+" says: Hy "+user1_id+", "+text
        else:
            text_f = "Hy "+user1_id+", "+text+"\nsays: "+user2_id

    # print(text_f)
    return(text_f)

