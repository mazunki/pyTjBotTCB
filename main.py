import watson.tts as tts
import watson.stt as stt
import audio.audioout as audioout
import audio.audioin as audioin
import neopixels.led_controller as led_controller
#import server_communication.chat_client as chat_client

from threading import Thread
import time

if __name__ == "__main__":
    
    th_led = Thread(target=led_controller.init_led)
    th_led.daemon = True
    th_led.start()
    
    audioin.record_file("testing.wav", recording_time=10)
    print("Done recording.")

    my_str = stt.stt_file("testing.wav")
    print("Watson finito")
    
    #th_server_connection = Thread(target=chat_client.go_online)

    #audioout.play_file("testing.wav")


    print("Found message {} in main from Watson".format(my_str))
    if my_str != None and "police" in my_str:
        led_controller.add_to_led("police")
    
    time.sleep(10)

