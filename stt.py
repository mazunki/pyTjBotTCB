from watson_developer_cloud import SpeechToTextV1 as stt
from watson_developer_cloud.websocket import RecognizeCallback

import requests
from threading import Thread

from creds import credentials
from audioin import stream_stt
import text_handler

def watson_stt():
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

            # Safe closing of program.
            sound_stream.stop_stream()
            sound_stream.close()
            mic.terminate()
            exit()
    
    
    
    stt_creds = credentials["speech_to_text"]
    
    stt_auth = stt(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])
    mic, watson_audio_source, sound_stream = stream_stt()
    
    # print(stt_auth.list_language_models().get_results()) # Unsupported in Lite version

    def stt_ws(*args):
        mycallback = MyRecognizeCallback()
        print("callback set")
        stt_auth.recognize_using_websocket( audio=watson_audio_source, 
                                            content_type="audio/l16; rate=88200", # rate = audioin.py's RATE*CHANNELS 
                                            recognize_callback=mycallback,
                                            interim_results=True, # Print all attempts, including not final responses.
                                          )
    
        
    try:
        listening_thread = Thread(target=stt_ws, args=(), name="speech_to_text_subthread")  # Run stt in the background
        sound_stream.start_stream()  # Start listening
        listening_thread.start()
    
        while True:  # xddddd
            pass
    except KeyboardInterrupt:
        watson_audio_source.completed_recording()  # Tell Watson they can close the session
        
        listening_thread.stop()
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
