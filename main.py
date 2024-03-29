import watson.tts as tts
import watson.stt as stt
import audio.audioout as audioout
import audio.audioin as audioin
import neopixels.led_controller as led_controller
import server_communication.chat_client as chat_client

from threading import Thread
import time

if __name__ == "__main__":

    print("beard")
    
    th_audio_out = Thread(target=audioout.init_audioout, name="maznoski")
    th_audio_in =  Thread(target=audioin.init_audioin, name="MiceLitoris")
    th_watson_stt_socket = Thread(target=stt.stt_ws_listener, name="mr_watson")
    th_server_connection = Thread(target=chat_client.go_online, name="servertalker")
    th_led = Thread(target=led_controller.init_led, name="god")
    
    th_audio_out.start()
    time.sleep(1) # Adding a delay to ensure dependencies set up in correct order
    th_audio_in.start()
    time.sleep(5)
    th_watson_stt_socket.start()
    time.sleep(5)
    th_led.start()
    time.sleep(1)
    th_server_connection.start()


    try:
        while True:
            if th_audio_out.isAlive() and th_audio_in.isAlive() and th_watson_stt_socket.isAlive():
                # tts.watson_play("hello how are you doing")
                if stt.error_call == True:
                    audioin.stopped = True
                    audioout.stopped = True
                
                else:
                    pass
            else:
                audioin.stopped = True
                audioout.stopped = True
                stt.error_call = True
                break
    except KeyboardInterrupt:
        audioout.stopped = True
        audioin.stopped = True
    
    #stt.watson_stt()
