import pyaudio
import wave

def play_audio(outputfile):
    wf = wave.open(outputfile, "rb")
    audio_interface = pyaudio.PyAudio()

    CHUNK = 1024
    FORMAT = audio_interface.get_format_from_width(wf.getsampwidth())
    CHANNELS = wf.getnchannels()
    RATE = wf.getframerate()

    audio_stream = audio_interface.open(format = FORMAT,
                                        channels = CHANNELS,
                                        rate=RATE,
                                        output=True,
                                        )

    data = wf.readframes(CHUNK)
    while data != b"":
        audio_stream.write(data)
        data = wf.readframes(CHUNK)

    audio_stream.close()
    audio_interface.terminate()
    wf.close()