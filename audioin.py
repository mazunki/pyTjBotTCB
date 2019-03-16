import pyaudio
from watson_developer_cloud.websocket import AudioSource  # So we can open a connection between mic and Watson
from queue import Queue, Full

import audioout

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
BUFFER_SIZE = 16*CHUNK

audio_interface = pyaudio.PyAudio()  # Python interface to PortAudio, check `class PyAudio` of pyaudio.py.

stack = audioout.audio_stack_out

def audio_to_stack():
    def add_to_stack(new_data, frame_count, time_info, status):
        """
            Try to add audio to the stack. If it's full, move on.
        """
        try:
            print("trying to add to stack")
            stack.put(new_data)
            print(stack.qsize())
        except Full:
            pass
        return (None, pyaudio.paContinue)
    
    sound_stream = audio_interface.open(format=FORMAT, 
                                        channels=CHANNELS, 
                                        rate=RATE, 
                                        input=True, 
                                        frames_per_buffer=CHUNK,
                                        stream_callback=add_to_stack,
                                        start=False,
                                       ) 

    while True:
        pass  # I'm having a ball. Don't stop me now~

if __name__ == '__main__':
    #stream_stt()
    pass
