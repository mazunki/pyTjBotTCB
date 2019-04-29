import pyaudio
from queue import Queue, Full, Empty

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
BUFFER_SIZE = 16*CHUNK

stack = Queue(maxsize=int(BUFFER_SIZE/CHUNK))

def add_to_stack(new_data, frame_count, time_info, status):
    global stack
    try:
        stack.put(new_data)
    except Full:
        pass
    return (None, pyaudio.paContinue)

audio_interface = pyaudio.PyAudio()  # Python interface to PortAudio, check `class PyAudio` of pyaudio.py.
sound_stream = audio_interface.open(
    format=FORMAT, 
    channels=CHANNELS, 
    rate=RATE, 
    input=True, 
    frames_per_buffer=CHUNK,
    stream_callback=add_to_stack,
)
print("")

def record_file(name, recording_time=5):
    import time

    print("Recording to file \"{}\" for {}s".format(name, recording_time))
    frames = list()
    end_time = time.time() + recording_time
    
    global sound_stream
    sound_stream.start_stream()

    while time.time() < end_time:
        try:
            oldest_frame = stack.get(CHUNK)
            frames.append(oldest_frame)
        except Empty:
            print("Nothing new to add.")
    else:
        print("Recording done. Saving to file...")

        sound_stream.stop_stream()
        sound_stream.close()
        with open(name, "wb") as f:
            f.write(b"".join(frames))
            print("Done.")

if __name__ == '__main__':
    record_file("hello_world.wav", 8) 

