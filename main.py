import watson.tts as tts
import watson.stt as stt
import audio.audioout as audioout
import audio.audioin as audioin
import neopixels.led_controller as led_controller
import servo.servo as servo
#import server_communication.chat_client as chat_client

from threading import Thread
import time

if __name__ == "__main__":
    print("\n"*50) 
    th_led = Thread(target=led_controller.init_led)
    th_led.daemon = True
    th_led.start()
    
    audioin.record_file("testing.wav", recording_time=10)
    print("Done recording.")

    my_str = stt.stt_file("testing.wav")
    print("Watson script is released.")
    
    #th_server_connection = Thread(target=chat_client.go_online)

    print("Found message {} in main from Watson".format(my_str))
    if my_str != None and "police" in my_str:
        led_controller.add_to_led("police")
        print("Added a police light")

    th_speaker = Thread(target=audioout.play_file, args=("call911.wav",))
    th_speaker.daemon = True
    th_speaker.start()
    print("And the crowd goes wild!")
    
    th_servo = Thread(target=servo.dance)
    th_servo.daemon = True
    th_servo.start()
    print("Started dancing!")
    
    time.sleep(10)

