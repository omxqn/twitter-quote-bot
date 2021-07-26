import tweepy as tw
import time
import json
import requests

CUNSUMER_KEY= '9HosWJf0O6OWIF4XgqXEGsqco'
CUNSUMER_SECRET= 'xtGsk8v15LhTIvrq3fZGkHKZOaJjjRyk7wgbB970BT3izySMQk'

ACCESS_KEY = '925390967557025792-kFWf2XCaMEVWmdbJZM8hgP511LH2VZs'
ACCESS_SECRET = 'vK6PXAMxvnUNdv0GdysYVbevLFf2QeBn5cGlM67hxCJBV'

# Bearer Token=_'AAAAAAAAAAAAAAAAAAAAAMUQSAEAAAAAT3RlEflgR4%2BAamJJ17hWYzHrtqc%3DNzNwhls2k4UYoktjZDu8zFaq2UZwoFF8C2OLPo4WS1Zsyvw8oe'

auth = tw.OAuthHandler(CUNSUMER_KEY,CUNSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
api = tw.API(auth,wait_on_rate_limit=True)


FILE_NAME = 'last_seen_id.txt'



def get_quots():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quots = json_data[0]["q"] + " |-| " + json_data[0]["a"]
  return(quots)



def retraive_last_seen_id(file_name):
    try:
        t = []
        f_read = open(file_name, 'r')
        last_seen_id = f_read.readlines()
        f_read.close()
        for i in last_seen_id:
            t.append(i.removesuffix('\n'))
        return t
    except Exception:
        print("Error getting id")

def store_last_seen_id(last_seen_id,filename):
    f_write = open(filename,'a')
    f_write.write(str(last_seen_id))
    f_write.write("\n")
    f_write.close()
    print(last_seen_id,"Has bees stored")
    return
# 1419187764558540800

'''print(mentions[0].__dict__.keys())
print(mentions[0].text)
print(mentions[0].id)
'''
def replying_to_tweets():

    print("Loading mentions")
    id_list = retraive_last_seen_id(FILE_NAME)
    last_seen_id = id_list[-1].removesuffix('\n')
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):
        print("NEW MENTION ",str(mention.id) + " - " + mention.full_text)
        last_id = mention.id
        
        if "#quote" in mention.full_text.lower() and str(mention.id) not in id_list:
            store_last_seen_id(last_id, FILE_NAME)
            print("Found #quote!")
            print("Responding back \n\n")
            api.update_status('@' + mention.user.screen_name + " " + get_quots() , mention.id)
        else:
            print("There is no hashtag #quote")



while True:
    replying_to_tweets()
    time.sleep(60)
    print("Update...\n\n")
