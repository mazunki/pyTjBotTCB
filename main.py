import tts
import stt
import audioout
import audioin

from threading import Thread
import time

if __name__ == "__main__":
    
    th_audio_out = Thread(target=audioout.init_audioout)
    th_audio_in =  Thread(target=audioin.init_audioin)
    th_watson_stt_socket = Thread(target=stt.stt_ws)
    
    th_audio_out.start()
    time.sleep(1)
    th_audio_in.start()
    time.sleep(1)
    th_watson_stt_socket.start()
    time.sleep(5)


    try:
        while True:
            tts.watson_play("hello how are you doing")
            pass
    except KeyboardInterrupt:
        th_audio_out.not_stopped = False
        th_audio_in.not_stopped = False
    
    #stt.watson_stt()
