import pyaudio
from queue import Queue, Full

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 44100
BUFFER_SIZE = 16*CHUNK

stopped = False 
testing = False
audio_interface = 0
sound_stream = 0
stack = 0
stack = Queue(maxsize=int(BUFFER_SIZE/CHUNK))

def add_to_stack(new_data, frame_count, time_info, status):
    global stack
    try:
        # print(new_data, "\n")
        stack.put(new_data)
    except Full:
        pass
    return (None, pyaudio.paContinue)

def setup():
    try:
        pass
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
                                start=True,
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
    # print("Created audio interface {}, sound stream {}, and stack {}".format(audio_interface, sound_stream, stack))

    if audio_interface == None:
        print("PyAudio crashed creating microphone.\n")
    elif sound_stream == None:
        print("Microphone stream couldn't be created.\n")
    elif stack == None:
        print("Couldn't set up microphone stack.\n")
    else:
        sound_stream.start_stream()
        print("Microphone should be working.\n")

        global stopped
        try:
            while stopped == False:
                pass  # I'm having a ball. Don't stop me now~
            else:
                if not testing:
                    print("Turning off microphone.")
                    sound_stream.stop_stream()
                    audio_interface.terminate()
                    print("Closing init_audioin")
                    return
                else:
                    return
        except KeyboardInterrupt:
            print("Interrupted audio_in")

def record_file(name, recording_time=5):
    import time

    print("Recording to file \"{}\" for {}s".format(name, recording_time))
    frames = list()
    start_time = time.time()
    end_time = start_time + recording_time
    
    while time.time() < end_time:
        try:
            oldest_frame = stack.get(CHUNK)
            frames.append(oldest_frame)
        except Empty:
            print("Nothing new to add.")
    else:
        print("Recording done. Saving to file...")

        with open(name, "wb") as f:
            f.write(b"".join(frames))
            print("Done.")

if __name__ == '__main__':
    stopped = False
    testing = True
    init_audioin()

    record_file("testing2.wav", 5) 

