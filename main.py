import tts
import stt
import audioout
import audioin

from threading import Thread
import time

if __name__ == "__main__":
    
    th_audio_out = Thread(target=audioout.init_audioout)
    th_audio_in =  Thread(target=audioin.init_audioin)
    th_watson_stt_socket = Thread(target=stt.stt_ws_listener)
    
    th_audio_out.start()
    time.sleep(1)
    th_audio_in.start()
    time.sleep(5)
    th_watson_stt_socket.start()
    time.sleep(5)


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
