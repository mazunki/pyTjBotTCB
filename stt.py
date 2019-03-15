from watson_developer_cloud import SpeechToTextV1 as stt
from watson_developer_cloud.websocket import RecognizeCallback

import requests
from threading import Thread

from creds import credentials
from audioin import stream_stt
import tts
import tone_analyzer
import telegramSendMessage

def watson_stt():
    class MyRecognizeCallback(RecognizeCallback):
        """
            Pretty much an imported class. Allows us to react to TCP responses from Watson.
        """
        def __init__(self):
            RecognizeCallback.__init__(self)

        def on_transcription(self, transcript):
            print(transcript)

        def on_connected(self):
            print('Connection was successful')

        def on_error(self, error):
            print('Error received: {}'.format(error))

        def on_inactivity_timeout(self, error):
            print('Inactivity timeout: {}'.format(error))

        def on_listening(self):
            print('Service is listening')

        def on_hypothesis(self, hypothesis):
            print(hypothesis)

        def on_data(self, data):
            print(data)
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
                    #tts.watson_play(text_output)
                    #telegramSendMessage.send_message(text=text_output)
                    tone, confidence = tone_analyzer.analyse_text(text_output)
                    print("\""+confidence+"\"", sep="")
                    tone_output = "I am "+str(round(float(confidence)*100))+"% confident you are "+tone
                    print(tone_output)
                    tts.watson_play(tone_output)

        def on_close(self):
            print("Connection closed")
            sound_stream.stop_stream()
            sound_stream.close()
            mic.terminate()
    
    
    
    stt_creds = credentials["speech_to_text"]
    
    stt_auth = stt(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])
    mic, watson_audio_source, sound_stream = stream_stt()
    
    # print(stt_auth.list_language_models().get_results()) # Unsupported in Lite version

    def stt_ws(*args):
        mycallback = MyRecognizeCallback()
        stt_auth.recognize_using_websocket( audio=watson_audio_source, 
                                            content_type="audio/l16; rate=88200", # rate = audioin.py's RATE*CHANNELS 
                                            recognize_callback=mycallback,
                                            interim_results=True, # Print all attempts, including not final responses.
                                          )
    
    sound_stream.start_stream()  # Start listening
    
    try:
        recognize_thread = Thread(target=stt_ws, args=())  # Keep sending audio pieces to Watson
        recognize_thread.start()
    
        while True:  # xddddd
            pass
    except KeyboardInterrupt:
        watson_audio_source.completed_recording()  # Tell Watson they can close the session
        sound_stream.stop_stream() # Stop sending audio
        sound_stream.close() # Close audio stream
        mic.terminate() # Close interface


def stt_file():
    
    stt_creds = credentials["speech_to_text"]
    
    stt_auth = stt(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])
    mic, watson_audio_source, sound_stream = stream_stt()
    
    with open("testing.wav", "rb") as testingfile:
        print(stt_creds["api_key"])
        resp = requests.post(   stt_creds["url"]+"/v1/recognize", 
                                headers={
                                            "Content-Type": "audio/wav"
                                        },
                                auth=("apikey", stt_creds["api_key"]), 
                                data=testingfile
                            )
    a = resp.json()
    print(a)


if __name__ == '__main__':
    watson_stt()
