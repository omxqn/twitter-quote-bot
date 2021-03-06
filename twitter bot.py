import tweepy as tw
import time
import requests
import json
from translator import translate
from database import get_table_info, add_new

CUNSUMER_KEY = 'hG3fEUlJQNszuGvc6Z0gYeb67'
CUNSUMER_SECRET = 'FpdSCzwhz5z1IjrKqzEX9r0TunI5HT6YFXFMXTfyXz37tUXrD0'

ACCESS_KEY = '925390967557025792-kFWf2XCaMEVWmdbJZM8hgP511LH2VZs'
ACCESS_SECRET = 'vK6PXAMxvnUNdv0GdysYVbevLFf2QeBn5cGlM67hxCJBV'

# Bearer Token=_'AAAAAAAAAAAAAAAAAAAAAMUQSAEAAAAAT3RlEflgR4%2BAamJJ17hWYzHrtqc%3DNzNwhls2k4UYoktjZDu8zFaq2UZwoFF8C2OLPo4WS1Zsyvw8oe'

auth = tw.OAuthHandler(CUNSUMER_KEY, CUNSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)


# FILE_NAME = 'last_seen_id.txt'


def get_quote(category=None):
    if category == None:
        response = requests.get(f"https://api.quotable.io/random").json()
    else:
        response = requests.get(f"https://api.quotable.io/random?tags={category}").json()
    quote = response['content'].strip()
    author = response['author'].strip()
    return quote, author


def get_quots():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quots = json_data[0]["q"] + " |-| " + json_data[0]["a"]
    return (quots)


'''
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
print(mentions[0].__dict__.keys())
print(mentions[0].text)
print(mentions[0].id)
'''


def replying_to_tweets():
    tags = ['business', 'education', 'faith', 'famous-quotes', 'friendship', 'future', 'happiness', 'history',
            'inspirational', 'life',
            'literature', 'love', 'nature', 'politics', 'religion', 'science', 'success', 'technology', 'wisdom']

    print("Loading mentions")
    id_list = get_table_info('id_list',True)
    last_seen_id = id_list[-1]
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')

    for mention in reversed(mentions):

        for t in tags:
            # "#quote" in mention.full_text.lower() and
            if str(mention.id) not in id_list:

                print("Found unseen mention!")
                if "english" in mention.full_text.lower() or "??????????????" in mention.full_text.lower() or "??????????????" in mention.full_text.lower():
                    # store_last_seen_id(last_id, FILE_NAME) # store the id to file
                    add_new(table='id_list',name=mention.user.screen_name, id=mention.id,
                            message=mention.full_text)  # store the mention info to database
                    print("NEW MENTION ", str(mention.id) + " - " + mention.full_text,
                          f"From: @{mention.user.screen_name}")

                    if t in mention.full_text.lower():
                        quote, author = get_quote(t)  # get a quote
                        api.update_status('@' + mention.user.screen_name + " " + quote + "|-|" + author, mention.id)

                        print("Responding back had been sent!!!! \n\n")
                        break
                    else:
                        quote, author = get_quots()  # get a quote
                        api.update_status('@' + mention.user.screen_name + " " + quote + "|-|" + author, mention.id)

                        print("Responding back had been sent!!!! -No category \n\n")
                        break

                elif "arabic" in mention.full_text.lower() or "????????" in mention.full_text.lower() or "??????????????" in mention.full_text.lower():
                    # store_last_seen_id(last_id, FILE_NAME) # store the id to file
                    add_new(name=mention.user.screen_name, id=mention.id,
                            message=mention.full_text)  # store the mention info to database
                    print("NEW MENTION ", str(mention.id) + " - " + mention.full_text,
                          f"From: @{mention.user.screen_name}")

                    if t in mention.full_text.lower():
                        quote, author = get_quote(t)  # get a quote
                        arabic_quote = translate(quote)  # translate the quote
                        print(f"Translated quote: {arabic_quote}")
                        api.update_status('@' + mention.user.screen_name + " " + arabic_quote + "|-|" + author,
                                          mention.id)

                        print("???? ?????????? ????????!!!! \n\n")
                        break
                    else:
                        quote, author = get_quots()  # get a quote
                        arabic_quote = translate(quote)  # translate the quote
                        print(f"Translated quote: {arabic_quote}")
                        api.update_status('@' + mention.user.screen_name + " " + arabic_quote + "|-|" + author,
                                          mention.id)

                        print("???? ?????????? ????????!!!! ???????????? ?????????? \n\n")
                        break
            else:
                print("There isn't any new mention \n\n")


while True:
    replying_to_tweets()
    time.sleep(60)
    print("Update...\n\n")
