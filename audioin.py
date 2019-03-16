import pyaudio
from queue import Queue, Full

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
BUFFER_SIZE = 16*CHUNK

not_stopped = True
audio_interface = 0
sound_stream = 0
stack = 0

def add_to_stack(new_data, frame_count, time_info, status):
    global stack
    try:
        stack.put(new_data)
    except Full:
        pass
    return (None, pyaudio.paContinue)

def setup():
    try:
        global stack
        stack = Queue(int(BUFFER_SIZE/CHUNK))
    except:
        print("Couldn't set up stack.")
        stack = None
        return None, None

    try:
        audio_interface = pyaudio.PyAudio()  # Python interface to PortAudio, check `class PyAudio` of pyaudio.py.
    except:
        audio_interface = None
        sound_stream = None
        stack = None
    finally:
        try:
            sound_stream = audio_interface.open(
                                format=FORMAT, 
                                channels=CHANNELS, 
                                rate=RATE, 
                                input=True, 
                                frames_per_buffer=CHUNK,
                                stream_callback=add_to_stack,
                                start=False,
                           )
        except:
            sound_stream = None
            stack = None

    return audio_interface, sound_stream


def init_audioin():
    print("Setting up microphone...")
    global audio_interface
    global sound_stream
    audio_interface, sound_stream = setup()

    if audio_interface == None:
        print("PyAudio crashed creating microphone.\n")
    elif sound_stream == None:
        print("Microphone stream couldn't be created.\n")
    elif stack == None:
        print("Couldn't set up microphone stack.\n")
    else:
        sound_stream.start_stream()
        print("Microphone should be working.\n")

        while not_stopped:
            pass  # I'm having a ball. Don't stop me now~
        else:
            print("Turning off microphone.")
            sound_stream.stop_stream()
            audio_interface.terminate()


if __name__ == '__main__':
    #stream_stt()
    pass
