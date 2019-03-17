import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16  # Guessing
CHANNELS = 2 
RATE = 44100
BUFFER_SIZE = 16*CHUNK

stopped = False
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

        global stopped
        while stopped == False:
            pass  # don't stop me now I'm having such a good time
        else:
            if not testing:
                print("Turning off speaker.")
                sound_stream.stop_stream()
                audio_interface.terminate()
                return
            else:
                return

def play_audio(bit_audio):
    print("Playing audio")
    sound_stream.start_stream()
    sound_stream.write(bit_audio)
    sound_stream.stop_stream()
    print("Done playing audio.")

def play_file(file_name):
    with open(file_name, "rb") as f:
        bit_data = f.read()
    play_audio(bit_data)

def test_if_stack_accessible(name, recording_time=5):
    import time
    import audioin
    import queue

    print("Recording to file \"{}\" for {}s".format(name, recording_time))
    frames = list()
    start_time = time.time()
    end_time = start_time + recording_time

    while time.time() < end_time:
        try:
            oldest_frame = audioin.stack.get(CHUNK)
            frames.append(oldest_frame)
        except queue.Empty:
            print("Nothing new to add.")
    else:
        print("Recording done. Saving to file...")

        with open(name, "wb") as f:
            f.write(b"".join(frames))
            print("Done.")



if __name__ == "__main__":
    not_stopped = False
    test_if_stack_accessible("testing2.wav")
    audioin.init_audioin()
    init_audioout()
    play_file("testing2.wav")

