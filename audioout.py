import pyaudio
import wave

def play_audio(outputfile):
    wf = wave.open(outputfile, "rb")
    audio_interface = pyaudio.PyAudio()

    CHUNK = 1024
    FORMAT = audio_interface.get_format_from_width(wf.getsampwidth())
    CHANNELS = wf.getnchannels()
    RATE = wf.getframerate()

    # What's the ratio between actual time, RATE and CHUNK? 
    # How many letters/words on average per second?

    audio_stream = audio_interface.open(format = FORMAT,
                                        channels = CHANNELS,
                                        rate=RATE,
                                        output=True,
                                        )

    data = wf.readframes(CHUNK)  # Select first stack
    while data != b"":
        audio_stream.write(data)  # Writing to output stream == Playing sound!
        data = wf.readframes(CHUNK)  # Remove already played from stack, and select next.

    # Cleanup
    audio_stream.close() # Stop the audio stream
    audio_interface.terminate() # Stop the interface connection
    wf.close() # Since we haven't used with wave.open(...) as wf