from watson_developer_cloud import SpeechToTextV1 as stt
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource

from threading import Thread

from creds import credentials
#import text_handler
import audio.audioin
import audio.audioout
import time

error_call = False

class MyRecognizeCallback(RecognizeCallback):
    """
        Pretty much an imported class. Allows us to react to TCP responses from Watson.
    """
    def __init__(self):
        RecognizeCallback.__init__(self)
        print("Callback set.")

    def on_transcription(self, transcript):
        print("Transcription done") 
    
    def on_connected(self):
        print('Connection to IBM Watson was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))
        global error_call
        error_call = True


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

    def on_close(self): 
        print("Connection closed")
            
    
stt_creds = credentials["speech_to_text"]

stt_auth = stt(iam_apikey=stt_creds["api_key"], url=stt_creds["url"])
mycallback = MyRecognizeCallback()

def stt_ws_listener():
    # import pyaudio
    # import queue
    # print("Preparing Watson websocket...")
    # stack = queue.Queue(maxsize=16)

    # def listener(new_data, frame_count, time_info, status):
    #     stack.put(new_data)
    #     return (None, pyaudio.paContinue)

    # print("using audioin ", audioin.stack)
    # a_int = pyaudio.PyAudio()
    # sound_stream = a_int.open(format=pyaudio.paInt16,
    #                         channels=1,
    #                         rate=44100,
    #                         input=True,
    #                         frames_per_buffer=1024,
    #                         start=True,
    #                         stream_callback=listener)

    watson_audio_stack = AudioSource(audioin.stack, is_recording=True, is_buffer=True)
    print("Watson Audio stack created.")

    try:
        socket_output = stt_auth.recognize_using_websocket( 
            audio=watson_audio_stack, 
            content_type="audio/l16; rate=44100", # rate = audioin.py's RATE*CHANNELS 
            recognize_callback=mycallback,
            interim_results=True, # Print all attempts, including not final responses.
            )
        print("Socket quit with message: {}".format(socket_output))
    except:
        print("Error at websocket!!")
        return


def stt_file(name):
    print("Opening file...")

    with open(name, "rb") as audio_file:
        watson_audio_stack = AudioSource(audio_file)

        print("Sending file to Watson...")
        stt_auth.recognize_using_websocket( 
            audio=watson_audio_stack, 
            content_type="audio/flac", # rate = audioin.py's RATE*CHANNELS 
            recognize_callback=mycallback,
            interim_results=True, # Print all attempts, including not final responses.
        )

if __name__ == '__main__':
    #stack = 
    stt_file("testing.wav")

    # stt_ws_listener()

