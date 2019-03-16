from watson_developer_cloud import SpeechToTextV1 as stt
from watson_developer_cloud.websocket import RecognizeCallback

import requests
from threading import Thread

from creds import credentials
import text_handler

class MyRecognizeCallback(RecognizeCallback):
    """
        Pretty much an imported class. Allows us to react to TCP responses from Watson.
    """
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        pass # We're using on_data() to handle everything. This function dismisses valuable information, 
              # and only shows the raw text. Useful for printing output, maybe.

    def on_connected(self):
        print('Connection to IBM Watson was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Watson is now listening')

    def on_hypothesis(self, hypothesis):
        pass
        # Interim results before on_transcription. Same deal.

    def on_data(self, data):
        print("handling")
        text_handler.parse_text(data)

    def on_close(self): 
        print("Connection closed")
    
    
stt_creds = credentials["speech_to_text"]

stt_auth = stt(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])

def stt_ws():
    mycallback = MyRecognizeCallback()
    print("Callback set")
    
    stt_auth.recognize_using_websocket( 
        audio=watson_audio_source, 
        content_type="audio/flac", # rate = audioin.py's RATE*CHANNELS 
        recognize_callback=mycallback,
        interim_results=True, # Print all attempts, including not final responses.
    )

    while True:
        pass
    
        
if __name__ == '__main__':
    watson_stt()
