"""
Allows using Telegram's API
"""
import requests
import json

api_telegram_url = "http://api.telegram.org/bot"
bot_token = "892823135:AAFE2jL98lx5mTrG3kwKLkQ_TmVQcUShodw"
tg_url = api_telegram_url+bot_token+"/"

def send_message(to_channel="@pyTJBOTTCB", text="from python test"):
    """
    Sends a message to the desired destination.
    """
    rq_url = tg_url + "sendMessage"
    rq_data = {
            "chat_id": to_channel,
            "text": text
            }

    answer = requests.get(rq_url, rq_data)
    print(json.dumps(answer.json()))

def getUpdates():
    """"
    Reads all new messages bot has received.
    """
    rq_url = tg_url + "getUpdates"

    with open("lastTgQuery.ini") as f:
        last_query = int(f.read()) 
    rq_data = {
        "offset": last_query+1 
         }

    #rq_data = {}

    answer = requests.get(rq_url, rq_data)
    print("\n\nReading from Telegram:\n================================\n")
    print(json.dumps(answer.json(), indent=2))
    return answer

if __name__ == "__main__":
    send_message()
