import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16  # Guessing
CHANNELS = 1
RATE = 44100
BUFFER_SIZE = 16*CHUNK

audio_interface = pyaudio.PyAudio()
sound_stream = audio_interface.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True
)

def play_audio(bit_audio, length=None):
    import time
    
    sound_stream.start_stream()
    sound_stream.write(bit_audio)
        
    end=time.time()+length
    while end > time.time():
        pass

    sound_stream.stop_stream()
    print("Done playing audio.")

def play_file(file_name):
    import time
    import wave
    print("Playing file:", file_name)
    
    wf = wave.open(file_name, 'rb')
    bit_data = wf.readframes(CHUNK)
    
    sound_stream.start_stream()
    while len(bit_data) > 0:
        sound_stream.write(bit_data)
        bit_data = wf.readframes(CHUNK)
    sound_stream.stop_stream()


if __name__ == "__main__":
    play_file("letsdance.wav")

