import watson.tts as tts
import watson.tone_analyzer as tone_analyzer
import telegram.telegramSendMessage as telegramSendMessage

def do_stuff(text):
    while True:
        update = telegramSendMessage.getUpdates()
        json_update = update.json()
        for message in json_update["result"]:
           tts.watson_play(message["message"]["from"]["first_name"]+" said "+message["message"]["text"])
           print("trying to say:", message["message"]["text"])
           with open("lastTgQuery.ini", "w+") as f:
               f.write(str(message["update_id"]))

if __name__ == '__main__':
    do_stuff("what are you doing")
