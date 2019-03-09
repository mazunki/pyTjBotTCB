import pyaudio
from watson_developer_cloud.websocket import AudioSource  # So we can open a connection between mic and Watson
from queue import Queue, Full

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
BUFFER_SIZE = 16*CHUNK

audio_interface = pyaudio.PyAudio()  # Python interface to PortAudio, check `class PyAudio` of pyaudio.py.

def stream_stt():
    stack = Queue(maxsize=int(BUFFER_SIZE/CHUNK))  # Allows us to save and load binary audio safely from a stack. 
    watson_audio_source = AudioSource(stack, is_recording=True, is_buffer=True)  # Opens a TCP socket to IBM Watson services, pointed towards the stack. 
    
    def pyaudio_callback(new_data, frame_count, time_info, status):
        """
            Try to add audio to the stack. If it's full, move on.
        """
        try:
            stack.put(new_data)
        except Full:
            pass
        return (None, pyaudio.paContinue)
    
    sound_stream = audio_interface.open(format=FORMAT, 
                                        channels=CHANNELS, 
                                        rate=RATE, 
                                        input=True, 
                                        frames_per_buffer=CHUNK,
                                        stream_callback=pyaudio_callback,
                                        start=False
                                       )
    
    return audio_interface, watson_audio_source, sound_stream
    

def file_stt():
    import wave
    WAVE_OUTPUT_FILENAME = "testing.wav"
    frames = []

    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio_interface.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()