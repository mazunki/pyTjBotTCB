import tts
import tone_analyzer
import telegramSendMessage

def parse_text(data):
    print("listening...", data)
    if data["results"][0]["final"] == True:
        text_output = data["results"][0]["alternatives"][0]["transcript"]  # fucked up json formatting, but who tf cares
        print("You said: {}\n".format(text_output))
        if "%HESITATION" in text_output: 
            tts.watson_play("I'm having an anxiety attack, please let me breathe")
        elif "read" in text_output:
           
            while True:
                try:    
                    print("trying to read something:")
                    update = telegramSendMessage.getUpdates()
                    json_update = update.json()

                    for message in json_update["result"]:
                        tts.watson_play(message["message"]["from"]["first_name"]+" said "+message["message"]["text"])
                        print("trying to say:", message["message"]["text"])
                        with open("lastTgQuery.ini", "w+") as f:
                            f.write(str(message["update_id"]))
                except KeyboardInterrupt:
                    tts.watson_play("I stopped listening to Telegram now.")
                    break
        else: 
            tts.watson_play(text_output)
            telegramSendMessage.send_message(text=text_output)
            
            tone, confidence = tone_analyzer.analyse_text(text_output)
            print("\""+confidence+"\"", sep="")
            tone_output = "I am "+str(round(float(confidence)*100))+"% confident you are "+tone
            print(tone_output)
            tts.watson_play(tone_output)