import pyaudio
import wave
import time
from queue import Queue, Full

CHUNK = 1024
FORMAT = pyaudio.paInt16  # Guessing
CHANNELS = 2
RATE = 44100
BUFFER_SIZE = 16*CHUNK

audio_stack_out = Queue(maxsize=int(BUFFER_SIZE/CHUNK))
not_stopped = None

def audio_from_stack():
    audio_interface = pyaudio.PyAudio()

    def read_from_stack(new_data, frame_count, time_info, status):
        try:
            print("trying to speak")
            data = audio_stack_out.get(frame_count)
            print(audio_stack_out.qsize())
        except Exception as e:
            pass 
        return (data, pyaudio.paContinue)

    sound_stream = audio_interface.open(
                        format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=read_from_stack,
                        start=True,
                       )

    while not_stopped:
        pass  # don't stop me now I'm having such a good time
    else:
        return

if __name__ == "__main__":
    audio_from_stack()
