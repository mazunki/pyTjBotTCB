import watson.tts as tts
import watson.tone_analyzer as tone_analyzer
import telegram.telegramSendMessage as telegramSendMessage

def do_stuff(text):
    if "%HESITATION" in text: 
        tts.watson_play("I'm having an anxiety attack, please let me breathe")

    # Telegram listening, not tested after refactor 16/03
    #elif "read" in text_output:
    #    while True:
    #        try:    
    #            print("trying to read something:")
    #            update = telegramSendMessage.getUpdates()
    #            json_update = update.json()
#
    #            for message in json_update["result"]:
    #                tts.watson_play(message["message"]["from"]["first_name"]+" said "+message["message"]["text"])
    #                print("trying to say:", message["message"]["text"])
    #                with open("lastTgQuery.ini", "w+") as f:
    #                    f.write(str(message["update_id"]))
    #        except KeyboardInterrupt:
    #            tts.watson_play("I stopped listening to Telegram now.")
    #            break

    elif text.split()[0] in ["light", "shine"]:
        import neopixels.led_controller as led_controller
        if "rainbow" in text.split()[1:]:
            led_controller.add_to_led("rainbow")
        elif "police" in text.split()[1:]:
            led_controller.add_to_led("police")

    else: 
        tts.watson_play(text)
        #telegramSendMessage.send_message(text=text)
        
        tone, confidence = tone_analyzer.analyse_text(text)
        print("\""+confidence+"\"", sep="")
        tone_output = "I am "+str(round(float(confidence)*100))+"% confident you are "+tone
        print(tone_output)
        tts.watson_play(tone_output)    


def parse_text(data):
    print("listening...", data)
    if data["results"][0]["final"] == True:
        text_output = data["results"][0]["alternatives"][0]["transcript"]  # fucked up json formatting, but who tf cares
        print("You said: {}\n".format(text_output))

        do_stuff(text_output)

if __name__ == '__main__':
    do_stuff("what are you doing")