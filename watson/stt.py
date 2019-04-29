"""
Allows a constant stream of raw string data from the microphone stream.
"""
from watson_developer_cloud import SpeechToTextV1 as stt
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource

from threading import Thread

from creds import credentials
#import text_handler
import audio.audioin as audioin
import audio.audioout as audioout
import time

output_string = None

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)
        print("Callback set.")

    def on_transcription(self, transcript):
        print("Transcription done") 
    
    def on_connected(self):
        print('Connection to IBM Watson was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Watson is listening...')

    def on_hypothesis(self, hypothesis):
        print("Hypotheses received")
        # Interim results before on_transcription. Not received if interim_results=False

    def on_data(self, data):
        print("Data received:")
        #text_handler.parse_text(data)

        print(data)
        global output_string
        output_string = "police"
        #led_controller.add_to_led("police")
        #print(list(led_controller.led_stack.queue))

    def on_close(self): 
        print("Closed websocket to Watson")

        #led_controller.add_to_led("police")
        #print("closed", list(led_controller.led_stack.queue))


stt_creds = credentials["speech_to_text"]

stt_auth = stt(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])
mycallback = MyRecognizeCallback()

def stt_file(name):
    print("Opening file...")

    with open(name, "rb") as audio_file:
        watson_audio_stack = AudioSource(audio_file)

        print("Sending file to Watson...")
        hi = stt_auth.recognize_using_websocket( 
            audio=watson_audio_stack, 
            content_type="audio/l16;rate=44100", # rate = audioin.py's RATE*CHANNELS 
            recognize_callback=mycallback,
            interim_results=True, # Print all attempts, including not final responses.
        )

        global output_string
        return output_string

if __name__ == '__main__':
    #stack = 
    stt_file("testing.wav")

    # stt_ws_listener()

