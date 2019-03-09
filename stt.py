from watson_developer_cloud import SpeechToTextV1 as stt
from watson_developer_cloud.websocket import RecognizeCallback

import requests
from threading import Thread

from creds import credentials
from audioin import stream_stt
import tts

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
                print("You said: {}".format(text_output))
                tts.watson_play(text_output)

        def on_close(self):
            print("Connection closed")
            sound_stream.stop_stream()
            sound_stream.close()
            mic.terminate()
    
    
    stt_creds = credentials["speech_to_text"]
    
    stt_auth = stt(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])
    mic, watson_audio_source, sound_stream = stream_stt()
    
    def stt_ws(*args):
        mycallback = MyRecognizeCallback()
        stt_auth.recognize_using_websocket( audio=watson_audio_source, 
                                            content_type="audio/l16; rate=44100",
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
    with open("robotvoice.wav", "rb") as testingfile:
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