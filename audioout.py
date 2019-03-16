import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16  # Guessing
CHANNELS = 2
RATE = 44100
BUFFER_SIZE = 16*CHUNK

not_stopped = True
audio_interface = 0
sound_stream = 0

def setup():
    global audio_interface
    global sound_stream

    try:
        audio_interface = pyaudio.PyAudio()
    except Exception as e:
        print(e)
        audio_interface = None
        sound_stream = None

    try:
        sound_stream = audio_interface.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            output=True,
                            frames_per_buffer=CHUNK,
                            start=False)
    except Exception as e:
        print(e)
        sound_stream = None

    return audio_interface, sound_stream


def init_audioout():
    print("Setting up speaker...")
    global audio_interface
    global sound_stream
    audio_interface, sound_stream = setup()

    if audio_interface == None:
        print("PyAudio crashed creating speaker.\n")
    elif sound_stream == None:
        print("Speaker stream couldn't be created.\n")
    else:
        print("Speaker should be working.\n")

        while not_stopped:
            pass  # don't stop me now I'm having such a good time
        else:
            print("Turning off speaker.")
            return

def play_audio(bit_audio):
    print("Playing audio")
    sound_stream.start_stream()
    sound_stream.write(bit_audio)
    sound_stream.stop_stream()
    print("Done playing audio.")


if __name__ == "__main__":
    pass