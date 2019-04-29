import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16  # Guessing
CHANNELS = 1
RATE = 44100
BUFFER_SIZE = 16*CHUNK

def setup():
    audio_interface = pyaudio.PyAudio()
    sound_stream = audio_interface.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True,
    )

    return audio_interface, sound_stream


def play_audio(bit_audio, length=None):
    import time

    audio_int, sound_stream = setup()
    
    sound_stream.start_stream()
    sound_stream.write(bit_audio)
        
    end=time.time()+length
    while end > time.time():
        pass
    
    sound_stream.stop_stream()
    print("Done playing audio.")

def play_file(file_name):
    import time
    print("Playing file:", file_name)
    
    with open(file_name, "rb") as f:
        bit_data = f.read()

    play_audio(bit_data, length=8)

if __name__ == "__main__":
    play_file("hello_world.wav")

