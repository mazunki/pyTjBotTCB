import watson.tts as tts
import watson.stt as stt
import audio.audioout as audioout
import audio.audioin as audioin
import neopixels.led_controller as led_controller

from threading import Thread
import time

if __name__ == "__main__":
    audioin.stopped = True
    audioin.testing = True
    audioin.init_audioin()

    audioin.record_file("sample.wav", 8)

    time.sleep(1)

    audioout.stopped = True
    audioout.external_connection = True
    audioout.play_file("sample.wav")
