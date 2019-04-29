import watson.tts as tts
import watson.stt as stt
import audio.audioout as audioout
import audio.audioin as audioin
import neopixels.led_controller as led_controller
import servo.servo as servo
import telegram.telegramSendMessage as telegram
#import server_communication.chat_client as chat_client

from threading import Thread
import time

if __name__ == "__main__":
    print("\n"*50) 
    
    while True:
        audioin.record_file("inputaudio.wav", recording_time=10)
        print("Done recording.")

        my_str = stt.stt_file("inputaudio.wav")
        print("Watson script is released.")
        
        print("Found message {} in message from Watson".format(my_str))
        if my_str != None and "read" in my_str:
            print("Telegram assistant on the run!")
            update = telegramSendMessage.getUpdates()
            json_update = update.json()
            for message in json_update["result"]:
                tts.watson_play(message["message"]["from"]["first_name"]+" said "+message["message"]["text"])
                print("trying to say:", message["message"]["text"])
                with open("lastTgQuery.ini", "w+") as f:
                    f.write(str(message["update_id"]))
        else:
            telegram.send_message(text=my_str)


